import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_csv(file: str):
    try:
        df = pd.read_csv(file, index_col=None)
        if df is None:
            return None
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def load_last_class_csv(file: str):
    try:
        df = pd.read_csv(file, index_col=None)
        if df is None:
            return None
        last_c = df.iloc[:, -1]
        return df, last_c
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def unique_columns(df: pd.DataFrame):
    valores_unicos = df.unique()
    mapeo = {valor: indice for indice, valor in enumerate(valores_unicos)}
    return mapeo


def histogram(df: pd.DataFrame):
    """
    n_cols: number of columns in the figure
    n_rows: number of rows in the figure
    bins: number of bins for the histogram
    """
    try:
        n_cols = 5
        n_rows = (len(df.columns) + 4) // n_cols
        fig_width=15
        fig_height=15
        bin_width=1

        # Crea una figura y un conjunto de subgráficos con 5 columnas
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(fig_width, fig_height), constrained_layout=True)


        # Aplanar la matriz de ejes para facilitar su iteración
        axes = axes.flatten()

        # Itera sobre cada columna y cada eje para crear un histograma
        for ax, column in zip(axes, df.columns):
            n, bins, patches  = ax.hist(df[column], bins=40, color='green', alpha=0.5, label='Knight', rwidth=bin_width)

            ax.set_title(column)
            ax.legend()
        
        # Oculta los ejes que no se utilizan (si alguno)
        for ax in axes[len(df.columns):]:
            ax.set_visible(False)

        plt.savefig("combined_histograms.png")  # Guarda la figura con todos los subgráficos
        plt.close(fig)  # Cierra la figura para liberar memoria
    except Exception as e:
        print(f"Error: {e}")

def histogram_tags(df: pd.DataFrame):
    """
    n_cols: number of columns in the figure
    n_rows: number of rows in the figure
    bins: number of bins for the histogram
    """
    try:
        n_cols = 5
        n_rows = (len(df.columns) + 4) // n_cols
        fig_width=15
        fig_height=15
        bin_width=1

        # Crea una figura y un conjunto de subgráficos con 5 columnas
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(fig_width, fig_height), constrained_layout=True)


        # Aplanar la matriz de ejes para facilitar su iteración
        axes = axes.flatten()

        # Itera sobre cada columna y cada eje para crear un histograma
        for ax, column in zip(axes, df.columns):
            n, bins, patches  = ax.hist(df[column], bins=40, color='green', alpha=0.5, label='Knight', rwidth=bin_width)

            ax.set_title(column)
            ax.legend()
        
        # Oculta los ejes que no se utilizan (si alguno)
        for ax in axes[len(df.columns):]:
            ax.set_visible(False)

        plt.savefig("combined_histograms.png")  # Guarda la figura con todos los subgráficos
        plt.close(fig)  # Cierra la figura para liberar memoria
    except Exception as e:
        print(f"Error: {e}")

# def histogram_jedi_sid(df: pd.DataFrame):

def main():
    df = load_csv("/vagrant/store/module03/Test_knight.csv")
    df2, df2_last = load_last_class_csv("/vagrant/store/module03/Train_knight.csv")
    if df is None or df2 is None:
        print("Wrong file")
        return
    df2_last = unique_columns(df2_last)
    histogram(df2)
    # category = divider_columns(df)
if __name__ == "__main__":
    main()