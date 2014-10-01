<script type='text/javascript'>
$(document).ready(function(){

	// powers python data
	var treeData = {{powertree|tojson}};
	//var treeData = [{'name':'Top','parent':'null','children':[
	//		{'name':'A','parent':'Top'},{'name':'B','parent':'Top'}
	//	]}];

	// initial variables ; shape of SVG container
	var margin = {top:40, right: 120, bottom: 20, left: 120};
	var height = 600 - margin.top - margin.bottom;
	var width = 600 - margin.right - margin.left;
	var i=0, duration=750, root;
	
	// build d3 tree with nodes and links (ie. leaves and branches)
	var tree = d3.layout.tree().size([height,width]);
	
	// function to define links between nodes; draws Bezier curves
	var diagonal = d3.svg.diagonal().projection(function(d) {return [d.y,d.x]; }); 
	
	// create and append an SVG element to the html element id=powers
	var svg = d3.select('#powers').append('svg')
		.attr('width', width + margin.right + margin.left)
		.attr('height', height + margin.top + margin.bottom)
		.append('g')
		.attr('transform', 'translate('+margin.left+','+margin.top+')');
	
	// set top level of data as the root of the tree	
	root = treeData[0];
	root.y0 = 0;
	root.x0 = height / 2;
	
	// collapse all initial children
	function collapse(d) {
    	if (d.children) {
      	  d._children = d.children;
      	  d._children.forEach(collapse);
      	  d.children = null;
    	}
	}
	root.children.forEach(collapse);
	
	//update the root and draw the tree
	update(root);
	
	// define update function
	function update(source){
		// compute the new tree layout
		var nodes = tree.nodes(root).reverse();
		var links = tree.links(nodes);
		
		// define fixed spacing between node levels
		nodes.forEach(function(d) { d.y = d.depth * 180; });
		
		// define node so it knows the select one with appropriate id
		var node = svg.selectAll('g.node').data(nodes, function(d) { return d.id || (d.id = ++i);});
		
		// On Enter
		// define action of entering node into position
		var nodeEnter = node.enter().append('g').attr('class', 'node')
			.attr('transform', function(d) {return 'translate('+source.y0+','+source.x0+')';})
			.on('click', click);
		
		// add circles and text
		nodeEnter.append('circle').attr('r',1e-6)
			.style('fill',function(d) {return d._children ? 'lightsteelblue' : '#fff'; });
		nodeEnter.append('text')
			.attr('x', function(d) {return d.children || d._children ? -10 : 10; })
			.attr('y', '0.35em')
			.attr('text-anchor', function(d) {return d.children || d._children ? 'end' : 'start'; })
			.text(function(d) {return d.name;})
			.style('fill-opacity', 1e-6);
			
		// On Update
		// transition nodes to new positions
		var nodeUpdate = node.transition().duration(duration)
			.attr('transform', function(d) {return 'translate('+d.y+','+d.x+')';});
		
		// update circles and text
		nodeUpdate.select('circle').attr('r',5.5)
			.style('fill',function(d) {return d._children ? 'lightsteelblue' : '#fff'; });
		nodeUpdate.select('text').style('fill-opacity',1);
		
		// On Exit
		// define exit transition actions
		var nodeExit = node.exit().transition().duration(duration)
			.attr('transform', function(d) {return 'translate('+source.y+','+source.x+')';})
			.remove();
			
		// update circles and text	
		nodeExit.select('circle').attr('r',1e-6);
		nodeExit.select('text').style('fill-opacity',1e-6);
		
		// update the links
		var link = svg.selectAll('path.link').data(links, function(d){return d.target.id; });
		
		// add new links at parent's previous position
		link.enter().insert('path','g').attr('class','link')
			.attr('d', function(d) {
				var o = {x: source.x0, y: source.y0};
				return diagonal({source: o, target: o});
			});
		
		// transition links to new positions and during exits
		link.transition().duration(duration).attr('d',diagonal);	
		link.exit().transition().duration(duration)
			.attr('d', function(d) {
				var o = {x: source.x, y: source.y};
				return diagonal({source: o, target: o});
			}).remove();
			
		// stash old position
		nodes.forEach(function(d){
			d.x0 = d.x;
			d.y0 = d.y;
		});
		
	}
	
	// Toggle children on click
	function click(d) {
		if (d.children) {
			d._children = d.children;
			d.children = null;
		} else {
			d.children = d._children;
			d._children = null;
		}
		update(d);
	}
	
});
</script>