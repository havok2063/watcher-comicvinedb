#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
import pycomicvine, sys, argparse, pdb

pycomicvine.api_key = 'd4fe17508ca365e7b3678411f5f8fc0db7594963'

def displayData(c, issues):
    ''' display some information'''
    
    fa = c.first_appeared_in_issue
    print('--- {0} ---'.format(c.name))
    print(u'First appeared in: {0} #{1}, {2}, "{3}"'.format(fa.volume.name, fa.issue_number, fa.cover_date.strftime('%m/%d/%y'),fa.name))
    print('Total number of issues: {0}'.format(c.count_of_issue_appearances))
    print('{0} has died in {1} issues.'.format(c.name, len(c.issues_died_in)))
    if len(c.issues_died_in) > 0:
        print('Issue Death List:')
        for issue in c.issues_died_in:
            print(u'{0}, #{1}, {2}, "{3}"'.format(issue.volume.name, issue.issue_number, issue.cover_date.strftime('%m/%d/%y'), issue.name))
    print(' ')
    

def characterXMatch(character1, character2, format='ids'):
    '''cross matches two characters'''
    
    clist1 = pycomicvine.Characters(filter='name:{0}'.format(character1), all=True)
    clist2 = pycomicvine.Characters(filter='name:{0}'.format(character2), all=True)
    
    # Assume the right character is always the one with the most issues in the list, MAY NOT BE TRUE
    c1count = [c.count_of_issue_appearances for c in clist1]
    c2count = [c.count_of_issue_appearances for c in clist2]
    c1 = clist1[c1count.index(max(c1count))]
    c2 = clist2[c2count.index(max(c2count))]
    
    # Grab Issue ids
    cids1 = [i.id for i in c1.issue_credits]
    cids2 = [i.id for i in c2.issue_credits]
    
    # X-match
    xmatch=list(set(cids1) & set(cids2))    
    c1percent = round(len(xmatch)/c1.count_of_issue_appearances*100,1)
    c2percent = round(len(xmatch)/c2.count_of_issue_appearances*100,1)
    #xiss = [c1.issue_credits[cids1.index(x)] for x in xmatch]
    #xsec = [x.cover_date.strftime('%s') for x in xiss if x.cover_date]
    #fa = xiss[xsec.index(min(xsec))]
    
    print(' ')
    print('{0} and {1} appeared in {2} issues together!'.format(character1, character2, len(xmatch)))
    print('This is {0}% of {1} issues an {2}% of {3} issues!'.format(c1percent, character1, c2percent, character2))
    #print(u'They first appeared together in {0} #{1}, {2}!'.format(fa.name, fa.issue_number, fa.cover_date.strftime('%m/%d/%y')))
    print(' ')
    
    # If format is Issues, then return list of Issue objects, instead of Issue ids
    #if format=='issues':
    #    xmatch = [c1.issue_credits[cids1.index(x)] for x in xmatch]

    # print data
    displayData(c1,xmatch)
    displayData(c2,xmatch)
        
    return xmatch 


def parseArgs():
    
    parser = argparse.ArgumentParser(prog='comicvine', usage='%(prog)s [options]')
    
    parser.add_argument('-f', '--first', type=str, dest='character1', help='first character', default=None, nargs='*')
    parser.add_argument('-s', '--second', type=str, dest='character2', help='second character', default=None, nargs='*')
    
    opts = parser.parse_args()
    opts.character1 = ' '.join(opts.character1)
    opts.character2 = ' '.join(opts.character2)
    
    return opts
    
def main(args):
    
    # parse arguments
    opts = parseArgs()
    
    # cross match
    xmatch = characterXMatch(opts.character1, opts.character2)
    

if __name__=='__main__':
    main(sys.argv[1:])










