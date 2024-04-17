import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

    
def load(file: str):
    try:
        df = pd.read_csv(file, index_col=None)
        verify_attributes = 'knight'
        if verify_attributes not in df.columns:
            df['knight'] = 'knight'
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None

def histogram(df: pd.DataFrame, name: str):
    try:
        categoria = df.iloc[:, -1]
        df_reduced = df.iloc[:, :-1]
        
        n_cols = 5
        n_rows = (len(df_reduced.columns) + 4) // n_cols
        fig_width=15
        fig_height=15
        bin_width=1
        color_map = {
            'Sith': 'red',
            'Jedi': 'blue',
            'knight': 'green'
        }
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(fig_width, fig_height), constrained_layout=True)
        axes = axes.flatten()
        

        for i, feature in enumerate(df_reduced.columns):
            ax = axes[i]
            for key in categoria.unique():
                mask = categoria == key
                ax.hist(df_reduced.loc[mask, feature], bins=40, alpha=0.5, label=str(key), color=color_map[key], rwidth=bin_width)
                ax.set_title(feature)
                ax.legend()
        
        # Ocultar ejes no utilizados
        for j in range(i+1, len(axes)):
            axes[j].set_visible(False)

        plt.savefig(f"histograms_{name}.png")
        plt.close(fig)
    except Exception as e:
        print(f"Error: {e}")

def main():
    df = load("/vagrant/store/module03/Test_knight.csv")
    df2 = load("/vagrant/store/module03/Train_knight.csv")
    histogram(df, "knight")
    histogram(df2, "jedai_sith")

if __name__ == "__main__":
    main()