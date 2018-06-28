#!/usr/bin/env python3

from collections import Counter

def pie_chart(data, main_title = 'Fluids Abundance', title_1 = 'Top 5', title_2 = 'Fluid', title_3 = 'N. of Samples', fifth = 'Others'):
	total = float(len(data))
	counter = Counter(data)
	top_4 = counter.most_common(4)
	first, second, third, fourth = [key for key, value in top_4]
	c_first, c_second, c_third, c_fourth = [value for key, value in top_4]
	p_first, p_second, p_third, p_fourth = list(map(lambda value: round(100*value/total, 2), [value for key, value in top_4]))
	fifth = fifth
	c_fifth = len(data) - c_first - c_second - c_third - c_fourth
	p_fifth = round(100 - p_first - p_second - p_third - p_fourth, 2)
	template = '''
	<script>
		function init_chart_doughnut() {{
			if (typeof(Chart) === 'undefined') {{ return }};
			console.log('init_chart_doughnut');
			if ($('.canvasDoughnut').length) {{
				var chart_doughnut_settings = {{
					type: 'doughnut',
					tooltipFillColor: "rgba(51, 51, 51, 0.55)",
					data: {{
						labels: ["{first}", "{second}", "{third}", "{fourth}", "{fifth}"],
						datasets: [{{
							data: ["{p_first}", "{p_second}", "{p_third}", "{p_fourth}", "{p_fifth}"],
							backgroundColor: ["#3498DB", "#26B99A", "#9B59B6", "#E74C3C", "#BDC3C7"],
							hoverBackgroundColor: ["#49A9EA", "#36CAAB", "#B370CF", "#E95E4F", "#CFD4D8"]
						}}]
					}},
					options: {{
						legend: false,
						responsive: false
					}}
				}}
				$('.canvasDoughnut').each(function() {{
					var chart_element = $(this);
					var chart_doughnut = new Chart(chart_element, chart_doughnut_settings);
				}});
			}}
		}}
	</script>
	<div class="x_panel tile fixed_height_320 overflow_hidden">
	<div class="x_title">
		<h2>{main_title}</h2>
		<div class="clearfix"></div>
	</div>
	<div class="x_content">
		<table class="" style="width:100%"><tbody>
			<tr>
				<th style="width:37%;"><p>{title_1}</p></th>
				<th>
					<div class="col-lg-7 col-md-7 col-sm-7 col-xs-7"><p class="">{title_2}</p></div>
					<div class="col-lg-5 col-md-5 col-sm-5 col-xs-5"><p class="">{title_3}</p></div>
				</th>
			</tr>
			<tr>
				<td><iframe class="chartjs-hidden-iframe" style="width: 100%; display: block; border: 0px; height: 0px; margin: 0px; position: absolute; left: 0px; right: 0px; top: 0px; bottom: 0px;"></iframe><canvas class="canvasDoughnut" height="140" width="140" style="margin: 15px 10px 10px 0px; width: 140px; height: 140px;"></canvas></td>
				<td><table class="tile_info"><tbody>
					<tr><td><p><i class="fa fa-square blue"></i>{first}</p></td><td>{c_first}</td></tr>
					<tr><td><p><i class="fa fa-square green"></i>{second}</p></td><td>{c_second}</td></tr>
					<tr><td><p><i class="fa fa-square purple"></i>{third}</p></td><td>{c_third}</td></tr>
					<tr><td><p><i class="fa fa-square red"></i>{fourth}</p></td><td>{c_fourth}</td></tr>
					<tr><td><p><i class="fa fa-square aero"></i>{fifth}</p></td><td>{c_fifth}</td></tr>
				</tbody></table></td>
			</tr>
		</tbody></table>
	</div>
	</div>
	'''.format(main_title = main_title, title_1 = title_1, title_2 = title_2, title_3 = title_3, first = first, second = second, third = third, fourth = fourth, fifth = fifth, p_first = p_first, p_second = p_second, p_third = p_third, p_fourth = p_fourth, p_fifth = p_fifth, c_first = c_first, c_second = c_second, c_third = c_third, c_fourth = c_fourth, c_fifth = c_fifth)
	return template

if __name__ == '__main__':
	data = ['A'] * 10 + ['B'] * 3 + ['C'] + ['D'] + ['E'] * 15 + ['F'] * 20 + ['G'] + ['H'] * 3 + ['I'] * 3 + ['J'] + ['K']
	my_pie = pie_chart(data)
	open('example.html', 'wt').write(my_pie)

