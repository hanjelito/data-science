import pandas as pd
import numpy as np



def load(file: str):
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None
    
    
    
def create_correlation(df: pd.DataFrame):
    if df is not None:
        df_knight = df.copy()
        df_knight['knight'] = (df_knight['knight'] == 'Jedi').astype(int)
        numeric_cols = df_knight.select_dtypes(include=[np.number]).columns
        correlation_with_knight = df_knight[numeric_cols].corr()['knight'].sort_values(ascending=False)
        return correlation_with_knight
    else:
        print("El DataFrame está vacío o no se pudo cargar.")

df = load("/vagrant/store/modulo03/Train_knight.csv")
cor = create_correlation(df)
print(cor)