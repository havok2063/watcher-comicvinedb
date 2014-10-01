
from __future__ import print_function
from __future__ import division
import pycomicvine, pdb, datetime, time
import argparse, socket, sqlalchemy
import pycomicvine.error as pcverr

# import db stuff
cpulist = ['havok','polaris']
if any(x in socket.gethostname().lower() for x in cpulist):
    from db.connections.MyLocalConnection import db
else:
    from db.connections.MyTunnelConnection import db    
import db.cvModelClasses as cvdb

_author_ = 'Brian Cherinka'

class addCharacterToDB:

    def __init__(self, name=None,quiet=False, console=None, key=None,
        limit=10, range=None, sleeptime=5, reverse=False):        
        ''' initialize '''
        
        self.name = name
        self.key = key
        self.quiet = quiet
        self.limit = limit
        self.range = range
        self.endloop = False
        self.sleeptime = sleeptime
        self.reverse = reverse
        if console: self.args = self.setArgs()
        if self.key: pycomicvine.api_key = self.key
        else: 
            print('Error: No API key set')
            return
        
        # Start session 
        self.session = db.Session()
        with self.session.begin():
            if self.name:
                self.getCharacter()
                self.loadCharacter(self.character)
            else:
                self.loopCharacters()
                #tmp = map(self.loadCharacter, self.character)
                
                
    def setArgs():
        ''' parse command line arguments '''
        
        parser = argparse.ArgumentParser(prog='addCharacterToDB', usage='%(prog)s [options]')
        parser.add_argument('-k', '--key', type=str, help='api_key to use for database', default=None, required=True)
        parser.add_argument('-q', '--quiet', action='store_true', help='turn off verbosity', default=False)
        parser.add_argument('-n', '--name', type=str, help='character name to add', default=None)
        parser.add_argument('-l', '--limit', type=int, help='limit of character loop', default=10)
        parser.add_argument('-r', '--range', type=str, help='range of character ids to search over', default=None)
        
        self.arg = parser.parse_args()

        if not self.arg.key: parser.error('No API key set.  Please set it.')
        
        if self.key == None: self.key = self.arg.key
        if self.quiet == None: self.quiet = self.arg.quiet
        if self.name == None: self.name = self.arg.name
        if self.limit == None: self.limit = self.arg.limit
        if self.range == None: self.range = self.arg.range
        
    def getCharacter(self):
        ''' Retrieve a character from the database'''
        
        characterlist = pycomicvine.Characters(filter='name:{0}'.format(self.name), all=True)
        counts = [c.count_of_issue_appearances for c in characterlist]
        self.character = characterlist[counts.index(max(counts))]
    
    def loopCharacters(self):
        ''' Loop over many characters and create list''' 
        
        if self.range:
            start = int(self.range.split('-')[0])
            end = int(self.range.split('-')[1])
        else: 
            start=0
            end = start + self.limit
            
        self.character = []
        for i in xrange(start,end+1):
            try: self.character.append(pycomicvine.Character(i,all=True))
            except: pass            
           
    	    
    def loadIntoDB(self, character=None):
        ''' Recursively load the characters into the database '''
        
        if character == None:
            self.character = pycomicvine.Characters()
        else:
            self.character = [character] if type(character) == str else character
            
        # reverse the list
        if self.reverse:
            self.character = list(self.character)
            self.character = self.character.reverse()
                
        # run loop
        while not self.endloop:
            try:
                tmp = [self.loadCharacter(character) for character in self.character]
            except: pass
            else: self.endloop=True
        
    def rebuildDB(self):
        ''' rebuild the db from scratch '''
        
        self.mapPublishers()
        self.loadTeams(None)
        self.loadPowers(None)
        self.loadStoryArcs(None)
        self.mapOrigins()
        self.mapPowersToClass()
        self.loadCreators(None)
        self.loadLocations(None)
        self.mapVolumes()

        
    def loadCharacter(self, character):
        ''' Load the character '''
        
        char = None
        try:
            char = self.session.query(cvdb.Character).filter_by(id = character.id).one()
        except sqlalchemy.orm.exc.MultipleResultsFound:
            print('Error: More than one character found.  Expecting only one! \n\n')
            raise
        except sqlalchemy.orm.exc.NoResultFound:
            if not self.quiet: print('No existing character found. Adding character {0}'.format(character.id))
            pass   
        
        # load new character
        if char == None:
            char = cvdb.Character()
            char.name = character.name
            char.id = character.id
            char.aliases = character.aliases
            char.deck = character.deck
            char.description = character.description
            char.issue_count = character.count_of_issue_appearances     
            if character.first_appeared_in_issue: char.first_issue = character.first_appeared_in_issue.id
            try:
                char.issues_died_in = [i.id for i in character.issues_died_in]
                if character.character_friends: char.friends = [i.id for i in character.character_friends]
                if character.character_enemies: char.enemies = [i.id for i in character.character_enemies]
                if character.team_friends: char.team_friends = [i.id for i in character.team_friends]
                if character.team_enemies: char.team_enemies = [i.id for i in character.team_enemies]
                if character.origin: char.origin = self.loadOrigin(character.origin)
            except pcverr.RateLimitExceededError:
                print('Error: Rate Limit Exceeded in Character')
                print('Waiting for {0} minutes'.format(self.sleeptime/60.))
                time.sleep(self.sleeptime)
                raise
                       
            # connect character to powers
            try:
                powers = character.powers
                powerlist = [self.session.query(cvdb.Power).filter_by(id=pow.id).one() for pow in powers]
                char.powers = powerlist
            except pcverr.RateLimitExceededError:
                print('Error: Rate Limit Exceeded in Character Power')
                print('Waiting for {0} minutes'.format(self.sleeptime/60.))
                time.sleep(self.sleeptime)
                raise
                            
            # connect character to teams
            try:
                teams = character.teams
                teamlist = [self.session.query(cvdb.Team).filter_by(id=team.id).one() for team in teams]
                char.teams = teamlist
            except pcverr.RateLimitExceededError:
                print('Error: Rate Limit Exceeded in Character Teams')
                print('Waiting for {0} minutes'.format(self.sleeptime/60.))
                time.sleep(self.sleeptime)                
                raise
                            
            # connect character to creators
            try:
                creators = character.creators
                creatorlist = [self.session.query(cvdb.Creator).filter_by(id=creator.id).one() for creator in creators]
                char.creators = creatorlist            
            except pcverr.RateLimitExceededError:
                print('Error: Rate Limit Exceeded in Character Creator')
                print('Waiting for {0} minutes'.format(self.sleeptime/60.))
                time.sleep(self.sleeptime)                
                raise
                
        self.char = char
                
        # load new identity
        ident = None
        try:
            ident = self.session.query(cvdb.Identity).filter_by(name = character.real_name).one()
        except sqlalchemy.orm.exc.MultipleResultsFound:
            print('Error: More than one identity found.  Expecting only one! \n\n')
            raise
        except sqlalchemy.orm.exc.NoResultFound:
            if not self.quiet: print('No existing identity found.')
            pass           
        
        if ident == None:
            ident = cvdb.Identity()
            ident.name = character.real_name
            ident.birth = character.birth
            # gender
            if character.gender: ident.gender = self.session.query(cvdb.Gender).filter_by(pk=character.gender-1).one()    
            
            #connect character to identities
            ident.characters = [char]
        
        # Add into database    
        self.session.add(char)
        self.session.add(ident)


            
    def loadOrigin(self, charorig):
        ''' Load origin into db'''
            
        origin = None
        try: 
            origin = self.session.query(cvdb.Origin).filter_by(id = charorig.id).one()
        except sqlalchemy.orm.exc.MultipleResultsFound:
            print('Error: More than one origin found.  Expecting only one! \n\n')
            raise
        except sqlalchemy.orm.exc.NoResultFound:
            if not self.quiet: print('No existing origin found.')
            pass              
        
        # load new origin
        if origin == None:
            origin = cvdb.Origin()
            self.session.add(origin)
            origin.id = charorig.id
            origin.name = charorig.name
            
        return origin
    
    def mapOrigins(self):
        ''' load all origins '''
        
        origlist = pycomicvine.Origins()
        tmp = map(self.loadOrigin, origlist)
            
    def loadIssues(self, iss):
        ''' Load the issues of a character '''
        
        # Get issue
        try:
            issue = self.session.query(cvdb.Issue).filter_by(id = iss.id).one()
        except sqlalchemy.orm.exc.MultipleResultsFound:
            print('Error: More than one issue found.  Expecting only one! \n\n')
            raise
        except sqlalchemy.orm.exc.NoResultFound:
            if not self.quiet: print('No existing issue found. Adding issue {0}'.format(iss.id))
            pass

        # Add new issues    
        if issue == None:
            issue = cvdb.Issue()
            issue.id = iss.id
            issue.name = iss.name
            try:
                issue.cover_date = iss.cover_date if iss.cover_date else None
                issue.aliases = iss.aliases
                issue.store_date = iss.store_date if iss.store_date else None
                issue.deck = iss.deck
                issue.description = iss.description
                issue.issue_number = iss.issue_number
                issue.first_appearances = [c.id for c in iss.first_appearance_characters]
                issue.first_appearance_teams = [c.id for c in iss.first_appearance_teams]
                issue.first_appearance_locations = [c.id for c in iss.first_appearance_locations]
                issue.volume = self.loadVolume(iss.volume)
            except pcverr.RateLimitExceededError:
                print('Error: Rate Limit exceeded. Waiting..')
            
            # Connect to characters
            try:
                characters = iss.character_credits
                charlist = [self.session.query(cvdb.Character).filter_by(id=character.id).one() for character in characters]
                issue.characters = charlist
            except pcverr.RateLimitExceededError:
                print('Error: Rate Limit Exceeded in Issue Character')
                print('Waiting for {0} minutes'.format(self.sleeptime/60.))
                time.sleep(self.sleeptime)
                raise        
                
            # Connect to creators
            try:
                creators = iss.person_credits
                creatorlist = [self.session.query(cvdb.Creator).filter_by(id=creator.id).one() for creator in creators]
                issue.creators = creatorlist
            except pcverr.RateLimitExceededError:
                print('Error: Rate Limit Exceeded in Issue Creator')
                print('Waiting for {0} minutes'.format(self.sleeptime/60.))
                time.sleep(self.sleeptime)
                raise                  

            # Connect to teams
            try:
                teams = iss.team_credits
                teamlist = [self.session.query(cvdb.Team).filter_by(id=team.id).one() for team in teams]
                issue.teams = teamlist
            except pcverr.RateLimitExceededError:
                print('Error: Rate Limit Exceeded in Issue Team')
                print('Waiting for {0} minutes'.format(self.sleeptime/60.))
                time.sleep(self.sleeptime)
                raise 

            # Connect to story arc
            try:
                stories = iss.story_arc_credits
                storylist = [self.session.query(cvdb.StoryArcs).filter_by(id=story.id).one() for story in stories]
                issue.storyarcs = storylist
            except pcverr.RateLimitExceededError:
                print('Error: Rate Limit Exceeded in Issue Story')
                print('Waiting for {0} minutes'.format(self.sleeptime/60.))
                time.sleep(self.sleeptime)
                raise 

            # Connect to location
            try:
                locations = iss.location_credits
                loclist = [self.session.query(cvdb.Location).filter_by(id=location.id).one() for location in locations]
                issue.locations = loclist
            except pcverr.RateLimitExceededError:
                print('Error: Rate Limit Exceeded in Issue Location')
                print('Waiting for {0} minutes'.format(self.sleeptime/60.))
                time.sleep(self.sleeptime)
                raise 

        # Add into database    
        self.session.add(issue)
                                                                        
    def loadVolume(self, vol):
        ''' Load the volume into db '''
        
        volume = None
        try: 
            volume = self.session.query(cvdb.Volume).filter_by(id = vol.id).one()
        except sqlalchemy.orm.exc.MultipleResultsFound:
            print('Error: More than one volume found.  Expecting only one! \n\n')
            raise
        except sqlalchemy.orm.exc.NoResultFound:
            if not self.quiet: print('No existing volume found. Adding volume {0}'.format(vol.id))
            pass              
        
        # load new origin
        if volume == None:
            volume = cvdb.Volume()
            self.session.add(volume)
            volume.id = vol.id
            volume.name = vol.name
            try:
                volume.aliases = vol.aliases
                volume.issue_count = vol.count_of_issues
                if vol.start_year: volume.start_year = vol.start_year if type(vol.start_year) == int else int(vol.start_year.split('-')[0]) if vol.start_year.split('-')[0].isdigit() else None
                volume.deck = vol.deck
                volume.description = vol.description
                if vol.first_issue: volume.first_issue = vol.first_issue.id
                if vol.last_issue: volume.last_issue = vol.last_issue.id
                volume.publisher = self.loadPublisher(vol.publisher)
            except pcverr.RateLimitExceededError:
                print('Error: Rate Limit exceeded. Exiting..')
                return volume
                            
        return volume        
    
    def mapVolumes(self, index=None):
        ''' load all volumes '''
        
        if index:
            vollist = pycomicvine.Volumes(filter='id:{0}'.format(index))
        else:
            vollist = pycomicvine.Volumes()
        
        tmp = map(self.loadVolume, vollist)
        self.session.flush()
                    
    def loadPublisher(self,pub):
        ''' Load the publisher into the db '''
        
        publisher = None
        try: 
            publisher = self.session.query(cvdb.Publisher).filter_by(id = pub.id).one()
        except sqlalchemy.orm.exc.MultipleResultsFound:
            print('Error: More than one publisher found.  Expecting only one! \n\n')
            raise
        except sqlalchemy.orm.exc.NoResultFound:
            if not self.quiet: print('No existing publisher found. Adding publisher {0}'.format(pub.id))
            pass
        except AttributeError:
            print('Error: No publisher id')
            return None
            
        # load new publisher
        if publisher == None:
            publisher = cvdb.Publisher()
            self.session.add(publisher)
            publisher.id = pub.id
            publisher.name = pub.name
            try:
                publisher.aliases = pub.aliases
                publisher.deck = pub.deck
                publisher.description = pub.description
            except pcverr.RateLimitExceededError:
                print('Error: Rate Limit exceeded. Exiting..')
                return publisher
                        
        return publisher                               
    
    def mapPublishers(self, index=None):
        ''' load all publishers '''
        
        if index:
            publist = pycomicvine.Publishers(filter='id:{0}'.format(index))
        else:
            publist = pycomicvine.Publishers()
        tmp = map(self.loadPublisher, publist)
        self.session.flush()
            
    def loadPowers(self,character):
        ''' load powers into db '''
        
        if character == None:
            powerlist = pycomicvine.Powers()
        else:
            powerlist = character.powers
        
            
        for pow in powerlist:
            power = None
            try:
                power = self.session.query(cvdb.Power).filter_by(id = pow.id).one()
            except sqlalchemy.orm.exc.MultipleResultsFound:
                print('Error: More than one power found.  Expecting only one! \n\n')
                raise
            except sqlalchemy.orm.exc.NoResultFound:
                if not self.quiet: print('No existing power found. Adding power {0}'.format(pow.id))
                pass
            
            # load new one    
            if power == None:
                power = cvdb.Power()
                self.session.add(power)
                power.id = pow.id
                power.name = pow.name
                power.aliases = pow.aliases
                power.description = pow.description
                
        self.session.flush()
                
    def loadTeams(self, character):
        ''' load teams into db '''
        
        if character == None:
            teamlist = pycomicvine.Teams()
        else:
            teamlist = character.teams
            
        for t in teamlist:
            team = None
            try:
                team = self.session.query(cvdb.Team).filter_by(id = t.id).one()
            except sqlalchemy.orm.exc.MultipleResultsFound:
                print('Error: More than one team found.  Expecting only one! \n\n')
                raise
            except sqlalchemy.orm.exc.NoResultFound:
                if not self.quiet: print('No existing team found. Adding team {0}'.format(t.id))
                pass
            
            # load new one    
            if team == None:
                team = cvdb.Team()
                self.session.add(team)
                team.id = t.id
                team.name = t.name
                team.aliases = t.aliases
                team.description = t.description
                team.deck = t.deck    
                team.member_count = t.count_of_team_members
                team.issue_count = t.count_of_issue_appearances
                try: team.first_issue = t.first_appeared_in_issue.id
                except: pass 
                
        self.session.flush()
        
    def loadStoryArcs(self, issue):
        ''' load story arcs into db '''
        
        if issue == None:
            storylist = pycomicvine.StoryArcs()
        else:
            storylist = issue.story_arc_credits
            
        for story in storylist:           
            storyarc = None
            try:
                storyarc = self.session.query(cvdb.StoryArc).filter_by(id = story.id).one()
            except sqlalchemy.orm.exc.MultipleResultsFound:
                print('Error: More than one story found.  Expecting only one! \n\n')
                raise
            except sqlalchemy.orm.exc.NoResultFound:
                if not self.quiet: print('No existing story found. Adding story {0}'.format(story.id))
                pass
            
            # load new one    
            if storyarc == None:
                storyarc = cvdb.StoryArc()
                self.session.add(storyarc)
                storyarc.id = story.id
                storyarc.name = story.name
                storyarc.aliases = story.aliases
                storyarc.description = story.description
                storyarc.deck = story.deck    
                storyarc.issue_count =  story.count_of_issue_appearances
                try: storyarc.first_issue = story.first_appeared_in_issue.id
                except: pass 
                
        self.session.flush()          
        
    def loadCreators(self, character):
        ''' load creators into db '''
        
        if character == None:
            creatorlist = pycomicvine.People()
        else:
            creatorlist = character.creators
            
        for person in creatorlist:
            creator = None
            try:
                creator = self.session.query(cvdb.Creator).filter_by(id = person.id).one()
            except sqlalchemy.orm.exc.MultipleResultsFound:
                print('Error: More than one creator found.  Expecting only one! \n\n')
                raise
            except sqlalchemy.orm.exc.NoResultFound:
                if not self.quiet: print('No existing creator found. Adding creator {0}'.format(person.id))
                pass
            
            # load new one    
            if creator == None:
                creator = cvdb.Creator()
                self.session.add(creator)
                creator.id = person.id
                creator.name = person.name
                creator.description = person.description
                creator.deck = person.deck
                if person.aliases: creator.aliases = person.aliases
                if person.birth: creator.birth = person.birth
                if person.hometown: creator.hometown = person.hometown
                if person.death: creator.death = person.death
                if person.country: creator.country = person.country
                if person.gender: creator.gender = person.gender
                
                # gender
                if person.gender: creator.gender = self.session.query(cvdb.Gender).filter_by(pk=person.gender-1).one()    

                
        self.session.flush()
        
    def mapPowersToClass(self):
        ''' Map all powers to their class '''
        
        # list for 130 powers, in order of pk
        pclist = [0,0,0,0,0,0,1,1,1,3,2,1,2,2,4,7,5,0,0,0,2,3,4,4,2,8,6,4,1,9,6,2,0,0,6,8,7,4,0,0,7,4,2,8,4,4,1,1,2,5,5,1,1,1,8,4,6,7,3,0,1,2,6,0,2,6,4,5,6,2,7,4,1,2,3,4,4,5,1,7,2,3,4,7,2,2,4,1,3,8,7,4,1,8,0,8,5,4,3,9,4,0,7,1,4,4,8,4,2,0,0,2,7,7,2,2,1,1,4,0,0,5,0,4,4,8,8,7,4,4]                     
        pc = {0:'Physical',1:'Mental',2:'Energy',3:'Spacetime',4:'Biology',5:'Training',6:'Technology',7:'Magic',8:'Elemental',9:'Economy'}
         
        powers = self.session.query(cvdb.Power).all()
        
        # check same length
        if len(powers) != len(pclist): 
            print('Error: Power list and index list must be the same length.')
            return
        
        # Perform mapping
        for i,power in enumerate(powers):
            powerclass = session.query(cvdb.PowerClass).filter_by(name=pc[pclist[i]]).one()
            power.powerclass = powerclass
            
    def loadLocations(self,issue):
        ''' load locations into db'''
        
        if issue == None:
            loclist = pycomicvine.Locations()
        else:
            loclist = issue.location_credits
            
        for loc in loclist:           
            location = None
            try:
                location = self.session.query(cvdb.Location).filter_by(id = loc.id).one()
            except sqlalchemy.orm.exc.MultipleResultsFound:
                print('Error: More than one location found.  Expecting only one! \n\n')
                raise
            except sqlalchemy.orm.exc.NoResultFound:
                if not self.quiet: print('No existing location found. Adding location {0}'.format(loc.id))
                pass
            
            # load new one    
            if location == None:
                location = cvdb.Location()
                self.session.add(location)
                location.id = loc.id
                location.name = loc.name
                location.aliases = loc.aliases
                location.description = loc.description
                location.deck = loc.deck    
                location.issue_count =  loc.count_of_issue_appearances
                if loc.start_year: location.start_year = loc.start_year if type(loc.start_year) == int else int(loc.start_year.split('-')[0]) if loc.start_year.split('-')[0].isdigit() else None
                try: location.first_issue = loc.first_appeared_in_issue.id
                except: pass 
                
        self.session.flush()             
    
        
        
            
        
            
        
        
        