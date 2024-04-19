import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant

def calculate_variable_inflation_factors(features_with_constant):
    vif_values = []

    for i in range(1, features_with_constant.shape[1]):  # Comienza en 1 para saltar la constante
        vif = variance_inflation_factor(features_with_constant.values, i)
        vif_values.append(vif)

    vif_series = pd.Series(vif_values, index=features_with_constant.columns[1:])

    return vif_series

def remove_high_vif_features(df):
	"""
	add_constant: add a constant column to the dataframe
	"""
	print(df.head())
	df_const = add_constant(df)

	# Eliminar iterativamente las características con un VIF mayor a 5 
	while True:
		c_vifs = calculate_variable_inflation_factors(df_const)
		max_vif = c_vifs.max()
		if max_vif < 5:
			break
		remove_item = c_vifs.idxmax()
		df_const.drop(columns=[remove_item], inplace=True)
		print(f"Remove {remove_item} VIF={max_vif} tolerance={100/max_vif}")

	print("Remaining features and their VIFs:")
	print(calculate_variable_inflation_factors(df_const).to_string())

def main():
	df = pd.read_csv('Train_knight.csv')
	df = df.drop('knight', axis=1)
	remove_high_vif_features(df)

    

if __name__ == "__main__":
    main()