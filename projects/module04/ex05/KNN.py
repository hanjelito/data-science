import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt


# K-Nearest Neighbors

train_data = pd.read_csv('Training_knight.csv')
test_data = pd.read_csv('Validation_knight.csv')

X_train = train_data.drop('knight', axis=1)
y_train = train_data['knight']

if 'knight' in test_data.columns:
    X_test = test_data.drop('knight', axis=1)
else:
    X_test = test_data

# Split the data into train and validation
X_train_split, X_val_split, y_train_split, y_val_split = train_test_split(
    X_train, y_train, test_size=0.2, random_state=42)

#initialize variables to store the best k and the best f1 score
f1_scores = []
k_values = range(1, 50)
best_f1_score = 0
best_k = 0

# iterate over k values
for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train_split, y_train_split)
    preds = knn.predict(X_val_split)
    f1 = f1_score(y_val_split, preds, average='macro')
    f1_scores.append(f1)
    if f1 > best_f1_score:
        best_f1_score = f1
        best_k = k
    print(f'k = {k}, F1 Score = {f1:.2f}')

#verify if the best f1 score is greater than 0.92
if best_f1_score < 0.92:
    print(f'Advertencia: El mejor F1 Score encontrado es {best_f1_score:.2f}, que es menor que 0.92. Mejoras necesarias.')
else:
    print(f'El mejor k es {best_k} con un F1 Score de {best_f1_score:.2f}')

    # train the model with the best k
    best_knn = KNeighborsClassifier(n_neighbors=best_k)
    best_knn.fit(X_train, y_train)
    
    # prediction in test data
    predictions_test = best_knn.predict(X_test)
    
    # savae predictions to file
    with open('KNN.txt', 'w') as f:
        for pred in predictions_test:
            f.write(pred + '\n')


plt.plot(k_values, f1_scores, marker='o')
plt.xlabel('k values')
plt.ylabel('Accuracy')
plt.title('F1 Score in function of k values')
plt.savefig('k_values_vs_f1.png')
plt.close()