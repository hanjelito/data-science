import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

# Cargar los datos
train_data = pd.read_csv('/vagrant/store/modulo04/Train_knight.csv')
test_data = pd.read_csv('/vagrant/store/modulo04/Test_knight.csv')

# Preparar los datos de entrenamiento y prueba
X_train = train_data.drop('knight', axis=1)
y_train = train_data['knight']
X_test = test_data

# model examples 04 and 05
model1 = DecisionTreeClassifier(random_state=42)
model2 = KNeighborsClassifier(n_neighbors=5)
model3 = SVC(probability=True, random_state=42)

# configurate the voting classifier whit trhe models
# estimators user to pass the models to the voting classifier
# voting='soft' use probabilities best results
# dt = DecisionTreeClassifier
voting_clf = VotingClassifier(estimators=[('dt', model1), ('knn', model2), ('svc', model3)], voting='soft')


X_train_split, X_val_split, y_train_split, y_val_split = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Train the voting classifier
voting_clf.fit(X_train_split, y_train_split)

# make predictions on the validation set
y_pred_val = voting_clf.predict(X_val_split)
# Calculate the F1 Score
f1 = f1_score(y_val_split, y_pred_val, average='macro')
print(f'F1 Score: {f1}')


# Comprobar si el F1 Score es al menos 0.94
if f1 < 0.94:
    print('El F1 Score en el conjunto de validación es menor que 0.94, necesitas mejorar el modelo.')
else:
    #attachment the model to the training data and create predictions for the test data
    voting_clf = voting_clf.fit(X_train, y_train)
    
    #create predictions for the test data
    predictions_test = voting_clf.predict(X_test)
    
    with open('Voting.txt', 'w') as f:
        for pred in predictions_test:
            f.write(f'{pred}\n')

    print('Predicciones guardadas en Voting.txt')
