import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_csv(file: str):
    try:
        df = pd.read_csv(file, index_col=None)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None

def histogram(df: pd.DataFrame):
    """
    n_cols: number of columns in the figure
    n_rows: number of rows in the figure
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
            n, bins, patches  = ax.hist(df[column], bins=40, color='green', alpha=0.5, label='Knight', rwidth=bin_width) #bins=40 para que se vea mejor
            
            # max_bin_height = max(n)  # Encuentra la altura del bin más alto
            # upper_limit = max_bin_height + (5 - (max_bin_height % 5))  # Redondea hacia arriba al múltiplo de 5 más cercano
            # ax.set_yticks(np.arange(0, upper_limit, 5)) # Establece los ticks del eje y
            # ax.set_yticklabels([str(int(y)) for y in np.arange(0, upper_limit, 5)]) # Establece las etiquetas de los ticks del eje y

            ax.set_title(column)
            ax.legend()
        
        # Oculta los ejes que no se utilizan (si alguno)
        for ax in axes[len(df.columns):]:
            ax.set_visible(False)

        plt.savefig("combined_histograms.png")  # Guarda la figura con todos los subgráficos
        plt.close(fig)  # Cierra la figura para liberar memoria
    except Exception as e:
        print(f"Error: {e}")

def main():
    df = load_csv("/vagrant/store/module03/Test_knight.csv")
    if df is None:
        return
    histogram(df)
if __name__ == "__main__":
    main()