#!/usr/bin/env python3

from collections import OrderedDict

def line_chart(SampleModel, main_title = 'Number of Samples / Fluids publicly available in SRA by Year', label_1 = 'Samples', label_2 = 'Fluids'):
    samples = SampleModel.objects.all()
    samples_count = OrderedDict({
        'before 2011' : 0,
        2011 : 0,
        2012 : 0,
        2013 : 0,
        2014 : 0,
        2015 : 0,
        2016 : 0,
        2017 : 0,
        2018 : 0
    })
    fluids = OrderedDict({
        'before 2011' : set(),
        2011 : set(),
        2012 : set(),
        2013 : set(),
        2014 : set(),
        2015 : set(),
        2016 : set(),
        2017 : set(),
        2018 : set()
    })

    for sample in samples:
        year = int(sample.DateString.replace('/', '-').split('-')[0])
        fluid = sample.Fluid
        if year < 2011:
            samples_count['before 2011'] += 1
            fluids['before 2011'].add(fluid)
        elif year > 2018:
            samples_count[2018] += 1
            fluids[2018].add(fluid)
        else:
            samples_count[year] += 1
            fluids[year].add(fluid)

    fluids = {year : len(fluids[year]) for year in fluids}

    samples_count[2011] += samples_count['before 2011']
    samples_count[2012] += samples_count[2011]
    samples_count[2013] += samples_count[2012]
    samples_count[2014] += samples_count[2013]
    samples_count[2015] += samples_count[2014]
    samples_count[2016] += samples_count[2015]
    samples_count[2017] += samples_count[2016]
    samples_count[2018] += samples_count[2017]

    fluids[2011] += fluids['before 2011']
    fluids[2012] += fluids[2011]
    fluids[2013] += fluids[2012]
    fluids[2014] += fluids[2013]
    fluids[2015] += fluids[2014]
    fluids[2016] += fluids[2015]
    fluids[2017] += fluids[2016]
    fluids[2018] += fluids[2017]

    samples_data = [samples_count[year] for year in samples_count]
    fluids_data = [fluids[year] for year in fluids]

    template = '''
    	<script src="static/build/js/Chart.bundle.js"></script>
    	<script src="static/build/js/utils.js"></script>
    	<script src="static/build/js/jquery.2.1.3.min.js"></script>
    	<style>
    		canvas{{
    			-moz-user-select: none;
    			-webkit-user-select: none;
    			-ms-user-select: none;
    		}}
    		.chartjs-tooltip {{
    			opacity: 1;
    			position: absolute;
    			background: rgba(0, 0, 0, .7);
    			color: white;
    			border-radius: 3px;
    			-webkit-transition: all .1s ease;
    			transition: all .1s ease;
    			pointer-events: none;
    			-webkit-transform: translate(-50%, 0);
    			transform: translate(-50%, 0);
    			padding: 4px;
    		}}

    		.chartjs-tooltip-key {{
    			display: inline-block;
    			width: 10px;
    			height: 10px;
    		}}
    	</style>

    	<div id="canvas-holder1" style="width:75%;">
    		<canvas id="chart1"></canvas>
    		<div class="chartjs-tooltip" id="tooltip-0"></div>
    		<div class="chartjs-tooltip" id="tooltip-1"></div>
    	</div>
    	<script>
    		var customTooltips = function(tooltip) {{
    			$(this._chart.canvas).css('cursor', 'pointer');

    			var positionY = this._chart.canvas.offsetTop;
    			var positionX = this._chart.canvas.offsetLeft;

    			$('.chartjs-tooltip').css({{
    				opacity: 0,
    			}});

    			if (!tooltip || !tooltip.opacity) {{
    				return;
    			}}

    			if (tooltip.dataPoints.length > 0) {{
    				tooltip.dataPoints.forEach(function(dataPoint) {{
    					var content = [dataPoint.xLabel, dataPoint.yLabel].join(': ');
    					var $tooltip = $('#tooltip-' + dataPoint.datasetIndex);

    					$tooltip.html(content);
    					$tooltip.css({{
    						opacity: 1,
    						top: positionY + dataPoint.y + 'px',
    						left: positionX + dataPoint.x + 'px',
    					}});
    				}});
    			}}
    		}};
    		var color = Chart.helpers.color;
    		var lineChartData = {{
    			labels: ['before 2011', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018'],
    			datasets: [{{
    				label: {label_1},
    				backgroundColor: color("rgba(38, 185, 154, 0.7)").alpha(0.2).rgbString(),
    				borderColor: "rgba(38, 185, 154, 0.7)",
    				pointBackgroundColor: "rgba(38, 185, 154, 0.7)",
    				data: {samples_data}
    			}}, {{
    				label: {label_2},
    				backgroundColor: color("rgba(3, 88, 106, 0.70)").alpha(0.2).rgbString(),
    				borderColor: "rgba(3, 88, 106, 0.70)",
    				pointBackgroundColor: "rgba(3, 88, 106, 0.70)",
    				data: {fluids_data}
    			}}]
    		}};

    		window.onload = function() {{
    			var chartEl = document.getElementById('chart1');
    			new Chart(chartEl, {{
    				type: 'line',
    				data: lineChartData,
    				options: {{
    					title: {{
    						display: true,
    						text: {main_title}
    					}},
    					tooltips: {{
    						enabled: false,
    						mode: 'index',
    						intersect: false,
    						custom: customTooltips
    					}}
    				}}
    			}});
    		}};
    	</script>
    '''.format(main_title = main_title, label_1 = label_1, label_2 = label_2, samples_data = samples_data, fluids_data = fluids_data)

    return template
