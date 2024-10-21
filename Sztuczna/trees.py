import pandas as pd
import math


def entropy(data):
    if len(data) == 0:
        return 0
    counts = data['Survived'].value_counts()
    probabilities = counts / len(data)
    return -sum(p * math.log2(p) for p in probabilities if p > 0)


def find_best_split(data, attribute):
    sorted_data = data.sort_values(by=attribute)
    best_entropy = float('inf')
    best_threshold = None

    for i in range(1, len(sorted_data)):
        if sorted_data['Survived'].iloc[i] != sorted_data['Survived'].iloc[i - 1]:
            threshold = (sorted_data[attribute].iloc[i] + sorted_data[attribute].iloc[i - 1]) / 2
            left = sorted_data[sorted_data[attribute] <= threshold]
            right = sorted_data[sorted_data[attribute] > threshold]
            weighted_entropy = (len(left) / len(data)) * entropy(left) + (len(right) / len(data)) * entropy(right)

            if weighted_entropy < best_entropy:
                best_entropy = weighted_entropy
                best_threshold = threshold

    return best_entropy, best_threshold


def conditional_entropy(data, attribute):
    if attribute == 'Age':
        return find_best_split(data, attribute)
    else:
        total_entropy = 0
        for value in data[attribute].unique():
            subset = data[data[attribute] == value]
            total_entropy += len(subset) / len(data) * entropy(subset)
     
        return total_entropy, None


def information_gain(data, attribute):
    cond_entropy, threshold = conditional_entropy(data, attribute)
    return entropy(data) - cond_entropy, threshold


def gain_ratio(data, attribute):
    ig, threshold = information_gain(data, attribute)
    if attribute == 'Age':
        left = data[data[attribute] <= threshold]
        right = data[data[attribute] > threshold]
        intrinsic = -(len(left) / len(data)) * math.log2(len(left) / len(data)) - (len(right) / len(data)) * math.log2(
            len(right) / len(data))
    else:
        intrinsic = -sum((len(data[data[attribute] == value]) / len(data)) *
                         math.log2(len(data[data[attribute] == value]) / len(data))
                         for value in data[attribute].unique() if len(data[data[attribute] == value]) > 0)
    return (ig / intrinsic if intrinsic != 0 else 0), threshold


def build_tree(data, attributes, depth=0, max_depth=5):
    if len(data) == 0 or depth == max_depth:
        return {'class': data['Survived'].mode()[0] if len(data) > 0 else None, 'samples': len(data)}
    if len(data['Survived'].unique()) == 1:
        return {'class': data['Survived'].iloc[0], 'samples': len(data)}
    if len(attributes) == 0:
        return {'class': data['Survived'].mode()[0], 'samples': len(data)}

    best_attr = max(attributes, key=lambda attr: gain_ratio(data, attr)[0])
    gr, threshold = gain_ratio(data, best_attr)

    tree = {'attribute': best_attr, 'gain_ratio': gr, 'samples': len(data), 'branches': {}}

    if best_attr == 'Age':
        tree['threshold'] = threshold
        left = data[data[best_attr] <= threshold]
        right = data[data[best_attr] > threshold]
        tree['branches']['<=' + str(round(threshold, 2))] = build_tree(left, attributes, depth + 1, max_depth)
        tree['branches']['>' + str(round(threshold, 2))] = build_tree(right, attributes, depth + 1, max_depth)
    else:
        for value in data[best_attr].unique():
            subset = data[data[best_attr] == value]
            tree['branches'][value] = build_tree(subset, [attr for attr in attributes if attr != best_attr], depth + 1,
                                                 max_depth)

    return tree


def visualize_tree(tree, indent="", is_last=True):
    node_marker = "└── " if is_last else "├── "

    if 'attribute' in tree:
        print(f"{indent}{node_marker}{tree['attribute']} (GR: {tree['gain_ratio']:.2f}, samples: {tree['samples']})")
        if 'threshold' in tree:
            print(f"{indent}    threshold: {tree['threshold']:.2f}")

        next_indent = indent + ("    " if is_last else "│   ")
        branches = list(tree['branches'].items())

        for i, (value, subtree) in enumerate(branches):
            is_last_branch = (i == len(branches) - 1)
            print(f"{next_indent}│")
            print(f"{next_indent}{value}")
            visualize_tree(subtree, next_indent, is_last_branch)
    else:
        print(f"{indent}{node_marker}Class: {tree['class']} (samples: {tree['samples']})")


data = pd.read_csv('titanic-homework.csv')
data = data.drop(['PassengerId', 'Name'], axis=1)

print("\nSurvival Distribution:")
print(data['Survived'].value_counts(normalize=True))

print("\nAttribute Analysis:")
attributes = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch']
total_entropy = entropy(data)
print(f"Total entropy of the dataset: {total_entropy:.4f}")

for attr in attributes:
    ig, threshold = information_gain(data, attr)
    gr, _ = gain_ratio(data, attr)

    print(f"\nAttribute: {attr}")
    print(f"  Information Gain: {ig:.4f}")
    print(f"  Gain Ratio: {gr:.4f}")
    if threshold is not None:
        print(f"  Best split threshold: {threshold:.2f}")

best_attr = max(attributes, key=lambda x: gain_ratio(data, x)[0])
print(f"\nBest attribute for the root split: {best_attr}")
print(f"Gain Ratio: {gain_ratio(data, best_attr)[0]:.4f}")


tree = build_tree(data, attributes)
print("\nDecision Tree:")
visualize_tree(tree)