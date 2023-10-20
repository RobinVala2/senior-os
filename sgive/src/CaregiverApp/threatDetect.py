import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import humanize as hm
import os
import re

class MLdetectionOfSusURL:
    def __init__(self):
        srcPath = os.path.dirname(os.getcwd())
        self.fullPathToCsv = os.path.join(srcPath, "PhisingSiteURL/phishing_site_urls.csv")
        self.generic = None
        self.vectorizer = None
        self.feature = None
        if os.path.isfile(self.fullPathToCsv):
           self.genericData()
           self.training()
           self.predictURL()
        else:
            return

    def genericData(self):
        self.generic = pd.read_csv(self.fullPathToCsv)
        self.generic = self.generic.rename(columns = {'URL':'url','Label':'threat'})
        self.generic.threat = self.generic.threat.replace({'bad':1,'good':0})

        # show numbers for benign and phishing URLs
        print('Benign (0) URLs, Phishing URLs (1)')

        print(self.generic.threat.value_counts().apply(hm.metric),"\n")

        print('Norm Benign (0) URLs, Norm Phishing URLs (1)')
        print(self.generic.threat.value_counts(normalize=True).round(2))
    def training(self):
        self.vectorizer = TfidfVectorizer()
        self.feature = self.vectorizer.fit_transform(self.generic.url)
        self.feature_train, self.feature_test, self.threat_train, self.threat_test = train_test_split(self.feature, self.generic.threat,
                                                                                  random_state=0)
        print(
            f'Train URLs {hm.metric(self.feature_train.shape[0])} ({int(round(self.threat_train.shape[0] / len(self.generic), 2) * 100)}%)\n')

        print(f'Test URLs {hm.metric(self.feature_test.shape[0])} ({int(round(self.threat_test.shape[0] / len(self.generic), 2) * 100)}%)\n')

        # phishing detection model
        self.model = LogisticRegression(max_iter=1000)

        # train model
        print('Training the model ...')
        self.model.fit(self.feature_train, self.threat_train)

        # predict phishing
        threat_predicted = self.model.predict(self.feature_test)

        cm_generic = confusion_matrix(self.threat_test, threat_predicted)

        print('Negative (N) = benign URLs, Positive (P) = phishing URLs')

        print(self.threat_test.value_counts()[0], self.threat_test.value_counts()[1]);
        print()

        print('True Negative (TN), False Positive (FP), False Negative {FN}, True Positive {TP}')

        print(dict(zip(['TN', 'FP', 'FN', 'TP'], cm_generic.ravel())))
        print('\nConfusion matrix')
        print('[TN FP]')
        print('[FN TP]')
        cm_generic
    def predictURL(self):
        print("-----pokus section-----")




if __name__ == '__main__':
    MLdetectionOfSusURL()



