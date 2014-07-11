

			var limit_text = function(string) {
				if (string.length >= 10) {
					return string.substring(0,9)+"...";
				}
				else {
					return string
				}
			}

			var smallest_element_in_list = function(list) {
				var best_len = 1000;
				for (var i = 0; i<list.length; i++) {
					if (list[i].length < best_len) {
						output = list[i];
						best_len = list[i].length
					}
				}
				return output;
			}

			var first_short_element = function(list, N) {
				for (var i=0 ; i<list.length; i++) {
					if (list[i].length <= N) {
						return list[i]
					}
				}
				// if there are none under N, return shortest
				return smallest_element_in_list(list)
			}

			var randomize_color = function(string_colour) {
				var r1 = Math.round(Math.random()*10)
				var r2 = Math.round(Math.random()*10)
				var r3 = Math.round(Math.random()*10)
				return '#'+string_colour[1]+r1+string_colour[3]+r2+string_colour[5]+r3
			}

			function randomIntFromInterval(min,max)
				{
				    return Math.floor(Math.random()*(max-min+1)+min);
				}

			d3.json("grid.json", function(json) {
				dataset = json; 
				idealSize = $(window).height()*0.9
				//idealSize = $('#grid').width()
				padding = 2

				var maxX = d3.max(dataset, function(d) { return d['x']; });
				var maxY = d3.max(dataset, function(d) { return d['y']; });
				var maxFB = d3.max(dataset, function(d) { return d['fb']; })
				var minRed = d3.min(dataset, function(d) { return d['r']; })
				var maxRed = d3.max(dataset, function(d) { return d['r']; })
				var minBlue = d3.min(dataset, function(d) { return d['b']; })
				var maxBlue = d3.max(dataset, function(d) { return d['b']; })
				var maxCluster = d3.max(dataset, function(d) { return d['cluster']; })

				// Setting the padding Bostock way
				var margin = {top: 10, right: 10, bottom: 10, left: 10};
				var width = idealSize - margin.left - margin.right, height = idealSize*maxY/maxX - margin.top - margin.bottom;
	    		var svg = d3.select("#grid")
	    					.append("svg")
				   			.attr("width", width + margin.left + margin.right)
				   			.attr("height", height + margin.top + margin.bottom)
				  			.append("g")
				    		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");


				//Create scale functions
				var xScale = d3.scale.linear()
									 .domain([0, maxX+1])
									 .range([0, width]);

				var yScale = d3.scale.linear()
									 .domain([0, maxY+1])
									 .range([0, height]);

				var sizeScale = d3.scale.linear()
									 .domain([0, maxFB])
									 .range([0, width/maxY]);
				
				var labelScale = d3.scale.linear()
									 .domain([7, 20])
									 .range([13, 5]);

				var hslScale = d3.scale.linear()
									 .domain([0, maxCluster])
									 .range([0,200]);

				var fbScale = d3.scale.linear()
									 .domain([0, maxFB])
									 .range([0.5,0.8]);


				//Create shapes
				type = 'rect'
				//type = 'image'
				svg.selectAll(type)
				   .data(dataset)
				   .enter()
				   .append(type)
				   //.attr("transform", "translate(250, 0) rotate(45)")  // If rotating to diamond formation
				   .attr( {
				   		x: function(d,i) {return xScale(d['x'])},
				   		y: function(d) {return yScale(d['y'])},
				   		width: width/(maxX+1)-padding,
				   		height: height/(maxY+1)-padding,
				   		// width: function(d) {return sizeScale(d['fb'])},
				   		// height: function(d) {return sizeScale(d['fb'])},
				   		// fill: function(d) {return "rgb("+Math.round(redScale(d['r']))+", "+d['g']+", "+Math.round((blueScale(d['b'])))+")"}
				   		fill: function(d) { 
				   			return d3.hsl ( hslScale(d['cluster'])+((Math.random()*30)) ,
				   											(Math.random()/4.0)+0.7 ,
				   											randomIntFromInterval(5,6)/10 )
				   							}

				   		//'xlink:href': function(d) {return d['img']},  // Set 'rect' to 'image' if we want to show image
				   })
				   .on("mouseover", function(d) {
			   		d3.select(this)
			   			.attr("fill", "white");
			   		d3.select('#headline')
			   			.text(function() {return d['headline']})
			   		d3.select('#standfirst')
			   			.html(function() {return d['standfirst']})
				   })
				   .on("mouseout", function(d) {
					   d3.select(this)
					   		.transition()
					   		.duration(350)
							.attr("fill", 
								function(d) { 
				   			return d3.hsl ( hslScale(d['cluster'])+((Math.random()*30)) ,
				   											(Math.random()/4.0)+0.66 ,
				   											randomIntFromInterval(5,8)/10 )
				   							}
									)
				   })
				   .on("click", function(d) {
				   		alert(d['url'])
				   		$(location).attr('href', d['url']);
				   		window.open(d['url'],'_blank');
				   })

				svg.selectAll("text")
				   .data(dataset)
				   .enter()
				   .append("text")
				   .text(function(d) {return first_short_element(d['tags'],1)
					})
				   .attr("x", function(d,i) {return xScale(d['x']+0.47)
				   })
				   .attr("y", function(d,i) {return yScale(d['y']+0.52)
				   })
				   .attr("font-family", "sans-serif")
				   .attr("font-size", labelScale(maxX))
				   .attr("fill", "black")
				   .attr("text-anchor", "middle")
				   .style("pointer-events", "none")

				   
			});