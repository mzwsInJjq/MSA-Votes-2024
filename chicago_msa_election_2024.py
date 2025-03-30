# Will County, IL
# https://willcounty.gov/County-Offices/Administration/GIS-Division/Data/Vector
# https://results.enr.clarityelections.com/IL/Will/122597/web.345435/#/detail/1

# Grundy County, IL
# https://cms3.revize.com/revize/grundycounty/County%20Clerk/Elections/November%202024%20Notices/FINAL%20Canvass.pdf
# https://maps.grundyco.org/arcgis/rest/services/CountyClerk/PollingPlaces_SPIE_Public/MapServer

import re
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

# 1. Will County, IL
# Define the file path
file_path = r"C:\Users\Chen\Downloads\detail.txt"

# Define the range of lines to read
start_line = 1267
end_line = 1576

# Open the file and read the specific lines
with open(file_path, "r") as file:
    lines = [
        re.split(r'\s{2,}', line.strip()) for i, line in enumerate(file, start=1) if start_line <= i <= end_line
    ]

# Process the lines to extract specific columns
lines = [[line[0], line[5], line[9], line[-1]] for line in lines]
will_precincts = gpd.read_file(r"C:\Users\Chen\Downloads\precincts\precincts_10282024.shp")
will_precincts = will_precincts.to_crs("epsg:4326")

# Filter will_precincts by name
for line in lines:
    precinct_name = line[0]
    votes_dem = int(line[1])
    votes_rep = int(line[2])
    votes_total = int(line[3])
    
    # Find the matching precinct
    matching_precinct = will_precincts[will_precincts['NAME'].str.contains(precinct_name, na=False)]
    if not matching_precinct.empty:
        # Update the votes in the matching precinct
        will_precincts.loc[matching_precinct.index, 'votes_dem'] = votes_dem
        will_precincts.loc[matching_precinct.index, 'votes_rep'] = votes_rep
        will_precincts.loc[matching_precinct.index, 'votes_total'] = votes_total
        will_precincts.loc[matching_precinct.index, 'pct_dem_lead'] = (votes_dem - votes_rep) / votes_total

# 2. Grundy County, IL
file_path = r"C:\Users\Chen\Downloads\grundy_il.txt"
with open(file_path, "r") as file:
    lines = [
        re.split(r'(?<=0\d)\s+', line.strip(), maxsplit=1) for line in file
    ]
    lines = [[line[0], *re.split(r'\s+', line[1])] for line in lines]
    lines = [[line[0], line[1], line[3], line[-4]] for line in lines]

# Remove zeroes from the precinct names
for line in lines:
    if line[0][-2] == '0':
        line[0] = line[0][:-2] + line[0][-1]

# Remove redundant 1 from precinct names
for line in lines:
    if len([l for l in lines if l[0].startswith(line[0].split()[0])]) == 1:
        line[0] = line[0][:-2]

gdf3 = gpd.read_file(r"C:\Users\Chen\Downloads\nhgis0007_shapefile_tl2020_us_votedist_2020\US_votedist_2020.shp")
grundy_precincts = gdf3[(gdf3['STATEFP20'] == '17') & (gdf3['COUNTYFP20'] == '063')]

# Add votes to the precincts
for line in lines:
    precinct_name = line[0]
    votes_dem = int(line[1])
    votes_rep = int(line[2])
    votes_total = int(line[3])
    
    # Find the matching precinct
    matching_precinct = grundy_precincts[grundy_precincts['NAME20'] == precinct_name]
    if not matching_precinct.empty:
        # Update the votes in the matching precinct
        grundy_precincts.loc[matching_precinct.index, 'votes_dem'] = votes_dem
        grundy_precincts.loc[matching_precinct.index, 'votes_rep'] = votes_rep
        grundy_precincts.loc[matching_precinct.index, 'votes_total'] = votes_total
        grundy_precincts.loc[matching_precinct.index, 'pct_dem_lead'] = (votes_dem - votes_rep) / votes_total
grundy_precincts = grundy_precincts.to_crs("epsg:4326")

# 3. Rest of the IL part of Chicago MSA
# Load the data
gdf1 = gpd.read_file(r'C:\Users\Chen\Downloads\IL-precincts-with-results.geojson')

# Filter precincts in gdf1 by GEOID
gdf1 = gdf1[gdf1['GEOID'].str.startswith('17031') | gdf1['GEOID'].str.startswith('17097') | gdf1['GEOID'].str.startswith('17111') | gdf1['GEOID'].str.startswith('17043') | gdf1['GEOID'].str.startswith('17089') | gdf1['GEOID'].str.startswith('17037') | gdf1['GEOID'].str.startswith('17093')]

# 4. IN part of Chicago MSA
gdf2 = gpd.read_file(r"C:\Users\Chen\Downloads\IN24\IN24.shp")
gdf2['geometry'] = gdf2['geometry'].force_2d()
gdf2 = gdf2.to_crs("epsg:4326")

# Filter precincts in gdf2 by JoinField
gdf2 = gdf2[gdf2['JoinField'].str.startswith('(073)') | gdf2['JoinField'].str.startswith('(089)') | gdf2['JoinField'].str.startswith('(111)') | gdf2['JoinField'].str.startswith('(127)')]

# Calculate the Democratic margin in each precinct for gdf2
gdf2['pct_dem_lead'] = (gdf2['PresDem'] - gdf2['PresRep']) / gdf2['PresTot']

# WI part of Chicago MSA
gdf3 = gpd.read_file(r"C:\Users\Chen\Downloads\WI-precincts-with-results.geojson")

# Filter precincts in gdf3 by GEOID
gdf3 = gdf3[gdf3['GEOID'].str.startswith('55059')]
# Concatenate the GeoDataFrames
gdf = gpd.GeoDataFrame(pd.concat([will_precincts, grundy_precincts, gdf1, gdf2, gdf3], ignore_index=True))

# Define the bbox for Chicago-Naperville-Elgin, IL-IN-WI MSA
bbox = (-88.9420709, 40.7364954, -86.9293210, 42.6697570)

# Filter the GeoDataFrame to include only precincts within the bbox
gdf = gdf.cx[bbox[0]:bbox[2], bbox[1]:bbox[3]]

# Create a color map
norm = TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)
cmap = plt.get_cmap('bwr_r')  # '_r' reverses the color map

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(15, 15))
gdf.plot(column='pct_dem_lead', cmap=cmap, linewidth=0, ax=ax, norm=norm)

# Remove axis
ax.axis('off')

# Set the axis limits to match the bounding box
ax.set_xlim(bbox[0], bbox[2])
ax.set_ylim(bbox[1], bbox[3])

plt.savefig('chicago_msa_election_2024.pdf', format='pdf', bbox_inches='tight')

# Show the plot
plt.show()

sum_votes_dem = gdf['votes_dem'].sum()
sum_votes_rep = gdf['votes_rep'].sum()
sum_votes_third_party = gdf['votes_total'].sum() - sum_votes_dem - sum_votes_rep
sum_votes_total = gdf['votes_total'].sum()
print(f"Democratic % for Chicago MSA: {100 * sum_votes_dem/sum_votes_total:.2f}%")
print(f"Republican % for Chicago MSA: {100 * sum_votes_rep/sum_votes_total:.2f}%")
print(f"Third Party % for Chicago MSA: {100 * sum_votes_third_party/sum_votes_total:.2f}%")