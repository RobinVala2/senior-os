import re
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
import sgive.src.CaregiverApp.configurationActions as ryuconf

logger = logging.getLogger(__file__)
logger.info("initiated logging")


class MachineLearning:
    def __init__(self):
        self.model = None
        self.vectorizer = None

    def machineLearning(self, language_option):
        path_to_csv = os.path.join(os.path.dirname(os.getcwd()), f"PhisingSiteURL/urldataset-{language_option}.csv")
        print(path_to_csv)

        self.model = LogisticRegression(max_iter=1000)
        self.vectorizer = TfidfVectorizer()
        generic = pd.read_csv(path_to_csv)
        generic = generic.rename(columns={'url': 'url', 'phish': 'threat'})
        generic.threat = generic.threat.replace({'True': 1, 'False': 0})

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

        print(threat_test.value_counts().iloc[0], threat_test.value_counts().iloc[1], "\n")

        print('True Negative (TN), False Positive (FP), False Negative {FN}, True Positive {TP}')

        print(dict(zip(['TN', 'FP', 'FN', 'TP'], cm_generic.ravel())))
        print('\nConfusion matrix')
        print('[TN FP]')
        print('[FN TP]')
        # cm_generic  # what this?

        # saving vectorizer and model
        timeStamp = datetime.now().strftime('%Y-%m-%d')
        pickle.dump(self.vectorizer, open(f"ML-saved/{timeStamp}_vectorizer_{language_option}", "wb"))
        pickle.dump(self.model, open(f"ML-saved/{timeStamp}_model_{language_option}", "wb"))

    @staticmethod
    def predictURL(model_file, vectorizer_file, URLarray):
        logging.info(f"Using Machine Learning model: {model_file}")
        try:
            with open(f"ML-saved/{vectorizer_file}", 'rb') as vf:
                vectorizer = pickle.load(vf)

            with open(f"ML-saved/{model_file}", 'rb') as mf:
                model = pickle.load(mf)

            feature = vectorizer.transform(URLarray)
            predict = model.predict(feature)

            whichUrlIsJudged = 0

            logging.info("Start of machine learning detection (looking through suspicious URLs for phishing)...")
            for finalJudgement in predict:  # 0 → OK, 1 → THREAT
                if finalJudgement == 0:
                    logging.info(f"URL[{URLarray[whichUrlIsJudged]}] isn't a threat. Marking as a False alarm.")
                else:
                    logging.warning(
                        f"URL[{URLarray[whichUrlIsJudged]}] IS possible threat, review recommended."
                    )
                whichUrlIsJudged += 1
            logging.info("End of machine learning detection...")

        except Exception as e:
            logging.error(f"An error occurred while loading model or vectorizer: {e}")


