import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns


def load_file(path):
    df = pd.read_csv(path, index_col=None)
    return df

def heatmap(df: pd.DataFrame):
    if 'knight' in df.columns:
        df['knight'] = df['knight'].map({'Jedi': 0, 'Sith': 1})
    
    
    correlation_matrix = df.corr()
    # print(correlation_matrix)

    # plt.figure(figsize=(20, 17))
    # sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.figure(figsize=(10, 7))
    sns.heatmap(correlation_matrix)
    plt.savefig("heatmap.png")
    plt.close()

def main():
    train_knight = '/vagrant/store/modulo04/Train_knight.csv'
    df = load_file(train_knight)
    heatmap(df)

if __name__ == '__main__':
    main()
