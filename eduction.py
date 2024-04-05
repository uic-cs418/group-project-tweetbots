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

for idx, df in enumerate(NPORS_df):
    # Print out the title of the dataframe
    print(f"Dataframe {idx + 1} Title: {df.name if hasattr(df, 'name') else 'Unnamed'}")
    
    if 'EDUCATION' in df:
        groups = df.groupby(['EDUCATION'])
        group_label = 'EDUCATION'
    elif 'EDUC_ACS' in df:
        groups = df.groupby(['EDUC_ACS'])
        group_label = 'EDUC_ACS'
    else: 
        pass

    social_media_data = {social_media: [] for social_media in mapping_socialmedia.values()}
    legend_labels = []
    
    for group_name, group_df in groups:
        selected_data = group_df[['SMUSE_a', 'SMUSE_b', 'SMUSE_c', 'SMUSE_d', 'SMUSE_e', 'SMUSE_f', 'SMUSE_g', 'SMUSE_h', 'SMUSE_i']]
        selected_data = selected_data.rename(columns=mapping_socialmedia) 
        social_media_counts = selected_data.sum()  
        for social_media, count in social_media_counts.items():
            social_media_data[social_media].append(count)
        
        
    social_media_df = pd.DataFrame(social_media_data)
    plt.figure(figsize=(12, 6))
    
    for social_media in social_media_df.columns:
        plt.bar(social_media_df.index, social_media_df[social_media], label=social_media)
    plt.legend(title='Social Media Platform')
    plt.title(f'Social Media Usage by Education Level - {df.name if hasattr(df, "name") else "Unnamed"}')
    plt.ylabel('Count')
    plt.xticks(range(len(legend_labels)), legend_labels, rotation=45)
    plt.tight_layout()
    #plt.show()