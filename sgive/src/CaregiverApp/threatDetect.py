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


class MLdetectionOfSusURL:
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

    def predictURL(self,model, vectorizer, url):
        print("-- detection --")
        vectorizer = pickle.load(open(f"ML-saved/{vectorizer}", "rb"))
        model = pickle.load(open(f"ML-saved/{model}", "rb"))
        feature = vectorizer.transform(url)
        predict = model.predict(feature)
        if predict == 1:
            print(f"\n{url} is possible threat...")
            logging.critical(f"{url} is possible threat... please check for sus activities.")
        else:
            print(f"\n{url} is OK i think...")
            logging.info(f"{url} that was flagged as threat was false alarm.")


class main:
    def __init__(self, URL):
        self.URLthing = [URL]
        self.srcPath = os.path.dirname(os.getcwd())
        self.fullPathToCsv = os.path.join(self.srcPath, "PhisingSiteURL/phishing_site_urls.csv")
        self.ML = MLdetectionOfSusURL(self.fullPathToCsv)   # call pro classu s ML akcema
        # modules:
        self.CheckingAgeOfML()

    def getSavedNames(self):
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

    def CheckingAgeOfML(self):
        pathToDir = os.path.join(os.getcwd(), "ML-saved")
        listFiles = os.listdir(pathToDir)

        # if there is no model or vectorizer files pressent, traing the model:
        if len(listFiles) == 0:
            print("There is no ML files in system, training ML model...")
            self.MLdetection()
            return

        timeModel = listFiles[0].split("_")
        dateObj = datetime.strptime(timeModel[0], '%Y-%m-%d').date()
        timeTreshold = date.today() - relativedelta(months=3)  # 3 months threshold
        finalJudgement = dateObj < timeTreshold

        # if the model and vectorizer aint that old:
        if not finalJudgement:
            print("there is no need to train model again!")
            self.MLdetection()

        # bro that shit old af, training again
        else:
            print("ML will be trained again!")
            os.remove(os.path.join(pathToDir, listFiles[0]))  # delete old vectorizer
            os.remove(os.path.join(pathToDir, listFiles[1]))  # delete old model
            self.MLdetection()
        return finalJudgement

    def MLdetection(self):
        getNames = self.getSavedNames()  # loading the files again
        # getNames[1] → MODEL
        # getNames[0] → vectorizer
        if not getNames is None:
            self.ML.predictURL(getNames[1], getNames[0], self.URLthing)  # prediction
        # when there is no model or vectorizer in OS
        else:
            self.ML.machineLearning()  # training
            getNamesV2 = self.getSavedNames()  # need to check of file names again
            self.ML.predictURL(getNamesV2[1], getNamesV2[0], self.URLthing)  # prediction



if __name__ == '__main__':
    obj = main('https://www.google.cz/?hl=cs')