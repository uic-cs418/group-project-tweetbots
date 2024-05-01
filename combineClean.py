import pyreadstat
import pandas as pd

# List of file names
file_names = ['Data/NPORS_Data/2020/NPORS 2020.sav', 'Data/NPORS_Data/2021/NPORS_2021_for_public_release.sav', 
              'Data/NPORS_Data/2022/NPORS_2022_for_public_release.sav', 'Data/NPORS_Data/2023/NPORS_2023_for_public_release.sav']

# Initialize an empty list to store DataFrames
dfs = []

# Read each .sav file and append its DataFrame to the list
for file_name in file_names:
    df, _ = pyreadstat.read_sav(file_name)
    dfs.append(df)

# Combine all DataFrames into one
combined_df = pd.concat(dfs, ignore_index=True)
combined_df = combined_df.fillna(0)

# Remove rows where RESPID_AP20 is zero
combined_df = combined_df[combined_df['RESPID_AP20'] != 0]

# Write the cleaned DataFrame to a new CSV file
combined_df.to_csv('combined_cleaned_data.csv', index=False)


