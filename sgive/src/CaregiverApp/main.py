import configurationActions as ryuconf
import os
from sgive.src.CaregiverApp import FrontEnd
from sgive.src.CaregiverApp import threatDetect
import logging
import datetime

_log_directory = ryuconf.get_log()
_log_file = os.path.join(_log_directory, 'ConfigurationApp.log')

# Last time update check
if os.path.exists(_log_file):
    last_change_time = datetime.datetime.fromtimestamp(os.path.getmtime(_log_file))
    current_date = datetime.datetime.now().date()

    # Time validation (if older than a day, delete it)
    if last_change_time.date() != current_date:
        try:
            os.remove(_log_file)
        except OSError:
            pass  # There is nothing we can do

logging.basicConfig(
    filename=_log_file,
    level=logging.INFO,
    format="%(asctime)s : %(module)s %(levelname)s - %(funcName)s at line %(lineno)s : %(message)s"
)
logging.info("START OF APPLICATION━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if __name__ == '__main__':
    print("Starting Caregiver Application ##################################################################")
    whereTheFuckAmI = os.getcwd()
    path_split = whereTheFuckAmI.split("sgive")
    config_folder = os.path.join(path_split[0], "sconf")

    configFilenames_arr = ["config.json", "SMAIL_config.json", "SWEB_config.json"]

    for file_name in configFilenames_arr:
        if not (os.path.exists(config_folder) and os.path.isfile(os.path.join(config_folder, file_name))):
            if file_name == "config.json":  # kind of redundant now, because frontend gets executed first...
                ryuconf.main_config_default(config_folder)
            elif file_name == "SMAIL_config.json":
                ryuconf.smail_config_default(config_folder)
            elif file_name == "SWEB_config.json":
                ryuconf.sweb_config_default(config_folder)

    # ML detection:
    threatDetect.ThreatDetection_ML()
    # calling Frontend
    FrontEnd.main()
