import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def load(path):
	df = pd.read_csv(path, index_col=None)
	return df

def process_pca(df):
    y = df['knight']
    X = df.drop(columns=['knight'])

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Fit the PCA model
    pca = PCA()
    pca.fit(X_scaled)
    print (f"Variances (Percentage):\n{pca.explained_variance_ratio_}\n")
    return pca

def variances(pca: PCA):
    cumulative_variances = np.cumsum(pca.explained_variance_ratio_ * 100)

    print(f"Cumulative Variances (Percentage):\n{cumulative_variances}")
    components_needed = np.argmax(cumulative_variances >= 90) + 1


    plt.figure(figsize=(10, 5))
    plt.plot(cumulative_variances, marker='o')
    plt.axhline(y=90, color='r', linestyle='-')
    plt.axvline(x=components_needed-1, color='g', linestyle='--')
    plt.text(components_needed-1, 90, f'  {components_needed} components', verticalalignment='bottom', color='g')
    plt.xlabel('Number of components')
    plt.ylabel('Explained variance (%)')
    plt.title('Cumulative Explained Variance by PCA Components')
    plt.grid(True)
    plt.savefig("variances.png")
    plt.show()
    plt.close()

def main():
	df = load('/vagrant/store/modulo04/Train_knight.csv')
    
	pca = process_pca(df)
	variances(pca)
    
if __name__ == '__main__':
    main()