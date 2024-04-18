import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns


# def confusion_matrix_report(path_predictions, path_truth):
# 	predictions = pd.read_csv(path_predictions, header=None, names=['label'])
# 	truth = pd.read_csv(path_truth, header=None, names=['label'])


# 	label_mapping = {'Jedi': 0, 'Sith': 1}
# 	predictions_encoded = predictions['label'].map(label_mapping)
# 	truth_encoded = truth['label'].map(label_mapping)

# 	# Calcular la matriz de confusión
# 	conf_matrix = confusion_matrix(truth_encoded, predictions_encoded)

# 	# Calcular precision, recall y f1-score
# 	report = classification_report(truth_encoded, predictions_encoded, target_names=['0', '1'])

# 	# Imprimir el reporte
# 	print(report)
# 	print(conf_matrix)

# 	# Visualizar la matriz de confusión
# 	fig, ax = plt.subplots(figsize=(8, 6))
# 	sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', ax=ax, xticklabels=['0', '1'], yticklabels=['0', '1'])
# 	plt.title('Confusion Matrix')
# 	plt.ylabel('Actual')
# 	plt.xlabel('Predicted')
# 	plt.tight_layout()
# 	plt.savefig('test.png')
 
def confusion_matrix_manual(y_true, y_pred):
    """
    TP: True Positives
    FP: False Positives
    TN: True Negatives
    FN: False Negatives
    """
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    
    for true, pred in zip(y_true, y_pred):
        if true == 1 and pred == 1:
            TP += 1
        elif true == 0 and pred == 0:
            TN += 1
        elif true == 0 and pred == 1:
            FP += 1
        elif true == 1 and pred == 0:
            FN += 1
            
    return [[TN, FP], [FN, TP]]
 
def classification_report_manual(y_true, y_pred, target_names=None):
	"""
	TP: True Positives
	FP: False Positives
	FN: False Negatives
	precision: TP / (TP + FP)
	recall: TP / (TP + FN)
	f1-score: 2 * (precision * recall) / (precision + recall)
	support: number of occurrences of each class
	accuracy: (TP + TN) / (TP  + FP  + TN + FN)
	specifity: TN / (TN + FP) -- (is not in the sklearn classification_report function)
	macro avg: unweighted mean of precision, recall and f1-score
	weighted avg: weighted mean of precision, recall and f1-score
	"""
	labels = sorted(set(y_true))
	if target_names is None or len(target_names) != len(labels):
		target_names = [str(label) for label in labels]

	metrics = []
	for label, name in zip(labels, target_names):
		TP = sum((y_true == label) & (y_pred == label))
		FP = sum((y_true != label) & (y_pred == label))
		FN = sum((y_true == label) & (y_pred != label))
		
		precision = TP / (TP + FP) if TP + FP > 0 else 0
		recall = TP / (TP + FN) if TP + FN > 0 else 0
		f1_score = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
		support = sum(y_true == label)
		
		metrics.append({
			'label': name,
			'precision': precision,
			'recall': recall,
			'f1-score': f1_score,
			'support': support
		})

	df = pd.DataFrame(metrics)
	total_support = df['support'].sum()
	df.set_index('label', inplace=True)
    
	# Calculating averages
	accuracy = round(sum(y_true == y_pred) / len(y_true), 2)
	macro_avg = df[['precision', 'recall', 'f1-score']].mean().round(2)
	weighted_avg = (df[['precision', 'recall', 'f1-score']].multiply(df['support'], axis=0).sum() / total_support).round(2)

	macro_avg['support'] = total_support
	weighted_avg['support'] = total_support

	df.loc['accuracy'] = [accuracy] * 3 + [total_support]
	df.loc['macro avg'] = macro_avg
	df.loc['weighted avg'] = weighted_avg

	# Ajustar la configuración de visualización de Pandas
	pd.options.display.float_format = '{:,.2f}'.format
    # https://www.v7labs.com/blog/confusion-matrix-guide
	return df

def confusion_matrix_report2(path_predictions, path_truth):
	predictions = pd.read_csv(path_predictions, header=None, names=['label'])
	truth = pd.read_csv(path_truth, header=None, names=['label'])


	label_mapping = {'Jedi': 0, 'Sith': 1}
	predictions_encoded = predictions['label'].map(label_mapping)
	truth_encoded = truth['label'].map(label_mapping)

	# Calcular la matriz de confusión
	conf_matrix = confusion_matrix_manual(truth_encoded, predictions_encoded)

	# Calcular precision, recall y f1-score
	report = classification_report_manual(truth_encoded, predictions_encoded, target_names=['0', '1'])

	print(report)
	print(conf_matrix)

	# Visualizar la matriz de confusión
	fig, ax = plt.subplots(figsize=(10, 6))
	sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='viridis', ax=ax, xticklabels=['0', '1'], yticklabels=['0', '1'])
	plt.tight_layout()
	plt.savefig('test.png')
 

 
def main():
	path_predictions = '/vagrant/store/modulo04/predictions.txt'
	path_truth = '/vagrant/store/modulo04/truth.txt'
	# confusion_matrix_report(path_predictions, path_truth)
	confusion_matrix_report2(path_predictions, path_truth)

if __name__ == '__main__':
	main()
	