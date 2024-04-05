import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pyreadstat

NPORS_2020 = 'TwitterBots_Data/NPORS_Data/2020/NPORS 2020.sav'  
NPORS_2021 = 'TwitterBots_Data/NPORS_Data/2021/NPORS_2021_for_public_release.sav'
NPORS_2022 = 'TwitterBots_Data/NPORS_Data/2022/NPORS_2022_for_public_release.sav'
NPORS_2023 = 'TwitterBots_Data/NPORS_Data/2023/NPORS_2023_for_public_release.sav'

df_2020 , meta_2020 = pyreadstat.read_sav(NPORS_2020)
df_2021 , meta_2021 = pyreadstat.read_sav(NPORS_2021)
df_2022 , meta_2022 = pyreadstat.read_sav(NPORS_2022)
df_2023 , meta_2022 = pyreadstat.read_sav(NPORS_2023)
NPORS_df = [df_2020, df_2021, df_2022, df_2023]

for index in NPORS_df:
    print(f'Information. \n')
    print(index.info())
    print(f' Number of unique values in each column:\n{index.nunique()}')


combined_df = pd.DataFrame()
names = ["2020_df", "2021_df", "2023_df", "2024_df"] 
for idx, df in enumerate(NPORS_df):
    df.name = names[idx]

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

age_bins = [0, 18, 25, 35, 45, 55, 65, 100]
age_labels = ['0-18', '19-25', '26-35', '36-45', '46-55', '56-65', '66+']

for idx, df in enumerate(NPORS_df):
    print(f"Dataframe {idx + 1} Title: {df.name if hasattr(df, 'name') else 'Unnamed'}")
    
    # Check and categorize AGE into bins
    if 'AGE' in df:
        df['AGE_GROUP'] = pd.cut(df['AGE'], bins=age_bins, labels=age_labels, right=False)
    else:
        continue

    groups = df.groupby(['AGE_GROUP'])

    social_media_data = {social_media: [] for social_media in mapping_socialmedia.values()}
    
    for group_name, group_df in groups:
        selected_data = group_df[list(mapping_socialmedia.keys())]
        selected_data = selected_data.rename(columns=mapping_socialmedia) 
        social_media_percentages = selected_data.div(selected_data.sum(axis=1), axis=0) * 100
        for social_media in social_media_percentages.columns:
            social_media_data[social_media].append(social_media_percentages[social_media].mean())

    social_media_df = pd.DataFrame(social_media_data, index=age_labels)
    
    # Plotting
    social_media_df.plot(kind='bar', figsize=(12, 6))
    plt.legend(title='Social Media Platform')
    plt.title(f'Social Media Usage by Age Group - {df.name if hasattr(df, "name") else "Unnamed"}')
    plt.xlabel('Age Group')
    plt.ylabel('Percentage')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
