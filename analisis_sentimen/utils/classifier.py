import pandas as pd
import numpy as np
import pickle
from django.contrib.staticfiles.storage import staticfiles_storage

class Classifier:
    # Default constructor
    def __init__(self, x_train, y_train):
        x = x_train
        y = [-1 if i == 'negatif' else 1 if i == 'positif' else 0 for i in y_train]
        # Load model
        self.model = open(staticfiles_storage.path('model.pickle'), 'rb')
        self.nbc_clf = pickle.load(self.model)
        self.clf = self.nbc_clf.fit(np.asarray(x), np.asarray(y))

    def predict(self, x_test):
        # Predik data tweet
        clf_value = self.clf.predict(x_test)
        return clf_value