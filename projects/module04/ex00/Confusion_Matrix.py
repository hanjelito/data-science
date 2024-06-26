import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns


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
	y_true = y_true.tolist() if isinstance(y_true, pd.Series) else y_true
	y_pred = y_pred.tolist() if isinstance(y_pred, pd.Series) else y_pred

	labels = sorted(set(y_true))
	if target_names is None or len(target_names) != len(labels):
		target_names = [str(label) for label in labels]

	metrics = []
	for label, name in zip(labels, target_names):
		TP = sum(1 for t, p in zip(y_true, y_pred) if t == label and p == label)
		FP = sum(1 for t, p in zip(y_true, y_pred) if t != label and p == label)
		FN = sum(1 for t, p in zip(y_true, y_pred) if t == label and p != label)

		precision = TP / (TP + FP) if TP + FP > 0 else 0
		recall = TP / (TP + FN) if TP + FN > 0 else 0
		f1_score = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
		total = sum(1 for t in y_true if t == label)

		metrics.append({
			'label': name,
			'precision': precision,
			'recall': recall,
			'f1-score': f1_score,
			'total': total
		})

	df = pd.DataFrame(metrics)
	total_support = df['total'].sum()
	df.set_index('label', inplace=True)

	accuracy = round(sum(t == p for t, p in zip(y_true, y_pred)) / len(y_true), 2)
	df.loc['accuracy'] =  '', '', accuracy, total_support

	pd.options.display.float_format = '{:,.2f}'.format

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
	report = classification_report_manual(truth_encoded, predictions_encoded, target_names=['Jedi', 'Sith'])

	# Imprimir el reporte
	print(report)
	print(conf_matrix)

	# Visualizar la matriz de confusión
	fig, ax = plt.subplots(figsize=(10, 6))
	sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='viridis', ax=ax, xticklabels=['0', '1'], yticklabels=['0', '1'])
	plt.tight_layout()
	plt.savefig('confusion_matrix_report.png')
	plt.close()
 
def main():
	path_predictions = 'Tree.txt'
	path_truth = 'truth.txt'
	confusion_matrix_report2(path_predictions, path_truth)

if __name__ == '__main__':
	main()
