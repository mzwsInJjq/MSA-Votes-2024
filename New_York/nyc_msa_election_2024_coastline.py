# 2023 TIGER/Line +
# https://data2.nhgis.org/main

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

# Load the data
gdf1 = gpd.read_file(r'C:\Users\Chen\Downloads\NY-precincts-with-results.geojson')
gdf2 = gpd.read_file(r'C:\Users\Chen\Downloads\NJ24\2024 NJ Precincts.shp')
gdf3 = gpd.read_file(r'C:\Users\Chen\Downloads\NJ-precincts-with-results.geojson')

df = gpd.read_file(r"C:\Users\Chen\Downloads\nhgis0001_shapefile_tl2023_us_state_2023\US_state_2023.shp")
df = df[(df['STATEFP'] == '36') | (df['STATEFP'] == '34')]
df = df.to_crs("epsg:4326")

# Filter precincts in gdf1 by gdf['GEOID']
gdf1 = gdf1[gdf1['GEOID'].str.startswith('36047') | gdf1['GEOID'].str.startswith('36081') | gdf1['GEOID'].str.startswith('36061') | gdf1['GEOID'].str.startswith('36005') | gdf1['GEOID'].str.startswith('36119') | gdf1['GEOID'].str.startswith('36085') | gdf1['GEOID'].str.startswith('36087') | gdf1['GEOID'].str.startswith('36079') | gdf1['GEOID'].str.startswith('36103') | gdf1['GEOID'].str.startswith('36059')]

# Filter precincts in gdf2 by gdf['CouName']
gdf2 = gdf2[gdf2['CouName'].str.startswith('Hunterdon')]

# Filter precincts in gdf3 by gdf['GEOID']
gdf3 = gdf3[gdf3['GEOID'].str.startswith('34003') | gdf3['GEOID'].str.startswith('34017') | gdf3['GEOID'].str.startswith('34023') | gdf3['GEOID'].str.startswith('34031') | gdf3['GEOID'].str.startswith('34029') | gdf3['GEOID'].str.startswith('34025') | gdf3['GEOID'].str.startswith('34035') | gdf3['GEOID'].str.startswith('34013') | gdf3['GEOID'].str.startswith('34039') | gdf3['GEOID'].str.startswith('34027') | gdf3['GEOID'].str.startswith('34037')]

# Calculate the Democratic margin in each precinct for gdf2
gdf2['pct_dem_lead'] = (gdf2['Harris'] - gdf2['Trump']) / gdf2['Total']

# Concatenate the GeoDataFrames
gdf = gpd.GeoDataFrame(pd.concat([gdf1, gdf2, gdf3], ignore_index=True))
gdf = gpd.overlay(gdf, df, how='intersection', keep_geom_type=False)

# Define the bbox for New York-Newark-Jersey City, NY-NJ MSA
bbox = (-75.1955447, 39.4751962, -71.790972, 41.5270230)

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