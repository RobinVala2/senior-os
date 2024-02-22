import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import humanize as hm
import os
import pickle
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import logging

logger = logging.getLogger(__file__)
logger.info("initiated logging")


class MachineLearning:
    def __init__(self, pathToCSV):
        self.pathToCSV = pathToCSV
        # phishing detection model
        self.model = LogisticRegression(max_iter=4000)
        self.vectorizer = TfidfVectorizer()

    def machineLearning(self):
        generic = pd.read_csv(self.pathToCSV)
        generic = generic.rename(columns={'URL': 'url', 'Label': 'threat'})
        generic.threat = generic.threat.replace({'bad': 1, 'good': 0})

        # show numbers for benign and phishing URLs
        print('Benign (0) URLs, Phishing URLs (1)')

        print(generic.threat.value_counts().apply(hm.metric), "\n")

        print('Norm Benign (0) URLs, Norm Phishing URLs (1)')
        print(generic.threat.value_counts(normalize=True).round(1))
        feature = self.vectorizer.fit_transform(generic.url)
        feature_train, feature_test, threat_train, threat_test = train_test_split(feature, generic.threat,
                                                                                  random_state=0)
        print(
            f'Train URLs {hm.metric(feature_train.shape[0])} ({int(round(threat_train.shape[0] / len(generic), 2) * 100)}%)\n')

        print(
            f'Test URLs {hm.metric(feature_test.shape[0])} ({int(round(threat_test.shape[0] / len(generic), 2) * 100)}%)\n')

        # train model
        print('Training the model ...')
        self.model.fit(feature_train, threat_train)

        # predict phishing
        threat_predicted = self.model.predict(feature_test)

        cm_generic = confusion_matrix(threat_test, threat_predicted)

        print('Negative (N) = benign URLs, Positive (P) = phishing URLs')

        print(threat_test.value_counts()[0], threat_test.value_counts()[1], "\n")

        print('True Negative (TN), False Positive (FP), False Negative {FN}, True Positive {TP}')

        print(dict(zip(['TN', 'FP', 'FN', 'TP'], cm_generic.ravel())))
        print('\nConfusion matrix')
        print('[TN FP]')
        print('[FN TP]')
        # cm_generic  # what this?

        # saving vectorizer and model
        timeStamp = datetime.now().strftime('%Y-%m-%d')
        pickle.dump(self.vectorizer, open(f"ML-saved/{timeStamp}_vectorizer", "wb"))
        pickle.dump(self.model, open(f"ML-saved/{timeStamp}_model", "wb"))

    @staticmethod
    def predictURL(model, vectorizer, URLarray):
        print("-- detection --")
        vectorizer = pickle.load(open(f"ML-saved/{vectorizer}", "rb"))
        model = pickle.load(open(f"ML-saved/{model}", "rb"))

        feature = vectorizer.transform(URLarray)
        predict = model.predict(feature)

        whichUrlIsJudged = 0
        for finalJudgement in predict:  # 0 → OK, 1 → THREAT
            if finalJudgement == 0:
                logging.info(f"URL[{URLarray[whichUrlIsJudged]}] isn't threat. Marking as a False alarm.")
            else:
                logging.warning(f"URL[{URLarray[whichUrlIsJudged]}] is possible threat. Human based check is recommended.")
            whichUrlIsJudged += 1


class Main:
    def __init__(self, URL):
        self.URLthing = URL
        self.srcPath = os.path.dirname(os.getcwd())
        self.fullPathToCsv = os.path.join(self.srcPath, "PhisingSiteURL/phishing_site_urls.csv")
        self.ML = MachineLearning(self.fullPathToCsv)
        # modules:
        self.validateML()

    @staticmethod
    def getSavedNames():
        # todo: check že existují obě složky
        pathToDir = os.path.join(os.getcwd(), "ML-saved")
        listFiles = os.listdir(pathToDir)
        if os.path.exists(pathToDir) and not len(listFiles) == 0:
            firstSplit = listFiles[0].split("_")
            if firstSplit[1] == "model":
                model = listFiles[0]
                vectorizer = listFiles[1]
            else:
                vectorizer = listFiles[0]
                model = listFiles[1]
            return vectorizer, model

    def validateML(self):  # check if model and vectorizer are up-to-date (max. 3 months old)
        pathToDir = os.path.join(os.getcwd(), "ML-saved")
        listFiles = os.listdir(pathToDir)

        # if there is no model or vectorizer files present, training the model:
        if len(listFiles) == 0:
            print("There is no ML files in system, training ML model...")
            self.MLdetection()
            return

        time_model = listFiles[0].split("_")
        date_object = datetime.strptime(time_model[0], '%Y-%m-%d').date()
        time_threshold = date.today() - relativedelta(months=3)  # 3 months threshold
        result = date_object < time_threshold

        if not result:  # aka its false (model isn't older than 3 months)
            print("there is no need to train model again!")
            self.MLdetection()
        else:   # aka its true (model is older than 3 months)
            print("Model and vectorizer will be trained again!")
            os.remove(os.path.join(pathToDir, listFiles[0]))  # delete old vectorizer
            os.remove(os.path.join(pathToDir, listFiles[1]))  # delete old model
            self.MLdetection()
        return result

    def MLdetection(self):
        get_names = self.getSavedNames()  # loading the files again
        # get_names[1] → MODEL
        # get_names[0] → vectorizer
        if not get_names is None:
            self.ML.predictURL(get_names[1], get_names[0], self.URLthing)  # prediction
        # when there is no model or vectorizer in OS
        else:
            self.ML.machineLearning()  # training
            getNamesV2 = self.getSavedNames()  # need to check of file names again
            self.ML.predictURL(getNamesV2[1], getNamesV2[0], self.URLthing)  # prediction


# ↓ needed when executing only this .py thing alone ↓
if __name__ == '__main__':
    possibleThreatURLs = ['https://www.google.com/', 'https://www.youtube.com/']
    obj = Main(possibleThreatURLs)
