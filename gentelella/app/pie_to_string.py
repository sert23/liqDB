#!/usr/bin/env python3

from collections import Counter
from plotly.offline import download_plotlyjs, plot
import plotly.graph_objs as go

def pie_chart(data, width = 300, height = 300, font_size = 30):
	counter = sorted(Counter(data).items())
	labels, values = [], []
	for item in counter: labels.append(item[0]), values.append(item[1])
	fig = {
		"data": [{
			"labels" : labels,
			"values" : values,
			"hoverinfo" : "label+percent",
			"type" : "pie",
			"textinfo" : "none",
			"textposition" : "inside"
		}],
		"layout" : {
			"showlegend" : True,
			"font"  : {
				"family" : 'Courier New, monospace',
				"size" : font_size,
				"color" :'#000000'
			},
			"autosize" : False,
			"width" : width,
			"height" : height,
			"margin" : {
				"l" : 0,
				"r" : 0,
				"b" : 0,
				"t" : 0,
				"pad" : 0
			}
		}
	}
	pie = plot(fig, show_link = False, auto_open = False, output_type = 'div')
	return pie

if __name__ == '__main__':
	string = pie_chart(['A', 'A', 'A', 'B', 'B', 'C', 'D'])
	#print(string)
	open('example.html', 'wt').write(string)