class ModelValidation:
    def __init__(self, URL):
        self.return_array = []
        self.URLthing = URL
        self.ML = MachineLearning()
        self.language = ryuconf.red_main_config("GlobalConfiguration", "language")
        # calls:
        self.MLdetection()

    def delete_and_retrain(self, filenames, language):
        folder_path = os.path.join(os.getcwd(), "ML-saved")

        for name in filenames:
            file_path = os.path.join(folder_path, name)
            if os.path.exists(file_path):
                os.remove(file_path)
                self.return_array = []
            else:
                self.return_array = []
                print("Already removed both files")
                self.model_and_vectorizer_check()
                return

        self.ML.machineLearning(language)
        self.model_and_vectorizer_check()

    def model_and_vectorizer_check(self):
        self.return_array = []
        num_of_languages = ryuconf.red_main_config("careConf", "LanguageOptions")
        list_dir = os.listdir("ML-saved")
        pattern_model = r'^\d{4}-\d{2}-\d{2}_model_[A-Z]{2}$'
        pattern_vecorizer = r'^\d{4}-\d{2}-\d{2}_vectorizer_[A-Z]{2}$'
        pattern_check_bool = False

        if len(list_dir) == 0:
            print("Training model for the first time (or the file got empty).")

        for filename in list_dir:
            if "model" in filename:
                match_model = re.match(pattern_model, filename)
                if not match_model and not pattern_check_bool:
                    pattern_check_bool = True
                    print("Name regex doesnt match up")
            elif "vectorizer" in filename:
                match_vectorizer = re.match(pattern_vecorizer, filename)
                if not match_vectorizer and not pattern_check_bool:
                    pattern_check_bool = True
                    print("Name regex doesnt match up")

        number_of_files = len(list_dir)
        # checking for any dotfiles, that i need to ignore :)
        for name in list_dir:
            if name.startswith('.'):
                number_of_files = int(number_of_files) - 1

        if number_of_files != len(num_of_languages) * 2 and not len(list_dir) == 0 or pattern_check_bool:
            folder_path = os.path.join(os.getcwd(), "ML-saved")
            for name in list_dir:
                if not name.startswith('.'):
                    file_path = os.path.join(folder_path, name)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    else:
                        print("couldn't remove")
            print("There are no Machine Learning files, or the files got corrupted. Generating new ones.")
            return None

        # Searching specific model and vectorizer, based on language.
        model_files = [f for f in os.listdir("ML-saved") if f.endswith(f"_{self.language}")]
        if model_files:
            for name in model_files:
                # checking, if model and vectorizer are older than 6 months
                time_check = name.split("_")
                date_object = datetime.strptime(time_check[0], '%Y-%m-%d').date()
                time_threshold = date.today() - relativedelta(months=6)  # 3 months threshold
                result = date_object < time_threshold
                if result:
                    print("Too old →", model_files)
                    self.delete_and_retrain(model_files, self.language)
                else:
                    self.return_array.append(name)

        return self.return_array

    def trainModels(self, language_options):
        for language in language_options:
            print(language)
            self.ML.machineLearning(language)  # training
        self.MLdetection()

    def MLdetection(self):
        # Check if ML-saved folder exists
        folder_path = os.path.join(os.getcwd(), "ML-saved")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            gitignore_path = os.path.join(folder_path, ".gitignore")
            # create gitignore
            with open(gitignore_path, 'w+') as f:
                f.write("*")

        # loading the files again
        get_names = self.model_and_vectorizer_check()
        model = None
        vectorizer = None

        # retrain if folder is empty:
        if not get_names:
            self.trainModels(["CZ", "EN", "DE"])
        elif get_names[0] is not None or get_names[1] is not None:
            # assign correct file to correct name
            for filename in get_names:
                if "model" in filename:
                    model = filename
                else:
                    vectorizer = filename
            self.ML.predictURL(model_file=model, vectorizer_file=vectorizer, URLarray=self.URLthing)  # prediction
        else:
            # don't know if this is needed, but making sure it at least tries to retrain the model if something random happens
            self.trainModels(["CZ", "EN", "DE"])


class ThreatDetection_ML:
    def __init__(self):
        self.URLs = []
        self.process_files()
        self.call_validation_of_ML()

    @staticmethod
    def get_path_to_log():
        current_dir = os.getcwd()
        path_parts = current_dir.split(os.sep)
        index = path_parts.index("senior-os")
        logs_path = os.path.join(os.sep.join(path_parts[:index + 1]), "sconf", "logs")
        return logs_path

    def filtering_log_files(self):
        logs_path = self.get_path_to_log()
        files = os.listdir(logs_path)
        filtered_files = [file for file in files if "ConfigurationApp.log" not in file and not file.startswith('.')]
        return filtered_files

    def process_files(self):
        filtered_files = self.filtering_log_files()
        for file in filtered_files:
            file_path = os.path.join(self.get_path_to_log(), file)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file2:
                # 'errors="ignore"' tells Python to skip characters that it cannot decode
                lines = file2.readlines()
                for line in lines:
                    if "WARNING" in line:
                        urls = re.findall(
                            r"https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(),]|%[0-9a-fA-F][0-9a-fA-F])+", line)
                        for url in urls:
                            self.URLs.append(url)

    def call_validation_of_ML(self):
        if self.URLs:  # aka, it array isn't empty
            ModelValidation(self.URLs)
        else:
            logging.warning(f"There is no URLs for Machine Learning validation, skipping ML check ...")
            return


# ↓ needed when executing only this .py thing alone ↓
if __name__ == '__main__':
    ThreatDetection_ML()

