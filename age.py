import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
dff = pd.read_csv("Data/NPORS_Data/combined_data.csv")

# Define the list of column names related to social media usage
social_media_columns = ['SMUSE_a', 'SMUSE_c', 'SMUSE_d', 'SMUSE_e', 'SMUSE_i']

# Filter the DataFrame to include only the social media columns and 'AGE'
dff_social_media = dff[social_media_columns + ['AGE']].copy()  # Make a copy of the DataFrame

# Define a dictionary to map column names to corresponding social media platforms
smuse_mapping = {
    'SMUSE_a': 'Facebook',
    'SMUSE_c': 'Twitter',
    'SMUSE_d': 'Instagram',
    'SMUSE_e': 'Snapchat',
    'SMUSE_i': 'TikTok'
}

# Rename the columns according to the mapping
dff_social_media.rename(columns=smuse_mapping, inplace=True)

# Group ages in slices of 5 years and calculate the sum for each group
dff_social_media['AGE_GROUP'] = pd.cut(dff_social_media['AGE'], bins=range(10, 116, 5), right=False)
grouped_dff = dff_social_media.groupby('AGE_GROUP').agg(lambda x: (x == 1).sum())

# Reset index to make 'AGE_GROUP' a column instead of an index
grouped_dff.reset_index(inplace=True)

# Plot the bar plot
plt.figure(figsize=(12, 6))

# Define colors for each platform
colors = ['blue', 'green', 'red', 'purple', 'orange']

# Define the social media platforms
social_media_platforms = ['Facebook', 'Twitter', 'Instagram', 'Snapchat', 'TikTok']

# Plot bars for each platform
for i, platform in enumerate(social_media_platforms):
    plt.bar(grouped_dff['AGE_GROUP'].astype(str), grouped_dff[platform], color=colors[i], label=platform)

plt.xlabel('Age Group')
plt.ylabel('Number of Users')
plt.title('Social Media Usage by Age Group')
plt.xticks(rotation=45, ha='right')
plt.legend()
plt.tight_layout()
plt.show()


