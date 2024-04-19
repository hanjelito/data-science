import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier

# Cargar los datos
train_data = pd.read_csv('Train_knight.csv')
test_data = pd.read_csv('Test_knight.csv')

X_train = train_data.drop('knight', axis=1)
y_train = train_data['knight']
X_test = test_data


clf = DecisionTreeClassifier(random_state=42)
clf = clf.fit(X_train, y_train)


predictions_train = clf.predict(X_train)
predictions_test = clf.predict(X_test)


f1 = f1_score(y_train, predictions_train, average='macro')
print(f'F1 Score: {f1}')


if f1 < 0.9:
    print('F1 Score es menor que 0.9, necesitas mejorar el modelo.')


fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(20, 10), dpi=300)
tree.plot_tree(clf, feature_names=X_train.columns, class_names=['Jedi', 'Sith'], filled=True, ax=axes)

# Guardar la figura
plt.savefig('decision_tree.png')

# Guardar las predicciones en un archivo
with open('predictions_04.txt', 'w') as f:
    for pred in predictions_test:
        f.write("%s\n" % pred)
