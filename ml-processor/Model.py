import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score, matthews_corrcoef
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier 
import matplotlib.pyplot as plt

class Model:

    def __init__(self):
        #self.__decisionTree = DecisionTreeClassifier(max_depth=5)
        self.__KNN = KNeighborsClassifier(n_neighbors=5, weights='uniform')
        #self.__X_train, self.__X_test, self.__y_train, self.__y_test = self.split_data()  # Call split_data during initialization

    def split_data(self, X, y, test_size=0.30, random_state=42, shuffle=True):
        return train_test_split(X, y, test_size=test_size, random_state=random_state, shuffle=shuffle)
        
    def fit_model(self, X_train, y_train):
        self.__KNN = self.__KNN.fit(X_train, y_train)


    def predict(self, X_test):
        return self.__KNN.predict(X_test)

    def predict_X(self, data):
        return self.__KNN.predict(data)
    

    def evaluate_model(self, preds, X, y, y_test):
        scores = cross_val_score(self.__KNN, X, y, cv=5)
        avg_accuracy = accuracy_score(y_test, preds)
        avg_precision = precision_score(y_test, preds)
        avg_recall = recall_score(y_test, preds)
        avg_f1 = f1_score(y_test, preds)
        avg_mcc = matthews_corrcoef(y_test, preds)
        avg_conf_matrix = confusion_matrix(y_test, preds)
        return scores, avg_accuracy, avg_precision, avg_recall, avg_f1, avg_mcc, avg_conf_matrix


    def plot_scatter_matrix(self, X_train, y_train):
        dataframe = pd.DataFrame(X_train)
        pd.plotting.scatter_matrix(dataframe, c=y_train, figsize=(15, 15), marker='o', hist_kwds={'bins': 20}, s=60, alpha=.8)
        plt.show()

        