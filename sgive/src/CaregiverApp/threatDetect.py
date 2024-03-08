import pandas as pd
from pandas.api.types import is_integer_dtype
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import sgive.src.CaregiverApp.configurationActions as ryuconf
import humanize as hm
import re
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
        self.model = LogisticRegression(max_iter=10000)
        self.vectorizer = TfidfVectorizer()

    def machineLearning(self, model_language):
        generic = pd.read_csv(self.pathToCSV)
        generic = generic.rename(columns={'phish': 'threat'})
        generic.threat = generic.threat.replace({'True': 1, 'False': 0})
        language_ml = model_language

        print('Benign (0) URLs, Phishing URLs (1)')
        print(generic.threat.value_counts(), "\n")

        print('Norm Benign (0) URLs, Norm Phishing URLs (1)')
        print(generic.threat.value_counts(normalize=True).round(1))

        feature = self.vectorizer.fit_transform(generic.url)
        feature_train, feature_test, threat_train, threat_test = train_test_split(feature, generic.threat, random_state=0)

        print(f'Train URLs {feature_train.shape[0]} ({int(round(threat_train.shape[0] / len(generic), 2) * 100)}%)\n')
        print(f'Test URLs {feature_test.shape[0]} ({int(round(threat_test.shape[0] / len(generic), 2) * 100)}%)\n')

        print('Training the model ...')
        self.model.fit(feature_train, threat_train)

        threat_predicted = self.model.predict(feature_test)
        cm_generic = confusion_matrix(threat_test, threat_predicted)

        print('Negative (N) = benign URLs, Positive (P) = phishing URLs')
        print((threat_test == 0).sum(), (threat_test == 1).sum(), "\n")

        print('True Negative (TN), False Positive (FP), False Negative {FN}, True Positive {TP}')
        print(dict(zip(['TN', 'FP', 'FN', 'TP'], cm_generic.ravel())))
        print('\nConfusion matrix')
        print('[TN FP]')
        print('[FN TP]')

        timeStamp = datetime.now().strftime('%Y-%m-%d')
        pickle.dump(self.vectorizer, open(f"ML-saved/{timeStamp}_{language_ml}_vectorizer", "wb"))
        pickle.dump(self.model, open(f"ML-saved/{timeStamp}_{language_ml}_model", "wb"))

    @staticmethod
    def predictURL(model_file, vectorizer_file, URLarray):
        logging.info(f"Machine learning is using model: {model_file}.")

        path_to_dir = os.path.join(os.getcwd(), "ML-saved")
        fullpath_vectorizer = os.path.join(path_to_dir, vectorizer_file)
        fullpath_model = os.path.join(path_to_dir, model_file)

        with open(fullpath_vectorizer, 'rb') as vf:
            vectorizer = pickle.load(vf)

        with open(fullpath_model, 'rb') as mf:
            model = pickle.load(mf)

        if hasattr(vectorizer, "transform"):  # Check if vectorizer has transform method
            feature = vectorizer.transform(URLarray)
            predict = model.predict(feature)

            whichUrlIsJudged = 0
            for finalJudgement in predict:  # 0 → OK, 1 → THREAT
                if finalJudgement == 0:
                    logging.info(f"URL[{URLarray[whichUrlIsJudged]}] isn't threat. Marking as a False alarm.")
                else:
                    logging.warning(
                        f"URL[{URLarray[whichUrlIsJudged]}] is possible threat. Human based check is recommended.")
                whichUrlIsJudged += 1
        else:
            logging.error("Vectorizer does not have a transform method.")


class Main:
    def __init__(self, URL):
        self.URLthing = URL
        self.srcPath = os.path.dirname(os.getcwd())
        self.language = ryuconf.red_main_config("GlobalConfiguration", "language")
        self.fullPathToCsv = os.path.join(self.srcPath, f"PhisingSiteURL/urldataset-{self.language}.csv")
        self.ML = MachineLearning(self.fullPathToCsv)
        # call:
        self.ML_detection_call()

    def validate_ml_files(self):
        path_to_dir = os.path.join(os.getcwd(), "ML-saved")
        num_of_lang = ryuconf.red_main_config("careConf", "LanguageOptions")
        return_array = []

        if os.path.exists(path_to_dir):
            list_files = os.listdir(path_to_dir)
            expected_files = len(num_of_lang) * 2

            if len(list_files) != expected_files:
                logging.error("Not all Machine learning files are present or some are corrupted. Generating new ones.")
                self.regenerate_ml_files(path_to_dir)
                return []

            lang_files = [file for file in list_files if self.language in file]
            if len(lang_files) != 2:
                logging.error(f"Not all required Machine learning files for language {self.language} are present. Generating new ones.")
                self.regenerate_ml_files(path_to_dir)
                return []

            for filename in lang_files:
                if not re.match(r"\d{4}-\d{2}-\d{2}_\w{2}_.+", filename):
                    logging.error(f"Invalid file name detected: {filename}. Regenerating files.")
                    self.regenerate_ml_files(path_to_dir)
                    return []

                file_parts = filename.split('_')
                date_ML = file_parts[0]
                type_ML = file_parts[2]

                date_object = datetime.strptime(date_ML, '%Y-%m-%d').date()
                time_threshold = date.today() - relativedelta(months=3)  # 3 months threshold

                if date_object < time_threshold:
                    logging.warning(f"{type_ML} is older than three months. Retraining specific language Machine Learning model")
                    self.remove_ml_files(path_to_dir, self.language)
                    return None
                else:
                    return_array.append(filename)

        return return_array

    @staticmethod
    def regenerate_ml_files(directory):
        files = os.listdir(directory)
        for file in files:
            file_path = os.path.join(directory, file)
            os.remove(file_path)

    @staticmethod
    def remove_ml_files(directory, language):
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if language in file:
                os.remove(file_path)

    def retrain_ml_for_all_languages(self):
        language_num = ryuconf.red_main_config("careConf", "LanguageOptions")
        language_mapping = {
            "Czech": "CZ",
            "English": "EN",
            "German": "DE"
        }

        for language in language_num:
            full_language_name = language_mapping.get(language, language)
            self.ML.machineLearning(full_language_name)

        get_names = self.validate_ml_files()
        self.ML.predictURL(get_names[0], get_names[1], self.URLthing)

    def ML_detection_call(self):
        get_names = self.validate_ml_files()
        if get_names is None:
            self.ML.machineLearning(self.language)
            get_names_reroll = self.validate_ml_files()
            self.ML.predictURL(get_names_reroll[0], get_names_reroll[1], self.URLthing)
        elif not get_names:
            self.retrain_ml_for_all_languages()
        elif len(get_names) == 2:
            self.ML.predictURL(get_names[0], get_names[1], self.URLthing)


    # ↓ needed when executing only this .py thing alone ↓
if __name__ == '__main__':
    possibleThreatURLs = ['https://xhamster.com/', 'https://www.youtube.com/']
    obj = Main(possibleThreatURLs)
