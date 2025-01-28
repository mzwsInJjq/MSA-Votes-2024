import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

# Load the data
gdf1 = gpd.read_file(r'C:\Users\Chen\Downloads\NY-precincts-with-results.geojson')
gdf2 = gpd.read_file(r'C:\Users\Chen\Downloads\NJ-precincts-with-results.geojson')
gdf3 = gpd.read_file(r'C:\Users\Chen\Downloads\PA-precincts-with-results.geojson')
gdf4 = gpd.read_file(r'C:\Users\Chen\Downloads\CT-precincts-with-results.geojson')
gdf5 = gpd.read_file(r'C:\Users\Chen\Downloads\RI-precincts-with-results.geojson')
gdf6 = gpd.read_file(r'C:\Users\Chen\Downloads\MA-precincts-with-results.geojson')

# Concatenate the GeoDataFrames
gdf = gpd.GeoDataFrame(pd.concat([gdf1, gdf2, gdf3, gdf4, gdf5, gdf6], ignore_index=True))

# Calculate pct_dem_lead
gdf['pct_dem_lead'] = (gdf['votes_dem'] - gdf['votes_rep']) / gdf['votes_total']

# Define the bbox for New York-Newark-Jersey City, NY-NJ-PA Metropolitan Statistical Area
bbox = (-75.3589959, 39.4751962, -71.7909720, 42.1752680)

# Filter the GeoDataFrame to include only precincts within the bbox
gdf = gdf.cx[bbox[0]:bbox[2], bbox[1]:bbox[3]]

# Create a color map
norm = TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)
cmap = plt.get_cmap('coolwarm_r')  # '_r' reverses the color map

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(15, 15))
gdf.plot(column='pct_dem_lead', cmap=cmap, linewidth=0, ax=ax, norm=norm)

# Remove axis
ax.axis('off')

# Set the axis limits to match the bounding box
ax.set_xlim(bbox[0], bbox[2])
ax.set_ylim(bbox[1], bbox[3])

plt.savefig('nyc_msa_election_2024.pdf', format='pdf', bbox_inches='tight')

# Show the plot
plt.show()
