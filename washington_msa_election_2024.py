import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

# Load the data
gdf1 = gpd.read_file(r"C:\Users\Chen\Downloads\DC-precincts-with-results.geojson")
gdf2 = gpd.read_file(r"C:\Users\Chen\Downloads\VA-precincts-with-results.geojson")
gdf3 = gpd.read_file(r"C:\Users\Chen\Downloads\MD-precincts-with-results.geojson")
gdf4 = gpd.read_file(r"C:\Users\Chen\Downloads\WV-precincts-with-results.geojson")

# Filter counties by gdf['GEOID']
gdf2 = gdf2[gdf2['GEOID'].str.startswith('51059') | gdf2['GEOID'].str.startswith('51153') | gdf2['GEOID'].str.startswith('51107') | gdf2['GEOID'].str.startswith('51013') | gdf2['GEOID'].str.startswith('51510') | gdf2['GEOID'].str.startswith('51179') | gdf2['GEOID'].str.startswith('51177') | gdf2['GEOID'].str.startswith('51061') | gdf2['GEOID'].str.startswith('51047') | gdf2['GEOID'].str.startswith('51683') | gdf2['GEOID'].str.startswith('51187') | gdf2['GEOID'].str.startswith('51630') | gdf2['GEOID'].str.startswith('51600') | gdf2['GEOID'].str.startswith('51685') | gdf2['GEOID'].str.startswith('51043') | gdf2['GEOID'].str.startswith('51610') | gdf2['GEOID'].str.startswith('51157')]
gdf3 = gdf3[gdf3['GEOID'].str.startswith('24031') | gdf3['GEOID'].str.startswith('24033') | gdf3['GEOID'].str.startswith('24021') | gdf3['GEOID'].str.startswith('24017')]
gdf4 = gdf4[gdf4['GEOID'].str.startswith('54037')]

# Concatenate the four GeoDataFrames
gdf = pd.concat([gdf1, gdf2, gdf3, gdf4], ignore_index=True)

# Define the bbox for Washington-Arlington-Alexandria, DC-VA-MD-WV MSA
bbox = (-78.3947036, 37.9906883, -76.6624791, 39.7200280)

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

plt.savefig('washington_msa_election_2024.pdf', format='pdf', bbox_inches='tight')

# Show the plot
plt.show()

sum_votes_dem = gdf['votes_dem'].sum()
sum_votes_rep = gdf['votes_rep'].sum()
sum_votes_third_party = gdf['votes_total'].sum() - sum_votes_dem - sum_votes_rep
sum_votes_total = gdf['votes_total'].sum()
print(f"Democratic % for Washington MSA: {100 * sum_votes_dem/sum_votes_total:.2f}%")
print(f"Republican % for Washington MSA: {100 * sum_votes_rep/sum_votes_total:.2f}%")
print(f"Third Party % for Washington MSA: {100 * sum_votes_third_party/sum_votes_total:.2f}%")