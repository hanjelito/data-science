import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def ensure_knight_column(df):
    if 'knight' not in df.columns:
        df['knight'] = 'knight'

def set_style(ax, legend_loc):
    ax.set_xlabel(ax.get_xlabel(), fontsize=14)
    ax.set_ylabel(ax.get_ylabel(), fontsize=14)
    ax.tick_params(labelsize=14)
    ax.legend(title='', loc=legend_loc)

def plot_scatter(df, x, y, ax, palette_colors, legend_loc):
    sns.scatterplot(data=df, x=x, y=y, hue='knight', palette=palette_colors, alpha=0.5, ax=ax, s=70)
    set_style(ax, legend_loc)

def standardize(df):
    # Comprobar si la columna 'knight' existe en el DataFrame
    if 'knight' in df.columns:
        # Separar las características y la variable de etiquetas
        X = df.drop('knight', axis=1)
        y = df['knight']
    else:
        X = df  # Si no existe la columna 'knight', usar todo el df como X
    
    # StandardScaler es una clase de Scikit-learn que estandariza las columnas de un DataFrame
    scaler = StandardScaler()
    # fit_transform() estandariza las columnas seleccionadas
    X_scaled = scaler.fit_transform(X)
    # Convertir de nuevo a DataFrame para mejor visualización con las columnas originales
    df_scaled = pd.DataFrame(X_scaled, columns=X.columns)
    df_scaled = df_scaled.round(2)
    
    # Reincorporar la columna 'knight' si existe
    if 'knight' in df.columns:
        df_scaled['knight'] = y
    
    return df_scaled

def configure_plots(df1, df2, filename):
    ensure_knight_column(df1)
    ensure_knight_column(df2)


    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    palette_colors = {'Sith': 'red', 'Jedi': 'blue', 'knight': 'green'}

    plots = [
        (df1, 'Repulse', 'Agility', axes[0, 0], 'upper left'),
        (df1, 'Dexterity', 'Power', axes[0, 1], 'upper right'),
        (df2, 'Repulse', 'Agility', axes[1, 0], 'upper left'),
        (df2, 'Dexterity', 'Power', axes[1, 1], 'upper right')
    ]

    for df, x, y, ax, legend_loc in plots:
        plot_scatter(df, x, y, ax, palette_colors, legend_loc)

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()



def main():
    df = pd.read_csv('/vagrant/store/modulo03/Train_knight.csv')
    df2 = pd.read_csv('/vagrant/store/modulo03/Test_knight.csv')
    df_st = standardize(df)
    df2_st = standardize(df2)
    print(df2.head(2))
    print(df2_st.head(2))
    configure_plots(df_st, df2_st, "clusters_standardization.png")

if "__main__" == __name__:
    main()