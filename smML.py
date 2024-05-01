import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pyreadstat
import matplotlib.pyplot as plt

# Load the SPSS dataset
df, meta = pyreadstat.read_sav('Data/NPORS_Data/2023/NPORS_2023_for_public_release.sav')

# Select relevant columns
columns = ['AGE', 'INTFREQ', 'SMUSE_a', 'SMUSE_b', 'SMUSE_c', 'SMUSE_d', 'SMUSE_e', 'SMUSE_f', 'SMUSE_g', 'SMUSE_h', 'SMUSE_i']
df_selected = df[columns]

# Drop rows with any missing values
df_selected.dropna(inplace=True)

# Separate features (X) and target (y)
X = df_selected.drop(columns=['SMUSE_a', 'SMUSE_b', 'SMUSE_c', 'SMUSE_d', 'SMUSE_e', 'SMUSE_f', 'SMUSE_g', 'SMUSE_h', 'SMUSE_i'])
y = df_selected['SMUSE_a']

# Initialize list to store accuracies
accuracies = []
sample_sizes = range(100, len(df_selected), 100)  # Define sample sizes

# Iterate over different sample sizes
for sample_size in sample_sizes:
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=sample_size / len(df_selected), random_state=42)

    # Impute missing values in X_train and X_test
    imputer = SimpleImputer(strategy='mean')
    imputer.fit(X_train)
    X_train_imputed = imputer.transform(X_train)
    X_test_imputed = imputer.transform(X_test)

    # Train a RandomForestClassifier
    clf = RandomForestClassifier()
    clf.fit(X_train_imputed, y_train)

    # Predict on the test set
    y_pred = clf.predict(X_test_imputed)

    # Calculate accuracy and append to accuracies list
    accuracy = accuracy_score(y_test, y_pred)
    accuracies.append(accuracy)

# Plotting the graph of accuracy
plt.plot(sample_sizes, accuracies, marker='o')
plt.xlabel('Sample Size')
plt.ylabel('Accuracy')
plt.title('Accuracy vs Sample Size')
plt.show()




