import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pyreadstat

# Data paths
NPORS_2020 = 'TwitterBots_Data/NPORS_Data/2020/NPORS 2020.sav'
NPORS_2021 = 'TwitterBots_Data/NPORS_Data/2021/NPORS_2021_for_public_release.sav'
NPORS_2022 = 'TwitterBots_Data/NPORS_Data/2022/NPORS_2022_for_public_release.sav'
NPORS_2023 = 'TwitterBots_Data/NPORS_Data/2023/NPORS_2023_for_public_release.sav'

# Reading data
df_2020, meta_2020 = pyreadstat.read_sav(NPORS_2020)
df_2021, meta_2021 = pyreadstat.read_sav(NPORS_2021)
df_2022, meta_2022 = pyreadstat.read_sav(NPORS_2022)
df_2023, meta_2022 = pyreadstat.read_sav(NPORS_2023)
NPORS_df = [df_2020, df_2021, df_2022, df_2023]

# Displaying information
for index in NPORS_df:
    print(f'Dataset Information:\n')
    print(index.info())
    print(f'Number of unique values in each column:\n{index.nunique()}')

# Combining dataframes
combined_df = pd.DataFrame()
names = ["2020_df", "2021_df", "2023_df", "2024_df"]

for idx, df in enumerate(NPORS_df):
    df.name = names[idx]

# Social media mapping
mapping_socialmedia = {
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

# Analyzing data
for idx, df in enumerate(NPORS_df):
    # Print dataframe title
    print(f"Analysis of Dataset {idx + 1}: {df.name if hasattr(df, 'name') else 'Unnamed'}")

    # Grouping by marital status
    groups = None

    if 'MARITAL' in df:
        groups = df.groupby(['MARITAL'])
        group_label = 'MARITAL'
    else:
        pass

    # Social media usage by marital status
    social_media_data = {social_media: [] for social_media in mapping_socialmedia.values()}
    legend_labels = ["Married", "Living with a partner", "Divorced", "Separated", "Widowed", "Never been married"]

    # Check if groups exist before iterating
    if groups is not None:
        for group_name, group_df in groups:
            selected_data = group_df[
                ['SMUSE_a', 'SMUSE_b', 'SMUSE_c', 'SMUSE_d', 'SMUSE_e', 'SMUSE_f', 'SMUSE_g', 'SMUSE_h', 'SMUSE_i']]
            selected_data = selected_data.rename(columns=mapping_socialmedia)
            # Calculate percentages
            social_media_percentages = selected_data.div(selected_data.sum(axis=1), axis=0) * 100
            for social_media in social_media_percentages.columns:
                social_media_data[social_media].append(social_media_percentages[social_media].mean())

        social_media_df = pd.DataFrame(social_media_data)
        plt.figure(figsize=(12, 6))

        # Plotting
        for col in social_media_df.columns:
            plt.plot(legend_labels, social_media_df[col], marker='o', label=col)

        plt.legend(title='Social Media Platform')
        plt.title(f'Social Media Usage by Marital Status - {df.name if hasattr(df, "name") else "Unnamed"}')
        plt.xlabel('Marital Status')
        plt.ylabel('Percentage')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()
