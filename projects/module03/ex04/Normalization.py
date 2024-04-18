import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

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

def normalize(df):
    """
    Normaliza los datos de un DataFrame.
    X_normalized = (X - X.min()) / (X.max() - X.min()) 
    """
    if 'knight' in df.columns:
        X = df.drop('knight', axis=1)
        y = df['knight']
    else:
        X = df

    scaler = MinMaxScaler()
    X_normalized = scaler.fit_transform(X)
    df_normalized = pd.DataFrame(X_normalized, columns=X.columns)
    df_normalized = df_normalized.round(2)
    
    # Reincorporar la columna 'knight' si existe
    if 'knight' in df.columns:
        df_normalized['knight'] = y
    
    return df_normalized

def configure_plots(df1, df2, filename):
    ensure_knight_column(df1)
    ensure_knight_column(df2)


    fig, axes = plt.subplots(2, 2, figsize=(10, 12))
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
    df_st = normalize(df)
    df2_st = normalize(df2)
    print(df2.head(2))
    print(df2_st.head(2))
    configure_plots(df_st, df2_st, "clusters_normalization.png")

if "__main__" == __name__:
    main()