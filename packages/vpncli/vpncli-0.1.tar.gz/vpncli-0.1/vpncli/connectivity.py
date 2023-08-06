import subprocess
import time
import logging


def wait_for_connection(address):
    for i in range(30):
        response = subprocess.Popen("ping -n 1 -w 200 " + address, stdout=subprocess.PIPE).wait()
        if response == 0:
            logging.debug("Received response from " + address)
            return 0
        else:
            logging.debug(address + " timed out.")

        time.sleep(0.2)


def wait_until_unreachable(address):
    for i in range(30):
        response = subprocess.Popen("ping -n 1 -w 200 " + address, stdout=subprocess.PIPE).wait()
        if response != 0:
            logging.debug(address + " timed out.")
            return 0
        else:
            logging.debug("Received response from " + address)

        time.sleep(0.2)
