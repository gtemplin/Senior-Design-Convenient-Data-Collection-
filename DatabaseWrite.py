import json  # interact with json 
import os  # interact with the operating system 
import requests  # used to make http requests or interact with   
import configparser # handle configuration files to store preferences 
import asyncio  # helps manage multiple IO related tasks 

# current working directory
import urllib3  # used for making requests to web servers through http 


Curpath='C:/Users/liyae/IdeaProjects/IAC_HASS_EdgePC/IAC_SENSOR_PROG_V2'

debug = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# format a message and send to database
# the asyncio loop lets this wait until complete w/o bottlenecking the whole program  
def send_to_database(address, msg):
    try:
        if msg!='':
            url=address.format(msg[0: 1], msg[2:])
            loop = asyncio.get_event_loop()

            return loop.run_until_complete(sendData(url))
    except ConnectionError as c:
        return False;
    except Exception as c:
        print(c)
        return False;

# uses an http get request to send the data 
async def sendData(url):
    print(url)
    response= requests.get(url, verify=False)
    return bool(int(response.status_code)==200)


# uses python's file management function to append 
def write_to_backup(backup, data):
    with open(backup, "a") as _:
        _.write(data)
        return True
    return False


def delete_from_file(file_name, part_to_delete):
    file = open(file_name, "w+")
    file_contents = file.read()
    file_contents = remove_prefix(file_contents, part_to_delete)
    file.truncate()
    file.write(file_contents)
    file.close()


def remove_prefix(input_string, prefix):
    if prefix and input_string.startswith(prefix):
        return input_string[len(prefix):]
    return input_string



# Main program starts here

# Get webserver addtess
def json_to_dict(filename):
    fp = open(filename, 'r')
    data = json.load(fp)
    fp.close()
    return data


config = json_to_dict(str(Curpath)+"/configCustomer.json")
webserver_address = config['WebserverAddress']

# Open backup file (file may or may not exist already)
if  not os.path.isfile(str(Curpath)+"/BackupData.txt"):
    f = open(str(Curpath)+"/BackupData.txt", "x")
    f.close()
while True:
    if os.path.isfile(str(Curpath)+"/CommunicationFlag.txt") or os.path.isfile(str(Curpath)+"/CommunicationFlagActuator.txt"):
        fileContents = ""
        fileContentsActuator = ""
        if os.path.isfile(str(Curpath)+"/CommunicationFlag.txt"):
            try:
                os.remove(str(Curpath)+"/CommunicationFlag.txt")
            except Exception:
                print("CommunicationFlag is not deleted")
                pass;
            file = open(str(Curpath)+"/FormattedSystemData.txt", "r+")
            fileContents = file.read()
            file.truncate(0)
            file.close()
        if os.path.isfile(str(Curpath)+"/CommunicationFlagActuator.txt"):
            try:
                os.remove(str(Curpath)+"/CommunicationFlagActuator.txt")
            except Exception:
                print("CommunicationFlagActuator is not deleted")
                pass;

            file2 = open(str(Curpath)+"/FormattedSystemDataActuator.txt", "r+")
            fileContentsActuator = file2.read()
            file2.truncate(0)
            file2.close()
        fileContents= fileContents + fileContentsActuator;

        if debug:
            print("FILE CONTENTS: {}".format(fileContents))
        start_index = 0
        successfulSend=False
        for i in range(0, len(fileContents), 1):
            if fileContents[i] == "$":
                msg = fileContents[start_index: i] ## TRY DIFFERENT SUBSTRING METHOD
                if debug:
                    print("sending: {}".format(msg))
                successfulSend = send_to_database(webserver_address, msg)
                start_index = i+1
                # if not successfulSend:
                #     break;

        if not successfulSend:

            print("CONNECTION IS DOWN--BACKING UP DATA")
            write_to_backup(str(Curpath)+"/BackupData.txt", fileContents)

        else:
            backup = open(str(Curpath)+"/BackupData.txt")
            backupContents = backup.read()
            start_index = 0
            for i in range(0, len(backupContents), 1):
                if backupContents[i] == "$":
                    msg = backupContents[start_index: i]
                    successfulSend = send_to_database(webserver_address, msg)
                    start_index = i + 1
                    if successfulSend:
                        delete_from_file(str(Curpath)+"/BackupData.txt", msg)
