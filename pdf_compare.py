import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create figures directory if it doesn't exist
os.makedirs('figures', exist_ok=True)

# Set style
sns.set(style="whitegrid", font_scale=1.2)

# Load character comparison data
chars = pd.read_csv('comparison_franchise_characters.csv')

# Calculate total mentions across datasets
chars['total'] = (chars['COYO-700M_count'] + 
                  chars['ReLAION-2B_count'] + 
                  chars['DataComp-1B_count'])

# Figure 1: Top 15 characters by total mentions
top15 = chars.sort_values('total', ascending=False).head(15).copy()
top15['total_millions'] = top15['total'] / 1e6

plt.figure(figsize=(12, 8))
ax = sns.barplot(x='total_millions', y='metric', data=top15, palette='tab20')
plt.xlabel('Total Mentions (millions)')
plt.ylabel('')
plt.title('Top 15 Franchise Characters by Total Mentions Across Datasets')
ax.bar_label(ax.containers[0], fmt='%.2fM', padding=3)
plt.tight_layout()
plt.savefig('figures/fig1_top_characters.pdf', bbox_inches='tight')
plt.close()

# Figure 2: Average % per character by rights holder group
def assign_group(row):
    metric = row['metric']
    if any(x in metric for x in ['Disney', 'Marvel', 'Star Wars', 'Pixar']):
        return 'Disney/Marvel/Lucasfilm/Pixar'
    elif any(x in metric for x in ['DC', 'Warner', 'Bugs', 'Scooby']):
        return 'Warner Bros/DC'
    elif 'Nintendo' in metric:
        return 'Nintendo'
    elif 'Sega' in metric:
        return 'Sega'
    elif 'Nickelodeon' in metric:
        return 'Nickelodeon'
    elif any(x in metric for x in ['Universal', 'DreamWorks']):
        return 'Universal/DreamWorks'
    else:
        return 'Other'

chars['group'] = chars.apply(assign_group, axis=1)

# Average percentage across the three datasets for each character
chars['avg_pct'] = (
    chars['COYO-700M_pct'].str.rstrip('%').astype(float) +
    chars['ReLAION-2B_pct'].str.rstrip('%').astype(float) +
    chars['DataComp-1B_pct'].str.rstrip('%').astype(float)
) / 3

group_avg = chars.groupby('group')['avg_pct'].mean().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
ax = group_avg.plot(kind='bar', color='skyblue')
plt.ylabel('Average Mentions per Character (%)')
plt.xlabel('Rights Holder Group')
plt.title('Average Percentage Mentions per Character by Rights Holder')
plt.xticks(rotation=45, ha='right')
for i, v in enumerate(group_avg):
    ax.text(i, v + 0.0005, f'{v:.5f}%', ha='center')
plt.tight_layout()
plt.savefig('figures/fig2_rights_holders.pdf', bbox_inches='tight')
plt.close()

# Figure 3: Dataset variance (max/min ratio) for characters with notable variance
count_cols = ['COYO-700M_count', 'ReLAION-2B_count', 'DataComp-1B_count']
max_counts = chars[count_cols].max(axis=1)
min_counts = chars[count_cols].min(axis=1).replace(0, 1)  # avoid division by zero
chars['variance_ratio'] = max_counts / min_counts

variance_top = chars.sort_values('variance_ratio', ascending=False).head(12)

plt.figure(figsize=(10, 7))
ax = sns.barplot(x='variance_ratio', y='metric', data=variance_top, palette='viridis')
plt.xlabel('Max/Min Ratio Across Datasets')
plt.ylabel('')
plt.title('Highest Dataset Variance in Character Mentions (Max/Min Ratio)')
ax.bar_label(ax.containers[0], fmt='%.1fx', padding=3)
plt.tight_layout()
plt.savefig('figures/fig3_variance.pdf', bbox_inches='tight')
plt.close()

# Figure 4: Copyright indicators across datasets
copy_ind = pd.read_csv('comparison_copyright_indicators.csv')

# Select major indicators for clarity (optional; comment out to plot all)
major_indicators = ['Getty Images', 'Shutterstock', 'Associated Press', 'Copyright Symbol ©']
copy_ind = copy_ind[copy_ind['metric'].isin(major_indicators)]

copy_ind.plot(
    kind='bar',
    x='metric',
    y=['COYO-700M_count', 'ReLAION-2B_count', 'DataComp-1B_count'],
    figsize=(12, 8),
    width=0.8
)
plt.ylabel('Absolute Count')
plt.xlabel('')
plt.title('Selected Copyright Indicators by Dataset')
plt.xticks(rotation=45, ha='right')
plt.legend(['COYO-700M', 'ReLAION-2B', 'DataComp-1B'])
plt.tight_layout()
plt.savefig('figures/fig4_copyright_indicators.pdf', bbox_inches='tight')
plt.close()

print("All four figures generated successfully in the 'figures/' directory.")