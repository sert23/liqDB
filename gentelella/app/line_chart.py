#!/usr/bin/env python3

from collections import OrderedDict

def line_chart(SampleModel):
    samples = SampleModel.objects.all()
    samples_count = OrderedDict({
        
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
        year = sample.Date.year
        fluid = sample.Fluid
        if year < 2011:
            pass
        elif year > 2018:
            samples_count[2018] += 1
            fluids[2018].add(fluid)
        else:
            samples_count[year] += 1
            fluids[year].add(fluid)

    fluids = {year : len(fluids[year]) for year in fluids}

    
    samples_count[2012] += samples_count[2011]
    samples_count[2013] += samples_count[2012]
    samples_count[2014] += samples_count[2013]
    samples_count[2015] += samples_count[2014]
    samples_count[2016] += samples_count[2015]
    samples_count[2017] += samples_count[2016]
    samples_count[2018] += samples_count[2017]

    
    fluids[2012] += fluids[2011]
    fluids[2013] += fluids[2012]
    fluids[2014] += fluids[2013]
    fluids[2015] += fluids[2014]
    fluids[2016] += fluids[2015]
    fluids[2017] += fluids[2016]
    fluids[2018] += fluids[2017]

    samples_data = ["[gd({year}, 1, 1), {count}]".format(year = year, count = samples_count[year]) for year in samples_count]
    samples_data = '[' + ','.join(samples_data) + ']'
    fluids_data = ["[gd({year}, 1, 1), {count}]".format(year = year, count = fluids[year]) for year in fluids]
    fluids_data = '[' + ','.join(fluids_data) + ']'

    return samples_data, fluids_data
