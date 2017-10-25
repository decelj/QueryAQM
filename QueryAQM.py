#! /usr/bin/env python
import json
import urllib2
import argparse
import sys

GISURL = 'https://gispub.epa.gov/arcgis/rest/services/OAR_OAQPS/AQSmonitor_sites/MapServer/{type}/query?where=State%3D%27{state}%27&text=&objectIds=&time=&geometry=&geometryType=esriGeometryPoint&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=AQS_Site_ID&returnGeometry=false&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentsOnly=false&datumTransformation=&parameterValues=&rangeValues=&f=pjson'

STATION_TYPES = {
'CO - Active':0,
'CO - Inactive':1,
'Lead - Active':2,
'Lead - Inactive':3,
'Lead - TSP(LC) - Active':4,
'Lead - TSP(LC) - Inactive':5,
'Lead - PM10(LC) - Active':6,
'Lead - PM10(LC) - Inactive':7,
'NO2 - Active':8,
'NO2 - Inactive':9,
'Ozone - Active':10,
'Ozone - Inactive':11,
'PM10 - Active':12,
'PM10 - Inactive':13,
'PM2.5 - Active':14,
'PM2.5 - Inactive':15,
'SO2 - Active':16,
'SO2 - Inactive':17,
'PM2.5 Chemical Speciation Network - Active':18,
'PM2.5 Chemical Speciation Network - Inactive':19,
'IMPROVE (Interagency Monitoring of Protected Visual Environments) - Active':20,
'IMPROVE (Interagency Monitoring of Protected Visual Environments) - Inactive':21,
'NATTS (National Air Toxics Trends Stations) - Active':22,
'NATTS (National Air Toxics Trends Stations) - Inactive':23,
'NCORE (Multipollutant Monitoring Network) - Active':24,
'NCORE (Multipollutant Monitoring Network) - Inactive':25,
}

TYPE_ID_TO_STR = dict()
for k, v in STATION_TYPES.iteritems():
    TYPE_ID_TO_STR[v] = k

STATES = {
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
'''
Query air quality site data from the EPA.
You can query one or more site types for one or more states. Pass -d to see listing of site types.
''')
    parser.add_argument('-type', type=int, action='append', help='Station type ID to query, see -d')
    parser.add_argument('-state', type=str, action='append', help='State to query, can be full name or abreviation')
    parser.add_argument('-allStates', action='store_true', help="Display data for all states");
    parser.add_argument('-d', action='store_true', help='Display mapping of site type ID to type name and exit');

    args = parser.parse_args(sys.argv[1:])
    if args.d:
        for k in sorted(TYPE_ID_TO_STR):
            print("Type {1}: {0}".format(TYPE_ID_TO_STR[k], k))
        exit(0)

    if args.state is None and args.allStates is False:
        parser.error("Must provide one or more states or -allStates")

    if args.type is None:
        parser.error("Must provide one or more station types")

    if args.state is None:
        states = STATES.values()
    else:
        states = list()
        for state in args.state:
            try:
                states.append(STATES[state.upper()])
            except KeyError:
                capState = ' '.join(x.capitalize() for x in state.split())
                if capState not in STATES.values():
                    parser.error("'{0}' does not appear to be a state!".format(state))

                states.append(capState)

    total = 0
    for siteType in args.type:
        print(TYPE_ID_TO_STR[siteType])
        for state in states:
            result = urllib2.urlopen(GISURL.format(state=state.replace(' ', '+'), type=siteType))
            if result.code != 200:
                raise RuntimeError(
                    "Failed to query data for station type {0}, state {1}: {2}".format(siteType, state, result.msg))

            data = json.loads(result.read())
            value = len(data['features']);
            total += value;
            print("  {0}: {1}".format(state, value))

    print("Total: {0}".format(total))

