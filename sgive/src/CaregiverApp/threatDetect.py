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

    def predictURL(self, model, vectorizer):
        print("-- detection --")
        url = ["https://www.google.com/"]
        vectorizer = pickle.load(open(f"ML-saved/{vectorizer}", "rb"))
        model = pickle.load(open(f"ML-saved/{model}", "rb"))
        feature = vectorizer.transform(url)
        predict = model.predict(feature)
        if predict == 1:
            print(f"\n{url} is possible threat")
        else:
            print("\nwe chillin")


def getSavedNames():
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

def checkForDate():
    pathToDir = os.path.join(os.getcwd(), "ML-saved")
    listFiles = os.listdir(pathToDir)
    if len(listFiles) == 0:
        return
    timeModel = listFiles[0].split("_")
    dateObj = datetime.strptime(timeModel[0], '%Y-%m-%d').date()
    timeTreshold = date.today() - relativedelta(months=6)
    finalJudgement = dateObj < timeTreshold
    if not finalJudgement:
        print("there is no need to train model again!")
    return finalJudgement

if __name__ == '__main__':
    checkForDate()
    model = None
    vectorizer = None
    srcPath = os.path.dirname(os.getcwd())
    fullPathToCsv = os.path.join(srcPath, "PhisingSiteURL/phishing_site_urls.csv")
    ML = MLdetectionOfSusURL(fullPathToCsv)

    gimmeNames = getSavedNames()
    if not gimmeNames is None:
        model = gimmeNames[1]  # load saved model
        vectorizer = gimmeNames[0]  # load saved vectorizer

    if os.path.isfile(fullPathToCsv):
        inpt = input("Wanna train dataset again? [y/N]")
        if inpt == "y" or inpt == "Y":
            ML.machineLearning() # traing the model
            if model is None or vectorizer is None:
                gimmeNames = getSavedNames()
                if not gimmeNames is None:
                    model = gimmeNames[1]  # load saved model
                    vectorizer = gimmeNames[0]  # load saved vectorizer
            ML.predictURL(model=model, vectorizer=vectorizer)
        else:
            ML.predictURL(model=model, vectorizer=vectorizer)
    else:
        exit(404)
