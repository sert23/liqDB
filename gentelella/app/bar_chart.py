#!/usr/bin/env python3

from collections import Counter

def year_bar_chart(data, main_title = 'Number of studies available', title_1 = 'Studies uploaded to SRA per year'):
	labels = ['2018 or later', '2016-2017', '2014-2015', '2012-2013', '2011 or before', 'total']
	labels = ['<p style="font-size:100%;">' + label + '</p>' for label in labels]
	time_slots_count = {
		labels[0] : 0,
		labels[1] : 0,
		labels[2] : 0,
		labels[3] : 0,
		labels[4] : 0,
		labels[5] : 0
	}
	for year in data:
		if isinstance(year, str):
			assert year.isnumeric()
		year = int(year)
		if year >= 2018:
			time_slots_count[labels[0]] += 1
		elif year in [2016, 2017]:
			time_slots_count[labels[1]] += 1
		elif year in [2014, 2015]:
			time_slots_count[labels[2]] += 1
		elif year in [2012, 2013]:
			time_slots_count[labels[3]] += 1
		elif year <= 2011:
			time_slots_count[labels[4]] += 1
		time_slots_count[labels[5]] += 1
	counts = [time_slots_count[label] for label in labels]
	percentages = list(map(lambda c: round(100*float(c)/counts[-1],2), counts))
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
					<div class="progress-bar bg-green" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: {p_second}%;">
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
					<div class="progress-bar bg-green" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: {p_third}%;">
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
					<div class="progress-bar bg-green" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: {p_fourth}%;">
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
					<div class="progress-bar bg-green" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: {p_fifth}%;">
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
	'''.format(main_title = main_title, title_1 = title_1, first = labels[0], second = labels[1], third = labels[2], fourth = labels[3], fifth = labels[4],
	           p_first = percentages[0], p_second = percentages[1], p_third = percentages[2], p_fourth = percentages[3], p_fifth = percentages[4],
	           c_first = counts[0], c_second = counts[1], c_third = counts[2], c_fourth = counts[3], c_fifth = counts[4])
	return template

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
					<div class="progress-bar bg-green" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: {p_second}%;">
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
					<div class="progress-bar bg-green" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: {p_third}%;">
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
					<div class="progress-bar bg-green" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: {p_fourth}%;">
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
					<div class="progress-bar bg-green" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: {p_fifth}%;">
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
	#data = ['A'] * 10 + ['B'] * 3 + ['C'] + ['D'] + ['E'] * 15 + ['F'] * 20 + ['G'] + ['H'] * 3 + ['I'] * 3 + ['J'] + ['K']
	#my_bar = bar_chart(data)
	#open('example.html', 'wt').write(my_bar)
	data = [2019, 2019, 2018, 2018, 2017, 2016, 2016, 2015, 2014, 2013, 2012, 2012, 2012, 2011, 2010, 2019]
	my_bar = year_bar_chart(data)
	open('example.html', 'wt').write(my_bar)
