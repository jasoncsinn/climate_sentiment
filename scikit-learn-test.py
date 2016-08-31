from sklearn import datasets
from sklearn import svm

import pdb

iris = datasets.load_iris()
classifier = svm.SVC()
classifier.fit(iris.data[:-1], iris.target[:-1])
print(classifier.predict(iris.data[-1:]))
