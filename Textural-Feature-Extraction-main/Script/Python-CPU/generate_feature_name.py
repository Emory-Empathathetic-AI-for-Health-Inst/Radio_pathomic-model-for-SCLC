import csv

# Define the name of the statistic
stats = ['mean', 'std', 'skewness', 'kurtosis', 'median']

# Generate Gabor feature names
gabor_features = [f'Gabor_f{f}_theta{t}_{s}' for f in [0, 2, 4, 8, 16, 32]
                                              for t in range(8)
                                              for s in stats]

# Generating Law's Feature Names
laws_bases = ['L', 'E', 'S', 'W', 'R']
laws_features = [f'Laws_{a}{b}_{s}' for a in laws_bases
                                    for b in laws_bases
                                    for s in stats]

# Generating Haralick Feature Names
haralick_features = [f'Haralick_{i}_{s}' for i in range(1, 14)
                                          for s in stats]

# Merge all feature names
feature_names = gabor_features + laws_features + haralick_features

# Write to CSV file
with open('feature_names.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(feature_names)