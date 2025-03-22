import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

# Load the data
gdf1 = gpd.read_file(r"C:\Users\Chen\Downloads\MA-precincts-with-results.geojson")
gdf2 = gpd.read_file(r"C:\Users\Chen\Downloads\NH-precincts-with-results.geojson")

# Filter counties by gdf['GEOID']
gdf1 = gdf1[gdf1['GEOID'].str.startswith('25009') | gdf1['GEOID'].str.startswith('25017') | gdf1['GEOID'].str.startswith('25021') | gdf1['GEOID'].str.startswith('25023') | gdf1['GEOID'].str.startswith('25025')]
gdf2 = gdf2[gdf2['GEOID'].str.startswith('33015') | gdf2['GEOID'].str.startswith('33017')]

# Concatenate the two GeoDataFrames
gdf = pd.concat([gdf1, gdf2], ignore_index=True)

# Define the bbox for Boston-Cambridge-Newton, MA-NH Metropolitan Statistical Area
bbox = (-71.8987719, 41.5665119, -70.4560544, 43.5729888)

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

plt.savefig('boston_msa_election_2024.pdf', format='pdf', bbox_inches='tight')

# Show the plot
plt.show()

sum_votes_dem = gdf['votes_dem'].sum()
sum_votes_rep = gdf['votes_rep'].sum()
sum_votes_third_party = gdf['votes_total'].sum() - sum_votes_dem - sum_votes_rep
sum_votes_total = gdf['votes_total'].sum()
print(f"Democratic % for Boston MSA: {100 * sum_votes_dem/sum_votes_total:.2f}%")
print(f"Republican % for Boston MSA: {100 * sum_votes_rep/sum_votes_total:.2f}%")
print(f"Third Party % for Boston MSA: {100 * sum_votes_third_party/sum_votes_total:.2f}%")