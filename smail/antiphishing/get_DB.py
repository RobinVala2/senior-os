import logging
import os
import datetime
import subprocess

file_path = "../sconf/phish/SMAIL_PHISH_1.txt"
command_file = "antiphishing/get_db.txt"

logger = logging.getLogger(__file__)

def get_DB():
    # check if database exists
    if os.path.exists(file_path):
        # get the last modification date
        last_modif_date = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        # get current date
        current_date = datetime.datetime.now()
        # getting the age of file
        file_age = current_date - last_modif_date
        # update time = 14 days
        update_time = datetime.timedelta(days=14)

        logger.info(f"Phishing database file is {file_age.days} days, {file_age.seconds // 3600} hours, "
              f"and {(file_age.seconds // 60) % 60} minutes old.")

        # if age of the file is bigger than update time,
        # new updated file will be downloaded
        if file_age >= update_time:

            try:
                with open(command_file, "r") as f:
                    command = f.read()
                f.close()
                # execute command
                subprocess.run(command, shell=True, check=True,
                               executable='/bin/bash', stdout=subprocess.PIPE)

            except:
                logger.info(f"The command file {command_file} does not exist. "
                            f"Cannot update phishing database.")

        else:
            logger.info(f"The file {file_path} is not older than 2 weeks. "
                        f"No need to update phishing database.")

    else:
        # if file with phishing database is missing
        # Execute command
        try:
            with open(command_file, 'r') as f:
                command = f.read()
            f.close()
            subprocess.run(command, shell=True, check=True,
                           executable='/bin/bash', stdout=subprocess.PIPE)
            logger.info(f"The file {file_path} does not exist. "
                        f"Downloading current phishing database")

        except:
            logger.info(f"The command file {command_file} does not exist. "
                        f"Cannot update phishing database.")
