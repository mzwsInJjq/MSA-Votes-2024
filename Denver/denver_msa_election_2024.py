import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

# Load the data
gdf = gpd.read_file(r'C:\Users\Chen\Downloads\CO24\CO24.shp')

print(gdf['COUNTY'].unique().tolist())

# Filter precincts in gdf by gdf['COUNTY']
gdf = gdf[gdf['COUNTY'].str.startswith('Denver') | gdf['COUNTY'].str.startswith('Arapahoe') | gdf['COUNTY'].str.startswith('Jefferson') | gdf['COUNTY'].str.startswith('Adams') | gdf['COUNTY'].str.startswith('Douglas') | gdf['COUNTY'].str.startswith('Broomfield') | gdf['COUNTY'].str.startswith('Elbert') | gdf['COUNTY'].str.startswith('Park') | gdf['COUNTY'].str.startswith('Gilpin') | gdf['COUNTY'].str.startswith('Clear Creek')]

# Calculate the Democratic margin in each precinct for gdf
gdf['pct_dem_lead'] = (gdf['PresDem'] - gdf['PresRep']) / gdf['PresTot']

# Define the bbox for Denver-Aurora-Centennial, CO MSA
bbox = (-106.2102060, 38.6910970, -103.7056950, 40.0442270)

# Filter the GeoDataFrame to include only precincts within the bbox
gdf = gdf.to_crs("epsg:4326")
gdf = gdf.cx[bbox[0]:bbox[2], bbox[1]:bbox[3]]

# Create a color map
norm = TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)
cmap = plt.get_cmap('bwr_r')  # '_r') reverses the color map

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(15, 15))
gdf.plot(column='pct_dem_lead', cmap=cmap, linewidth=0, ax=ax, norm=norm)

# Set the axis limits to match the bounding box
ax.set_xlim(bbox[0], bbox[2])
ax.set_ylim(bbox[1], bbox[3])

# Remove axis
ax.axis('off')

plt.savefig('denver_msa_election_2024.pdf', format='pdf', bbox_inches='tight')

# Show the plot
plt.show()

sum_votes_dem = gdf['PresDem'].sum()
sum_votes_rep = gdf['PresRep'].sum()
sum_votes_third_party = gdf['PresTot'].sum() - sum_votes_dem - sum_votes_rep
sum_votes_total = gdf['PresTot'].sum()
print(f"Democratic % for Denver MSA: {100 * sum_votes_dem/sum_votes_total:.2f}%")
print(f"Republican % for Denver MSA: {100 * sum_votes_rep/sum_votes_total:.2f}%")
print(f"Third Party % for Denver MSA: {100 * sum_votes_third_party/sum_votes_total:.2f}%")
