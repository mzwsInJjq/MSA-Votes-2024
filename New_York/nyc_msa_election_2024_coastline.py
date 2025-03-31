# 2023 TIGER/Line +
# https://data2.nhgis.org/main

# https://www.pikepa.org/Document%20Center/Government/Election%20Office/2024/Nov.%205,%202024%20Results%20Per%20Precinct.pdf

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

# Load the data
gdf1 = gpd.read_file(r'C:\Users\Chen\Downloads\NY-precincts-with-results.geojson')
gdf2 = gpd.read_file(r'C:\Users\Chen\Downloads\NJ24\2024 NJ Precincts.shp')
gdf3 = gpd.read_file(r'C:\Users\Chen\Downloads\NJ-precincts-with-results.geojson')
gdf4 = gpd.read_file(r"C:\Users\Chen\Downloads\nhgis0007_shapefile_tl2020_us_votedist_2020\US_votedist_2020.shp")

df = gpd.read_file(r"C:\Users\Chen\Downloads\nhgis0001_shapefile_tl2023_us_state_2023\US_state_2023.shp")
df = df[(df['STATEFP'] == '36') | (df['STATEFP'] == '34') | (df['STATEFP'] == '42')]
df = df.to_crs("epsg:4326")

# Filter precincts in gdf1 by gdf['GEOID']
gdf1 = gdf1[gdf1['GEOID'].str.startswith('36047') | gdf1['GEOID'].str.startswith('36081') | gdf1['GEOID'].str.startswith('36061') | gdf1['GEOID'].str.startswith('36005') | gdf1['GEOID'].str.startswith('36119') | gdf1['GEOID'].str.startswith('36085') | gdf1['GEOID'].str.startswith('36087') | gdf1['GEOID'].str.startswith('36079') | gdf1['GEOID'].str.startswith('36103') | gdf1['GEOID'].str.startswith('36059')]

# Filter precincts in gdf2 by gdf['CouName']
gdf2 = gdf2[gdf2['CouName'].str.startswith('Hunterdon') | gdf2['CouName'].str.startswith('Sussex')]

# Filter precincts in gdf3 by gdf['GEOID']
gdf3 = gdf3[gdf3['GEOID'].str.startswith('34003') | gdf3['GEOID'].str.startswith('34017') | gdf3['GEOID'].str.startswith('34023') | gdf3['GEOID'].str.startswith('34031') | gdf3['GEOID'].str.startswith('34029') | gdf3['GEOID'].str.startswith('34025') | gdf3['GEOID'].str.startswith('34035') | gdf3['GEOID'].str.startswith('34013') | gdf3['GEOID'].str.startswith('34039') | gdf3['GEOID'].str.startswith('34027')]

# Calculate the Democratic margin in each precinct for gdf2
gdf2['pct_dem_lead'] = (gdf2['Harris'] - gdf2['Trump']) / gdf2['Total']

# Filter precincts in gdf4
gdf4 = gdf4[(gdf4['STATEFP20'] == '42') & (gdf4['COUNTYFP20'] == '103')]
gdf4 = gdf4.to_crs("epsg:4326")

gdf4.loc[gdf4['NAME20'].str.startswith('MATAMORAS DISTRICT '), 'NAME20'] = 'MATAMORAS'

csv_file_path = r"C:\Users\Chen\Downloads\pike_pa.csv"
# Read the CSV file
df2 = pd.read_csv(csv_file_path, header=None)

# Iterate through the rows of the DataFrame
for index, row in df2.iterrows():
    precinct_name = row[0].strip()  # First column
    votes_dem = int(row[1])  # Second column
    votes_rep = int(row[2])  # Third column
    votes_total = int(row[1]) + int(row[2]) + int(row[3]) + int(row[4]) + int(row[5])  # Sum of second to sixth columns

    # Find the matching precinct in gdf4
    matching_precinct = gdf4[gdf4['NAME20'] == precinct_name]
    if not matching_precinct.empty:
        # Update the votes in the matching precinct
        gdf4.loc[matching_precinct.index, 'votes_dem'] = votes_dem
        gdf4.loc[matching_precinct.index, 'votes_rep'] = votes_rep
        gdf4.loc[matching_precinct.index, 'votes_total'] = votes_total
        gdf4.loc[matching_precinct.index, 'pct_dem_lead'] = (votes_dem - votes_rep) / votes_total

# Concatenate the GeoDataFrames
gdf = gpd.GeoDataFrame(pd.concat([gdf1, gdf2, gdf3, gdf4], ignore_index=True))
gdf = gpd.overlay(gdf, df, how='intersection', keep_geom_type=False)

# Define the bbox for New York-Newark-Jersey City, NY-NJ-PA MSA
bbox = (-75.3589959, 39.4751962, -71.790972, 41.5270230)

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

plt.savefig('nyc_msa_election_2024_coastline.pdf', format='pdf', bbox_inches='tight')

# Show the plot
plt.show()

sum_votes_dem = gdf['votes_dem'].sum()
sum_votes_rep = gdf['votes_rep'].sum()
sum_votes_third_party = gdf['votes_total'].sum() - sum_votes_dem - sum_votes_rep
sum_votes_total = gdf['votes_total'].sum()
print(f"Democratic % for NYC MSA: {100 * sum_votes_dem/sum_votes_total:.2f}%")
print(f"Republican % for NYC MSA: {100 * sum_votes_rep/sum_votes_total:.2f}%")
print(f"Third Party % for NYC MSA: {100 * sum_votes_third_party/sum_votes_total:.2f}%")