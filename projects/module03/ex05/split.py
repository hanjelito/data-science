import pandas as pd
from sklearn.model_selection import train_test_split

def training_validation_split(df):
	train_df, validation_df = train_test_split(df, test_size=0.3, random_state=42)
	train_df.to_csv('Training_knight.csv', index=False)
	validation_df.to_csv('Validation_knight.csv', index=False)

def main():
	df = pd.read_csv('/vagrant/store/modulo03/Train_knight.csv')
	training_validation_split(df)
 
if __name__ == '__main__':
    main()