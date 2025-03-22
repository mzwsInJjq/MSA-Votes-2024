import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

# Load the data
gdf1 = gpd.read_file(r"C:\Users\Chen\Downloads\OR24\Oregon2024\Oregon2024.shp")
gdf1['pct_dem_lead'] = (gdf1['USP24D'] - gdf1['USP24R']) / gdf1['USP24Tot']

gdf2 = gpd.read_file(r"C:\Users\Chen\Downloads\WA-precincts-with-results.geojson")

# Filter counties by gdf['GEOID']
gdf1 = gdf1[gdf1['County'].isin([51, 67, 5, 71, 9])]
gdf1 = gdf1.to_crs("epsg:4326")
gdf2 = gdf2[gdf2['GEOID'].str.startswith('53011') | gdf2['GEOID'].str.startswith('53059')]

# Concatenate the two GeoDataFrames
gdf = pd.concat([gdf1, gdf2], ignore_index=True)

# Define the bbox for Portland-Vancouver-Hillsboro, OR-WA MSA
bbox = (-123.7854910, 44.8857083, -121.5143826, 46.3892200)

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

plt.savefig('portland_msa_election_2024.pdf', format='pdf', bbox_inches='tight')

# Show the plot
plt.show()

sum_votes_dem = gdf['votes_dem'].sum()
sum_votes_rep = gdf['votes_rep'].sum()
sum_votes_third_party = gdf['votes_total'].sum() - sum_votes_dem - sum_votes_rep
sum_votes_total = gdf['votes_total'].sum()
print(f"Democratic % for Portland MSA: {100 * sum_votes_dem/sum_votes_total:.2f}%")
print(f"Republican % for Portland MSA: {100 * sum_votes_rep/sum_votes_total:.2f}%")
print(f"Third Party % for Portland MSA: {100 * sum_votes_third_party/sum_votes_total:.2f}%")