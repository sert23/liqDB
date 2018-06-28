#!/usr/bin/env python3

from collections import Counter

def bar_chart(data, main_title = 'Fluids Abundance', title_1 = 'Top 5', fifth = 'Others'):
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
	<div class="x_panel tile fixed_height_320 overflow_hidden">
	<div class="x_title">
		<h2>{main_title}</h2>
		<div class="clearfix"></div>
	</div>
	<div class="x_content">
		<h4>{title_1}</h4>
		<div class="widget_summary">
			<div class="w_left w_25">
				<span>{first}</span>
			</div>
			<div class="w_center w_55">
				<div class="progress">
					<div class="progress-bar bg-green" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: {p_first}%;">
						<span class="sr-only">{p_first}%</span>
					</div>
				</div>
			</div>
			<div class="w_right w_20">
				<span>{c_first}</span>
			</div>
			<div class="clearfix"></div>
		</div>
		<div class="widget_summary">
			<div class="w_left w_25">
				<span>{second}</span>
			</div>
			<div class="w_center w_55">
				<div class="progress">
					<div class="progress-bar bg-blue" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: {p_second}%;">
						<span class="sr-only">{p_second}%</span>
					</div>
				</div>
			</div>
			<div class="w_right w_20">
				<span>{c_second}</span>
			</div>
			<div class="clearfix"></div>
		</div>
		<div class="widget_summary">
			<div class="w_left w_25">
				<span>{third}</span>
			</div>
			<div class="w_center w_55">
				<div class="progress">
					<div class="progress-bar bg-purple" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: {p_third}%;">
						<span class="sr-only">{p_third}%</span>
					</div>
				</div>
			</div>
			<div class="w_right w_20">
				<span>{c_third}</span>
			</div>
			<div class="clearfix"></div>
		</div>
		<div class="widget_summary">
			<div class="w_left w_25">
				<span>{fourth}</span>
			</div>
			<div class="w_center w_55">
				<div class="progress">
					<div class="progress-bar bg-red" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: {p_fourth}%;">
						<span class="sr-only">{p_fourth}%</span>
					</div>
				</div>
			</div>
			<div class="w_right w_20">
				<span>{c_fourth}</span>
			</div>
			<div class="clearfix"></div>
		</div>
		<div class="widget_summary">
			<div class="w_left w_25">
				<span>{fifth}</span>
			</div>
			<div class="w_center w_55">
				<div class="progress">
					<div class="progress-bar bg-aero" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: {p_fifth}%;">
						<span class="sr-only">{p_fifth}%</span>
					</div>
				</div>
			</div>
			<div class="w_right w_20">
				<span>{c_fifth}</span>
			</div>
			<div class="clearfix"></div>
		</div>
	</div>
	</div>
	'''.format(main_title = main_title, title_1 = title_1, first = first, second = second, third = third, fourth = fourth, fifth = fifth, p_first = p_first, p_second = p_second, p_third = p_third, p_fourth = p_fourth, p_fifth = p_fifth, c_first = c_first, c_second = c_second, c_third = c_third, c_fourth = c_fourth, c_fifth = c_fifth)
	return template

if __name__ == '__main__':
	data = ['A'] * 10 + ['B'] * 3 + ['C'] + ['D'] + ['E'] * 15 + ['F'] * 20 + ['G'] + ['H'] * 3 + ['I'] * 3 + ['J'] + ['K']
	my_bar = bar_chart(data)
	open('example.html', 'wt').write(my_bar)

