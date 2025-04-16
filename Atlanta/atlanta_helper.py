# https://www.metroatlantachamber.com/wp-content/uploads/2022/11/atlmsa_map_8.9.21-1.pdf

import re
county_name = 'Barrow Clayton Douglas Haralson Meriwether Pike Bartow Cobb Fayette Heard Morgan Rockdale Butts Coweta Forsyth Henry Newton Spalding Carroll Dawson Fulton Jasper Paulding Walton Cherokee DeKalb Gwinnett Lamar Pickens'.split()
# Search for lines that matches each county
for name in county_name:
    with open('fips.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if re.search(rf'^13.*{name}.*', line):
                print(line.strip())
