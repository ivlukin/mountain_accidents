from datetime import datetime
from dateutil import parser
import codecs

from rangers_analyzer.RangersAccident import RangersAccident

def get_date_from_raw_line(line: str):
    index_of_dot = line.find(".")
    if index_of_dot < 0:
        index_of_dot = float('inf')
    index_of_comma = line.find(",")
    if index_of_comma < 0:
        index_of_comma = float('inf')
    date_str = line[:min(index_of_dot, index_of_comma)]
    return parser.parse(date_str), min(index_of_dot, index_of_comma)


with open('rangers.txt', encoding='UTF-8') as file:
    lines = [line.rstrip() for line in file]
lines = list(filter(lambda x: len(x) > 0, lines))

lines_by_county = dict()
current_county = ""
for line in lines:
    if "county" in line.lower() and line not in lines_by_county:
        lines_by_county[line] = []
        current_county = line

    elif "county" in line.lower() and line in lines_by_county:
        current_county = line
    else:
        lines_by_county[current_county].append(line)

accidents_by_county = dict()
for county in lines_by_county:
    lines = lines_by_county[county]
    accidents_by_county[county] = []
    for i in range(1, len(lines), 2):
        line_with_date = lines[i]
        line_with_place = lines[i - 1]
        accident_date, end_index = get_date_from_raw_line(line_with_date)
        line_with_accident = line_with_date[end_index + 1:].strip()
        accidents_by_county[county].append(RangersAccident(county, line_with_place, accident_date, line_with_accident))

f = codecs.open('rangers_report.csv', 'w', 'utf-8')

for county in accidents_by_county:
    accidents = accidents_by_county[county]
    for acc in accidents:
        f.write(str(acc) + '\n')

f.close()
