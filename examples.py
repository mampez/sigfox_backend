"""Example test"""
from modules import sigfox_backend
from pprint import pprint


USER = ''
PASSWORD = ''

def main():
    """ main example"""

    ## Class
    sigfox = sigfox_backend.sigfox(USER, PASSWORD)
    ## Device list
    devices = sigfox.device_list_id()

    for device in devices:
        print device
        pprint(sigfox.device_n_messages(device, 2))


if __name__ == "__main__":
    main()

