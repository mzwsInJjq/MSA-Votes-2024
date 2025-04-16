# https://www.metroatlantachamber.com/wp-content/uploads/2022/11/atlmsa_map_8.9.21-1.pdf

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

# Load the data
gdf = gpd.read_file(r"D:\Misc\GA-precincts-with-results.geojson")

# Filter counties by gdf['GEOID']
atlanta_msa_counties = ['13013', '13063', '13097', '13143', '13199', '13231', '13015', '13067', '13113', '13149', '13211', '13247', '13035', '13077', '13117', '13151', '13217', '13255', '13045', '13085', '13121', '13159', '13223', '13297', '13057', '13089', '13135', '13171', '13227']
gdf = gdf[gdf['GEOID'].str.startswith(tuple(atlanta_msa_counties))]

# Define the bbox for Atlanta-Sandy Springs-Alpharetta, GA MSA
bbox = (-85.3867732, 32.8446400, -83.2691960, 34.6176260)

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

plt.savefig('atlanta_msa_election_2024.pdf', format='pdf', bbox_inches='tight')

# Show the plot
plt.show()

sum_votes_dem = gdf['votes_dem'].sum()
sum_votes_rep = gdf['votes_rep'].sum()
sum_votes_third_party = gdf['votes_total'].sum() - sum_votes_dem - sum_votes_rep
sum_votes_total = gdf['votes_total'].sum()
print(f"Democratic % for Atlanta MSA: {100 * sum_votes_dem/sum_votes_total:.2f}%")
print(f"Republican % for Atlanta MSA: {100 * sum_votes_rep/sum_votes_total:.2f}%")
print(f"Third Party % for Atlanta MSA: {100 * sum_votes_third_party/sum_votes_total:.2f}%")