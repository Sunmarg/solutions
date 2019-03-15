
# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('trainingset.csv')
df=dataset

df=df.drop('Hillshade_9am',axis=1)
X = df.iloc[:,1:-1] .values
y = df.iloc[:, -1].values

# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Fitting Naive Bayes to the Training set
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 110, criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)



# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

from matplotlib.colors import ListedColormap
X_set, y_set = X_train, y_train

for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('red', 'green'))(i), label = j)
plt.title('Random Forest(Training set)')
plt.xlabel('Elevation')
plt.ylabel('Aspect')
plt.legend()
plt.show()

dft=pd.read_csv('testset.csv')
dft=dft.drop('Hillshade_9am',axis=1)
Xt = dft.iloc[:,1:-1] .values


# Splitting the dataset into the Training set and Test set
#from sklearn.cross_validation import train_test_split
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
Xt = sc.fit_transform(Xt)


# Fitting Naive Bayes to the Training set
#from sklearn.ensemble import RandomForestClassifier
#classifier = RandomForestClassifier(n_estimators = 110, criterion = 'entropy', random_state = 0)
#classifier.fit(X_train, y_train)



# Predicting the Test set results
y_predt = classifier.predict(Xt)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_trainn = sc.fit_transform(X)
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 110, criterion = 'entropy', random_state = 0)
classifier.fit(X_trainn, y)
y_predtn = classifier.predict_proba(Xt)
y_predt1=classifier.predict(Xt)
#predtn is final answer


for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('red', 'green'))(i), label = j)
plt.title('Random Forest(Training set)')
plt.xlabel('Elevation')
plt.ylabel('Aspect')
plt.legend()
plt.show()
