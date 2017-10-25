# QueryAQM
Quick Python script to gather data on Air Quality Monitoring sites from the EPA.

<pre>
usage: QueryAQM.py [-h] [-type TYPE] [-state STATE] [-allStates] [-d]

Query air quality site data from the EPA. You can query one or more site types
for one or more states. Pass -d to see listing of site types.

Arguments:
  -h, --help    Show this help message and exit
  -type TYPE    Station type ID to query, see -d
  -state STATE  State to query, can be full name or abreviation
  -allStates    Display data for all states
  -d            Display mapping of site type ID to type name and exit
</pre>
