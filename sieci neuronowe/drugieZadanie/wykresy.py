import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data into a DataFrame
data = {
    'confidenceFactor': [0.85, 0.65, 0.25, 0.85, 0.65, 0.25, 0.25, 0.25, 0.25, 0.65, 0.65, 0.85, 0.85, 0.85],
    'minNumObj': [2, 2, 2, 2, 2, 2, 4, 6, 2, 4, 6, 2, 4, 6],
    'binarySplits': [False, False, False, True, True, True, True, True, True, True, True, True, True, True],
    'Precision': [0.534, 0.517, 0.532, 0.61, 0.61, 0.567, 0.567, 0.558, 0.547, 0.61, 0.534, 0.534, 0.61, 0.561],
    'Recall': [0.549, 0.533, 0.533, 0.626, 0.626, 0.59, 0.59, 0.585, 0.574, 0.626, 0.549, 0.549, 0.626, 0.574],
    'Kappa': [0.0249, -0.0107, 0.0213, 0.1698, 0.1698, 0.0836, 0.0836, 0.0654, 0.045, 0.1698, 0.0249, 0.0249, 0.1698, 0.0781]
}
data_all_attr= {
    'confidenceFactor': [0.85, 0.65, 0.25, 0.85, 0.65, 0.45, 0.25, 0.25, 0.25, 0.65, 0.65, 0.65, 0.85, 0.85, 0.85],
    'minNumObj': [2, 2, 2, 2, 2, 2, 2, 4, 6, 2, 4, 6, 2, 4, 6],
    'binarySplits': [False, False, False, True, True, True, True, True, True, True, True, True, True, True, True],
    'Precision': [0.497, 0.497, 0.508, 0.555, 0.555, 0.557, 0.557, 0.538, 0.545, 0.555, 0.565, 0.522, 0.555, 0.565, 0.522],
    'Recall': [0.497, 0.497, 0.508, 0.549, 0.549, 0.549, 0.549, 0.549, 0.559, 0.549, 0.569, 0.528, 0.549, 0.569, 0.528],
    'Kappa': [-0.0516, -0.0516, -0.0302, 0.0683, 0.0683, 0.0724, 0.0724, 0.0339, 0.0471, 0.0683, 0.0904, -0.0008, 0.0683, 0.0904, -0.0008]
}

lengths = {key: len(value) for key, value in data.items()}

# Check if all lengths are the same
all_same_length = len(set(lengths.values())) == 1

print("All lists have the same length:", all_same_length)
print("Lengths of each list:", lengths)
df = pd.DataFrame(data)

# Set up the figure and axes
fig, axes = plt.subplots(3, 1, figsize=(10, 15), sharex=True)

# Plot Precision
sns.lineplot(data=df, x='confidenceFactor', y='Precision', hue='binarySplits', style='minNumObj', markers=True, ax=axes[0])
axes[0].set_title('Precision by Confidence Factor')
axes[0].set_ylabel('Precision')

# Plot Recall
sns.lineplot(data=df, x='confidenceFactor', y='Recall', hue='binarySplits', style='minNumObj', markers=True, ax=axes[1])
axes[1].set_title('Recall by Confidence Factor')
axes[1].set_ylabel('Recall')

# Plot Kappa
sns.lineplot(data=df, x='confidenceFactor', y='Kappa', hue='binarySplits', style='minNumObj', markers=True, ax=axes[2])
axes[2].set_title('Kappa by Confidence Factor')
axes[2].set_ylabel('Kappa')
axes[2].set_xlabel('Confidence Factor')

# Adjust layout and show plot
plt.tight_layout()
plt.show()