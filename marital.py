import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from combined_data.csv
combined_data_path = 'Data/NPORS_Data/combined_data.csv'
df = pd.read_csv(combined_data_path)

# Mapping for marital status
marital_status_mapping = {
    1: 'Married',
    2: 'Living with partner',
    3: 'Divorced',
    4: 'Separated',
    5: 'Widowed',
    6: 'Never been married'
}

mapping_social_media = {
    'SMUSE_a': 'Facebook',
    'SMUSE_b': 'YouTube',
    'SMUSE_c': 'Twitter',
    'SMUSE_d': 'Instagram',
    'SMUSE_e': 'Snapchat',
    'SMUSE_f': 'WhatsApp',
    'SMUSE_g': 'LinkedIn',
    'SMUSE_h': 'Pinterest',
    'SMUSE_i': 'TikTok'
}

# Replace numerical marital status with labels
df['MARITAL'] = df['MARITAL'].map(marital_status_mapping)

# Group by marital status and calculate mean social media usage percentage
social_media_data = df.groupby('MARITAL')[list(mapping_social_media.keys())].mean()

# Rename columns based on social media mapping
social_media_data.rename(columns=mapping_social_media, inplace=True)

# Plotting
plt.figure(figsize=(12, 6))

# Use seaborn for better styling
sns.set(style="whitegrid")

# Plot grouped bar plot
social_media_data.plot(kind='bar', figsize=(12, 6))

# Adjust legend position outside the plot
plt.legend(title='Social Media Platform', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.title('Social Media Usage by Marital Status')
plt.xlabel('Marital Status')
plt.ylabel('Percentage')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.show()

