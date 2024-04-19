import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pyreadstat

# File paths for NPORS data
file_paths = {
    '2020': 'TwitterBots_Data/NPORS_Data/2020/NPORS 2020.sav',
    '2021': 'TwitterBots_Data/NPORS_Data/2021/NPORS_2021_for_public_release.sav',
    '2022': 'TwitterBots_Data/NPORS_Data/2022/NPORS_2022_for_public_release.sav',
    '2023': 'TwitterBots_Data/NPORS_Data/2023/NPORS_2023_for_public_release.sav'
}

# Read NPORS data
datasets = {}
for year, path in file_paths.items():
    datasets[year], _ = pyreadstat.read_sav(path)

# Display dataset information
for year, data in datasets.items():
    print(f'Dataset Info for {year}:\n')
    print(data.info())
    print(f'Number of unique values in each column:\n{data.nunique()}')

# Combine datasets
combined_df = pd.DataFrame()
for year, df in datasets.items():
    df.name = f"{year}_df"

# Social media platform mapping
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

# Analyze data for each dataset
for year, df in datasets.items():
    print(f"Analysis of Dataset {year}: {df.name if hasattr(df, 'name') else 'Unnamed'}")

    # Group data by education level
    groups = None

    if 'EDUCATION' in df:
        groups = df.groupby(['EDUCATION'])
        group_label = 'EDUCATION'
    elif 'EDUC_ACS' in df:
        groups = df.groupby(['EDUC_ACS'])
        group_label = 'EDUC_ACS'
    else:
        pass

    # Collect social media usage data
    social_media_data = {social_media: [] for social_media in social_media_mapping.values()}

    for group_name, group_df in groups:
        selected_data = group_df[
            ['SMUSE_a', 'SMUSE_b', 'SMUSE_c', 'SMUSE_d', 'SMUSE_e', 'SMUSE_f', 'SMUSE_g', 'SMUSE_h', 'SMUSE_i']]
        selected_data = selected_data.rename(columns=social_media_mapping)
        social_media_counts = selected_data.sum()
        for social_media, count in social_media_counts.items():
            social_media_data[social_media].append(count)

    # Create DataFrame for social media usage
    social_media_df = pd.DataFrame(social_media_data)
    plt.figure(figsize=(12, 6))

    # Plot line chart for each social media platform
    for social_media in social_media_df.columns:
        plt.plot(social_media_df.index, social_media_df[social_media], marker='o', label=social_media)
    plt.legend(title='Social Media Platform')
    plt.title(f'Social Media Usage by Education Level - {df.name if hasattr(df, "name") else "Unnamed"}')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
