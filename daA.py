import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pyreadstat


# Load the CSV file for depression data
df_depression = pd.read_csv("Data/MentalHealth_Data/2022_MentalHealth_Data/Mental_Health_Survey_Feb_20_22.csv")

# Remove unnecessary columns and preprocess the data
df_depression = df_depression[['year_1', 'phq9_2']]
df_depression = df_depression.iloc[2:]
current_year = datetime.now().year
df_depression['year_1'] = df_depression['year_1'].astype(int)
df_depression['age'] = current_year - df_depression['year_1']
df_depression.drop(columns=['year_1'], inplace=True)
df_depression.rename(columns={'age': 'year_1'}, inplace=True)
df_depression['phq9_2'] = df_depression['phq9_2'].replace({'Several days': 'Depressed', 'Nearly every day': 'Depressed'})
result_depression = df_depression.groupby('year_1').size().reset_index(name='Depression_Count')

# Load the .sav file for social media usage data
df_social_media, meta = pyreadstat.read_sav("Data/NPORS_Data/2023/NPORS_2023_for_public_release.sav")

social_media_columns = ['SMUSE_a', 'SMUSE_c', 'SMUSE_d', 'SMUSE_e', 'SMUSE_i']
df_social_media = df_social_media[social_media_columns + ['AGE']].copy()
smuse_mapping = {
    'SMUSE_a': 'Facebook',
    'SMUSE_c': 'Twitter',
    'SMUSE_d': 'Instagram',
    'SMUSE_e': 'Snapchat',
    'SMUSE_i': 'TikTok'
}
df_social_media.rename(columns=smuse_mapping, inplace=True)
df_social_media = df_social_media[(df_social_media['AGE'] >= 21) & (df_social_media['AGE'] <= 53)]
grouped_df_social_media = df_social_media.groupby('AGE').agg(lambda x: (x == 1).sum())
grouped_df_social_media.reset_index(inplace=True)

# Load the .sav file for internet frequency data
df_internet_freq, meta = pyreadstat.read_sav("Data/NPORS_Data/2023/NPORS_2023_for_public_release.sav")

internet_freq_column = 'INTFREQ'
df_internet_freq = df_internet_freq[['AGE', internet_freq_column]].copy()
df_internet_freq = df_internet_freq[df_internet_freq[internet_freq_column].isin([1, 2])]
df_internet_freq = df_internet_freq[(df_internet_freq['AGE'] >= 21) & (df_internet_freq['AGE'] <= 53)]
grouped_internet_freq = df_internet_freq.groupby('AGE').size().reset_index(name='Internet_Frequency_Count')

# Load the CSV file for sadness data
df_sadness = pd.read_csv("Data/MentalHealth_Data/2022_MentalHealth_Data/Mental_Health_Survey_Feb_20_22.csv")

# Remove unnecessary columns and preprocess the data
df_sadness = df_sadness[['year_1', 'acha_12months_times_5']]
df_sadness = df_sadness.iloc[2:]
df_sadness['year_1'] = df_sadness['year_1'].astype(int)
df_sadness['age'] = current_year - df_sadness['year_1']
df_sadness.drop(columns=['year_1'], inplace=True)
df_sadness.rename(columns={'age': 'year_1'}, inplace=True)
df_sadness['acha_12months_times_5'] = (df_sadness['acha_12months_times_5'] == '11 or more times').astype(int)
result_sadness = df_sadness.groupby('year_1').sum().reset_index()

# Load the CSV file for 'was diagnosed with depression' data
df_diagnosed = pd.read_csv("Data/MentalHealth_Data/2022_MentalHealth_Data/Mental_Health_Survey_Feb_20_22.csv")

# Remove unnecessary columns and preprocess the data
df_diagnosed = df_diagnosed[['year_1', 'acha_services_1']]
df_diagnosed = df_diagnosed.iloc[2:]
df_diagnosed['year_1'] = df_diagnosed['year_1'].astype(int)
df_diagnosed['age'] = current_year - df_diagnosed['year_1']
df_diagnosed.drop(columns=['year_1'], inplace=True)
df_diagnosed.rename(columns={'age': 'year_1'}, inplace=True)
df_diagnosed['acha_services_1'] = (df_diagnosed['acha_services_1'] == 'Yes').astype(int)
result_diagnosed = df_diagnosed.groupby('year_1').sum().reset_index()

# Load the CSV file for anxiety data
df_anxiety = pd.read_csv("Data/MentalHealth_Data/2022_MentalHealth_Data/Mental_Health_Survey_Feb_20_22.csv")

# Remove unnecessary columns and preprocess the data
df_anxiety = df_anxiety[['year_1', 'gad7_1']]
df_anxiety = df_anxiety.iloc[2:]
df_anxiety['year_1'] = df_anxiety['year_1'].astype(int)
df_anxiety['age'] = current_year - df_anxiety['year_1']
df_anxiety.drop(columns=['year_1'], inplace=True)
df_anxiety.rename(columns={'age': 'year_1'}, inplace=True)
df_anxiety['gad7_1'] = df_anxiety['gad7_1'].replace({'Several days': 'Anxi', 'Nearly every day': 'Anxi'})
result_anxiety = df_anxiety.groupby('year_1').size().reset_index(name='Anxiety_Count')

# Read the CSV file for additional anxiety data
df_additional_anxiety = pd.read_csv("Data/MentalHealth_Data/2022_MentalHealth_Data/Mental_Health_Survey_Feb_20_22.csv")
df_additional_anxiety = df_additional_anxiety.iloc[2:]
current_year = 2024
df_additional_anxiety['age'] = current_year - df_additional_anxiety['year_1'].astype(int)
anxiety_df = df_additional_anxiety[df_additional_anxiety['gad7_1'].isin(['Several days', 'Nearly every day'])]
age_anxiety_counts = anxiety_df.groupby('age').size().reset_index(name='Anxiety_Count')

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))

# Plot line graph for depression count
ax.plot(result_depression['year_1'], result_depression['Depression_Count'], marker='o', linestyle='-', color='orange', label='Depression Count')

# Plot line graph for sadness count
ax.plot(result_sadness['year_1'], result_sadness['acha_12months_times_5'], marker='o', linestyle='-', color='blue', label='Sadness Count (11 or more times)')

# Plot bar graph for social media usage
social_media_platforms = ['Facebook', 'Twitter', 'Instagram', 'Snapchat', 'TikTok']
for platform in social_media_platforms:
    ax.bar(grouped_df_social_media['AGE'], grouped_df_social_media[platform], label=platform, alpha=0.5)

# Plot line graph for internet frequency count
ax.plot(grouped_internet_freq['AGE'], grouped_internet_freq['Internet_Frequency_Count'], marker='o', linestyle='-', color='green', label='Internet Frequency Count')

# Plot line graph for diagnosed with depression count
ax.plot(result_diagnosed['year_1'], result_diagnosed['acha_services_1'], marker='o', linestyle='-', color='red', label='Diagnosed with Depression Count')

# Plot line graph for additional anxiety count
ax.plot(age_anxiety_counts['age'], age_anxiety_counts['Anxiety_Count'], marker='o', linestyle='-', color='black', label='Anxiety Count')

# Set common y-axis label
ax.set_ylabel('Count')

# Add legend
ax.legend()

# Add title and show plot
plt.title('Depression, Sadness, Social Media Usage, Diagnosed with Depression, and Anxiety Count by Age')
plt.xlabel('Age')
plt.grid(True)
plt.tight_layout()
plt.show()