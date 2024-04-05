age_bins = [0, 18, 25, 35, 45, 55, 65, 100]
age_labels = ['0-18', '19-25', '26-35', '36-45', '46-55', '56-65', '66+']

for idx, df in enumerate(NPORS_df):
    print(f"Dataframe {idx + 1} Title: {df.name if hasattr(df, 'name') else 'Unnamed'}")
    
    # Check and categorize AGE into bins
    if 'AGE' in df:
        df['AGE_GROUP'] = pd.cut(df['AGE'], bins=age_bins, labels=age_labels, right=False)
    else:
        continue  # If none of the specified age columns are found, skip to the next dataframe

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
