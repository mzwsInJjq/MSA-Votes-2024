import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

# Load the data
gdf = gpd.read_file(r"C:\Users\Chen\Downloads\MN-precincts-with-results.geojson")

# Filter precincts by gdf['GEOID']
gdf = gdf[gdf['GEOID'].str.startswith('27003') | gdf['GEOID'].str.startswith('27019') | gdf['GEOID'].str.startswith('27037') | gdf['GEOID'].str.startswith('27053') | gdf['GEOID'].str.startswith('27059') | gdf['GEOID'].str.startswith('27123') | gdf['GEOID'].str.startswith('27139') | gdf['GEOID'].str.startswith('27163')]

# Define the bbox for Twin Cities
bbox = (-94.0123331, 44.4711806, -92.7396452, 45.4145196)

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

plt.savefig('twin_cities_city_election_2024.pdf', format='pdf', bbox_inches='tight')

# Show the plot
plt.show()

sum_votes_dem = gdf['votes_dem'].sum()
sum_votes_rep = gdf['votes_rep'].sum()
sum_votes_third_party = gdf['votes_total'].sum() - sum_votes_dem - sum_votes_rep
sum_votes_total = gdf['votes_total'].sum()
print(f"Democratic % for Twin Cities: {100 * sum_votes_dem/sum_votes_total:.2f}%")
print(f"Republican % for Twin Cities: {100 * sum_votes_rep/sum_votes_total:.2f}%")
print(f"Third Party % for Twin Cities: {100 * sum_votes_third_party/sum_votes_total:.2f}%")
