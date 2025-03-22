# 2023 TIGER/Line +
# https://data2.nhgis.org/main

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

# Load the data
gdf = gpd.read_file(r"C:\Users\Chen\Downloads\WA-precincts-with-results.geojson")
df = gpd.read_file(r"C:\Users\Chen\Downloads\nhgis0001_shapefile_tl2023_us_state_2023\US_state_2023.shp")
df = df[df['STATEFP'] == '53']
df = df.to_crs("epsg:4326")

# Filter counties by gdf['GEOID']: startswith (King) 53033, (Pierce) 53053, (Snohomish) 53061
gdf = gdf[gdf['GEOID'].str.startswith('53033') | gdf['GEOID'].str.startswith('53053') | gdf['GEOID'].str.startswith('53061')]
gdf = gpd.overlay(gdf, df, how='intersection', keep_geom_type=False)

# Define the bbox for Seattle-Tacoma-Bellevue, WA Metropolitan Statistical Area
bbox = (-122.8529952, 46.7287986, -120.9067414, 48.2992336)

# Filter the GeoDataFrame to include only precincts within the bbox
gdf = gdf.cx[bbox[0]:bbox[2], bbox[1]:bbox[3]]

# Create a color map
norm = TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)
cmap = plt.get_cmap('bwr_r')  # '_r' reverses the color map

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(15, 15))
gdf.plot(column='pct_dem_lead', cmap=cmap, linewidth=0, ax=ax, norm=norm)

# Set the axis limits to match the bounding box
ax.set_xlim(bbox[0], bbox[2])
ax.set_ylim(bbox[1], bbox[3])

# Remove axis
ax.axis('off')

plt.savefig('seattle_msa_election_2024_coastline.pdf', format='pdf', bbox_inches='tight')

# Show the plot
plt.show()

sum_votes_dem = gdf['votes_dem'].sum()
sum_votes_rep = gdf['votes_rep'].sum()
sum_votes_third_party = gdf['votes_total'].sum() - sum_votes_dem - sum_votes_rep
sum_votes_total = gdf['votes_total'].sum()
print(f"Democratic % for Seattle MSA: {100 * sum_votes_dem/sum_votes_total:.2f}%")
print(f"Republican % for Seattle MSA: {100 * sum_votes_rep/sum_votes_total:.2f}%")
print(f"Third Party % for Seattle MSA: {100 * sum_votes_third_party/sum_votes_total:.2f}%")