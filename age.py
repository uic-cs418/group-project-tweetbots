import pandas as pd
import matplotlib.pyplot as plt
import pyreadstat

# Paths to NPORS data files
file_paths = {
    'NPORS_2020': 'TwitterBots_Data/NPORS_Data/2020/NPORS 2020.sav',
    'NPORS_2021': 'TwitterBots_Data/NPORS_Data/2021/NPORS_2021_for_public_release.sav',
    'NPORS_2022': 'TwitterBots_Data/NPORS_Data/2022/NPORS_2022_for_public_release.sav',
    'NPORS_2023': 'TwitterBots_Data/NPORS_Data/2023/NPORS_2023_for_public_release.sav'
}

# Read NPORS data
datasets = {}
for key, path in file_paths.items():
    datasets[key], _ = pyreadstat.read_sav(path)

# Display dataset information
for name, data in datasets.items():
    print(f'Dataset Information for {name}:\n')
    print(data.info())
    print(f'Number of unique values in each column:\n{data.nunique()}')

# Initialize combined dataframe
combined_df = pd.DataFrame()

# Assign names to datasets
for key, df in datasets.items():
    df.name = key

# Mapping of social media codes to platform names
social_media_mapping = {
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

# Age bins and labels
age_bins = [0, 18, 25, 35, 45, 55, 65, 100]
age_labels = ['0-18', '19-25', '26-35', '36-45', '46-55', '56-65', '66+']

# Analyze data for each dataset
for key, df in datasets.items():
    print(f"Analysis of Dataset {key}: {df.name if hasattr(df, 'name') else 'Unnamed'}")

    # Check and categorize AGE into bins
    if 'AGE' in df:
        df['AGE_GROUP'] = pd.cut(df['AGE'], bins=age_bins, labels=age_labels, right=False)
    else:
        continue

    # Group by age group
    groups = df.groupby(['AGE_GROUP'])

    # Initialize dictionary to store social media data
    social_media_data = {social_media: [] for social_media in social_media_mapping.values()}

    # Calculate average social media usage for each age group
    for group_name, group_df in groups:
        selected_data = group_df[list(social_media_mapping.keys())]
        selected_data = selected_data.rename(columns=social_media_mapping)
        social_media_percentages = selected_data.div(selected_data.sum(axis=1), axis=0) * 100
        for social_media in social_media_percentages.columns:
            social_media_data[social_media].append(social_media_percentages[social_media].mean())

    # Create DataFrame for social media usage
    social_media_df = pd.DataFrame(social_media_data, index=age_labels)

    # Plotting
    social_media_df.plot(kind='line', figsize=(12, 6), marker='o')
    plt.legend(title='Social Media Platform')
    plt.title(f'Social Media Usage by Age Group - {df.name if hasattr(df, "name") else "Unnamed"}')
    plt.xlabel('Age Group')
    plt.ylabel('Percentage')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
