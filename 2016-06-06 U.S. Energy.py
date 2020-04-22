# -*- coding: utf-8 -*-
"""
Created on Mon Jun 06 18:12:24 2016

@author: Amit
"""
from __future__ import print_function
import os
import urllib
import json
from collections import defaultdict
import pandas as pd

# Pulls data from EIA API.
def get_data_from_EIA(APIKey, seriesID):
    url = url = 'http://api.eia.gov/series/?api_key=' + APIKey + '&series_id=' + seriesID
    response = urllib.urlopen(url)    
    data = json.loads(response.read())
    return data

# Prints JSON data to text file.
def write_json_to_txt(jsonObj, filename):
    with open(filename, "w") as outfile:
        json.dump(jsonObj, outfile, indent=4)

# Pull data for all states into a nested dictionary.
def compile_state_energy_data():
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    totalEnergyProdByState = dict(keys = states)
    for state in states:
        dataFromEIA = get_data_from_EIA("DC4B181A26EDF82B41F2A7446102CAB7","SEDS.TEPRB.%s.A" % state)
        totalEnergyProdByState[state] = dataFromEIA
    return totalEnergyProdByState

# Get the range of years with recorded data.
def get_years(totalEnergyProdByState):
    datasetSample = totalEnergyProdByState['AK']['series'][0]['data']
    years = [item[0] for item in datasetSample]
    return years

# Collect data and reorganize by year.
def state_energy_by_year(totalEnergyProdByState):
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    years = get_years(totalEnergyProdByState)
    
    stateDict = dict((states,0) for states in states)
    stateEnergyByYear = dict((year,0) for year in years)
    
    for year in years:
        stateEnergyByYear[year] = stateDict
        
    energyByStateSimple = stateDict
    for state in states:
        energyByStateSimple[state] = dict(totalEnergyProdByState[state]['series'][0]['data'])  
        
    flipped = defaultdict(dict)
    for key, val in energyByStateSimple.items():
        for subkey, subval in val.items():
            flipped[subkey][key] = subval
            
    stateEnergyByYear = dict(flipped)
    
    return stateEnergyByYear

if __name__ == '__main__':
    os.chdir("C:/Users/Amit/OneDrive/1 - Data Projects/2016-06-06 U.S. Energy")
    
# Pull data from EIA API and sort by state and year in nested dictionary.
    totalEnergyProdByState = compile_state_energy_data()
    stateEnergyByYear = state_energy_by_year(totalEnergyProdByState)

# Convert state abbreviations to full names    
    stateIDs = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
        }

# Convert data to pandas dataframe
    stateEnergyByYear = pd.DataFrame.from_dict(stateEnergyByYear)
    stateEnergyByYear.reset_index(level=0, inplace=True)
    stateIDs = pd.DataFrame({"State ID": stateIDs.keys(), "State Name": stateIDs.values()})
    stateEnergyByYear.rename(columns = {'index':'State ID'}, inplace = True)
    stateEnergyByYear = pd.merge(stateEnergyByYear, stateIDs)
    
    year = '2000'
    
    stateEnergyProduction = dict(zip(stateEnergyByYear['State Name'], stateEnergyByYear[year]))
    
    
    
# mapping
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.basemap import Basemap as Basemap
    from matplotlib.colors import rgb2hex
    from matplotlib.patches import Polygon
    
    # Lambert Conformal map of lower 48 states.
    m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
                projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
    # draw state boundaries.
    # data from U.S Census Bureau
    # http://www.census.gov/geo/www/cob/st2000.html
    shp_info = m.readshapefile('Data/state shapefiles 1/st99_d00','states',drawbounds=True)
    # population density by state from
    # http://en.wikipedia.org/wiki/List_of_U.S._states_by_population_density
#    popdensity = {
#    'New Jersey':  438.00,
#    'Rhode Island':   387.35,
#    'Massachusetts':   312.68,
#    'Connecticut':	  271.40,
#    'Maryland':   209.23,
#    'New York':    155.18,
#    'Delaware':    154.87,
#    'Florida':     114.43,
#    'Ohio':	 107.05,
#    'Pennsylvania':	 105.80,
#    'Illinois':    86.27,
#    'California':  83.85,
#    'Hawaii':  72.83,
#    'Virginia':    69.03,
#    'Michigan':    67.55,
#    'Indiana':    65.46,
#    'North Carolina':  63.80,
#    'Georgia':     54.59,
#    'Tennessee':   53.29,
#    'New Hampshire':   53.20,
#    'South Carolina':  51.45,
#    'Louisiana':   39.61,
#    'Kentucky':   39.28,
#    'Wisconsin':  38.13,
#    'Washington':  34.20,
#    'Alabama':     33.84,
#    'Missouri':    31.36,
#    'Texas':   30.75,
#    'West Virginia':   29.00,
#    'Vermont':     25.41,
#    'Minnesota':  23.86,
#    'Mississippi':	 23.42,
#    'Iowa':	 20.22,
#    'Arkansas':    19.82,
#    'Oklahoma':    19.40,
#    'Arizona':     17.43,
#    'Colorado':    16.01,
#    'Maine':  15.95,
#    'Oregon':  13.76,
#    'Kansas':  12.69,
#    'Nebraska':    8.60,
#    'Nevada':  7.03,
#    'Idaho':   6.04,
#    'New Mexico':  5.79,
#    'South Dakota':	 3.84,
#    'North Dakota':	 3.59,
#    'Montana':     2.39,
#    'Wyoming':      1.96,
#    'Alaska':     0.42}
    print(shp_info)
    # choose a color for each state based on population density.
    colors={}
    statenames=[]
    cmap = plt.cm.hot # use 'hot' colormap
    vmin = 0
    vmax = 450
#    vmin = stateEnergyProduction[min(stateEnergyProduction)]; vmax = stateEnergyProduction[max(stateEnergyProduction)] # set range.
    print(m.states_info[0].keys())
    for shapedict in m.states_info:
        statename = shapedict['NAME']
        # skip DC and Puerto Rico.
        if statename not in ['District of Columbia','Puerto Rico']:
            pop = stateEnergyProduction[statename]
            # calling colormap with value between 0 and 1 returns
            # rgba value.  Invert color range (hot colors are high
            # population), take sqrt root to spread out colors more.
#            colors[statename] = cmap(1.-np.sqrt((pop-vmin)/(vmax-vmin)))[:3]
            colors[statename] = cmap(pop/vmax)[:3]
        statenames.append(statename)
    # cycle through state names, color each one.
    ax = plt.gca() # get current axes instance
    for nshape,seg in enumerate(m.states):
        # skip DC and Puerto Rico.
        if statenames[nshape] not in ['District of Columbia','Puerto Rico']:
            color = rgb2hex(colors[statenames[nshape]]) 
            poly = Polygon(seg,facecolor=color,edgecolor=color)
            ax.add_patch(poly)
    # draw meridians and parallels.
    plt.title('Filling State Polygons by Population Density')
    plt.show()
    

## IPython slider code
##    from IPython.html.widgets import *
##
##    def slider(x):
##        print(x)
##    
##    interact(slider, x=10)    
    
    
    
