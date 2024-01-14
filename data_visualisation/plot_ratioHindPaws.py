import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

path_ratios = r"H:\.shortcut-targets-by-id\1MH0egFqTqTToPE-wxCs7mDWL48lVKqDB\EurDyscover\Dystonia_Data\perSessionAnalysis_meanRatioHindPaws.csv"
df = pd.read_csv(path_ratios)

# Extract surgery and genetic information from groupSpecs
df['Surgery'] = df['groupSpecs'].apply(lambda x: x.split('_')[0])
df['Genetic_Info'] = df['groupSpecs'].apply(lambda x: x.split('_')[1])
df['Timepoint'] = df['groupSpecs'].apply(lambda x: x.split('_')[2])

# Combine Surgery and Genetic_Info to create distinct groups
df['Group'] = df['Surgery'] + '_' + df['Genetic_Info']

# Map the Group to different colors
palette = sns.color_palette("husl", n_colors=len(df['Group'].unique()))
color_mapping = dict(zip(df['Group'].unique(), palette))

# Box plot with mean, standard deviation, and individual data points
plt.figure(figsize=(12, 8))
box_plot = sns.boxplot(x='Timepoint', y='ratioDistances_digitalTip_heel_hindPaws', hue='Group', data=df, showmeans=True, meanprops={"marker":"o","markerfacecolor":"white", "markeredgecolor":"black"}, boxprops=dict(alpha=.3), palette=color_mapping)
sns.swarmplot(x='Timepoint', y='ratioDistances_digitalTip_heel_hindPaws', hue='Group', data=df, dodge=True, palette=color_mapping)

plt.title('Box Plot with Mean, Standard Deviation, and Individual Data Points')
plt.xlabel('Timepoint')
plt.ylabel('Ratio Distances (Digital Tip to Heel of Hind Paws)')
plt.legend(title='Group Specifications', loc='upper right')

plt.show()