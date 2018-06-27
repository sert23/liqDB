import numpy
import math
import itertools
#import test

from plotly.offline import plot
import plotly.graph_objs as go
import pandas
import os.path
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import numpy as np

def makeGenomePlot(input_file, output_file):
    first_table = pandas.read_table(input_file, sep='\t')
    input_table = first_table.head(10)
    data = []
    for index, row in input_table.iterrows():
        line = numpy.ndarray.flatten(row.values)
        trace = go.Box(
            y=line[1:-1],
            name=line[0]
        )
        data.append(trace)
    layout = go.Layout(
        autosize=True,

        margin=go.Margin(
            l=50,
            r=50,
            b=150,
            t=100,
            pad=4
        ),
        title="RNA types distribution",
        xaxis=dict(
            # title='Nulceotide added',
            tick0=0,
            dtick=1,
        ),
        yaxis=dict(
            title='Percentage of reads (%)')
    )
    fig = go.Figure(data=data, layout=layout)
    div_obj = plot(fig, show_link=False, auto_open=False, output_type = 'div')
    return div_obj

def makeSpeciesPlot():
    print(" ")


makeGenomePlot("C:/Users/Ernesto/PycharmProjects/liqDB/gentelella/data_folder/studies/SRP062974/RCperc_genome.txt","")