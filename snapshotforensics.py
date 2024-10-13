import subprocess
import pathlib
import hashlib
import os
import platform
import logging
from datetime import datetime

# input pool and dataset to use to mount snapshots
# input directory where unsorted incremental snapshots live
# iterate through the directory, attempting to receive the snapshots until the inital snapshot recieves
# dump the file hashes of all contents within the snapshot to a text file
# continue iterating through until the next is recieved
# loop this behavior until all snapshots are recieved
# after each snapshot is recieved, append the file hashes of that snapshot's files to the text file

# --- FUNCTION DEFINITION --- #
def getSystemInfo():
    try:
        info={}
        info['platform']=platform.system()
        info['platform-release']=platform.release()
        info['platform-version']=platform.version()
        info['architecture']=platform.machine()
        return info

    except Exception as e:
        logging.exception(e)
        return False

def dirHashDump(poolPath):
    try:
        print(f'Walking snapshot...') # Insert snapshot name here
        logging.info(f'Walking snapshot...')
        with open(f'{snapshotHashFile}', 'a') as hashFile:
            try:
                for file2hash in poolPath.rglob('*'): # Iterates through each item in the directory
                    if file2hash.is_file():

                        # Generates the hashes of each file's contents
                        with open(file2hash, 'rb') as file:
                            sha256 = hashlib.sha256()
                            sha256.update(file.read())
                            fileHash = sha256.hexdigest()

                        logging.info(f'File Hash of {file2hash}: {fileHash}\n')
                        hashFile.write(f'File Hash of {file2hash}: {fileHash}\n')

                logging.info(f'Hash file updated: {snapshotHashFile}')

            except Exception as err:
                logging.info(f'ERROR: Failed to process {hashFile} - {err}')
    except Exception as err:
        logging.info(f'FUNCTION ERROR: {err}')

# --- TIME --- #
startTime = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
print(f'Start Time:\t{startTime}')

# --- VARIABLE DECLARATION --- #
snapList = []
snapshotHashFile = f'SnapshotForensics-{startTime}'

# --- DEBUG LOG --- #
#Modify the filename for logFile to be your firstNameLastName-Final.txt
logFile = f'{snapshotHashFile}-debug'

# Creates a new log file if one already exists
if os.path.isfile(logFile):
    os.remove(logFile)

# Initializes logging and logs basic system info
logging.basicConfig(filename = logFile, level = logging.DEBUG, format = '%(process)d - %(levelname)s - %(asctime)s - %(message)s')
logging.info('Starting log...')
logging.info(f'Log created on: {startTime}')
logging.info('=' * 90)

# Log the following platform information (system, release, version, machine)
sysInfoDict = getSystemInfo()

if sysInfoDict: # This section creates the system information in log
    logging.info('*** SYSTEM INFORMATION ***')
    for k, v in sysInfoDict.items():
        logging.info(f'\t{k}: {v}')
    logging.info('=' * 90)

# --- MAIN --- #
if os.path.isfile(snapshotHashFile): # Creates a new hash file if one already exists
    os.remove(snapshotHashFile)

while True:
    snapPath = input("Enter directory snapshot path or 'q' to quit: ") # Requests the snapshot storage directory

    if snapPath == 'q':
        break

    snapPath = pathlib.Path(snapPath)

    if snapPath.is_dir(): # Input validation
        zfsPath = pathlib.Path(f'/{input("(PLEASE NOTE: This pool and dataset should already be mounted)\nWhat pool and dataset would you like to use to receieve the snapshots? (ex: pool/dataset):")}') # Requests the ZFS pool & dataset
    else:
        print(f'{snapPath} is not a valid directory')
        logging.info(f'{snapPath} is not a valid directory')
        break

    if zfsPath.is_dir(): # Input validation
        for snapshot in snapPath.rglob('*'): # Iterates through the snapshot directory
            snapList.append(snapshot) # Adds each snapshot to a list

        try:
            while snapList:
                for item in snapList[:]:
                    if item.is_file():
                        command = f'sudo zfs receive -F {str(zfsPath).lstrip('/')} < {item}'
                        rxProcess = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        stdout, stderr = rxProcess.communicate()

                        if rxProcess.returncode == 0:
                            dirHashDump(zfsPath)
                            snapList.remove(item)
                            print(f'Snapshots remaining: {len(snapList)}\n')
                            logging.info(f'Snapshots remaining: {len(snapList)}\n')
                            break
                        else:
                            logging.info(f"NON-FATAL ERROR: Failed to receive snapshot {item}")
                            logging.info(f"Command failed with return code {rxProcess.returncode}: {stderr}") # Remove after debug or add to debug messages

            print(f'All snapshots have been processed')
            logging.info(f'All snapshots have been processed')
        except Exception as err:
            logging.info(f'LOOP ERROR: {err}')
        except PermissionError as permerr:
            logging.info(f'LOOP PERMISSION ERROR: {permerr}')
    else:
        print(f'{zfsPath} is not a pool or dataset. Did you create them prior to running this script?')