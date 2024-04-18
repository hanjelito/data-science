import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def heatmap(conf_matrix, filename):
	fig, ax = plt.subplots(figsize=(8, 6))
	sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', ax=ax, xticklabels=['0', '1'], yticklabels=['0', '1'])
	plt.title('Confusion Matrix')
	plt.ylabel('Actual')
	plt.xlabel('Predicted')
	plt.tight_layout()
	plt.tight_layout()
	plt.savefig(filename)
	plt.close()
 

def main():
	Test_knight = '/vagrant/store/modulo04/Test_knight.csv'
	Train_knight = '/vagrant/store/modulo04/Train_knight.csv'
	# confusion_matrix_report(path_predictions, path_truth)
	heatmap(Test_knight, 'test.png')

if __name__ == '__main__':
	main()