import subprocess
import pathlib
import hashlib
import os
from datetime import datetime

# input pool and dataset to use to mount snapshots
# input directory where unsorted incremental snapshots live
# iterate through the directory, attempting to receive the snapshots until the inital snapshot recieves
# dump the file hashes of all contents within the snapshot to a text file
# continue iterating through until the next is recieved
# loop this behavior until all snapshots are recieved
# after each snapshot is recieved, append the file hashes of that snapshot's files to the text file

# --- FUNCTION DEFINITION --- #
def dirhashdump(poolPath):
    try:
        print(f'Walking: {poolPath.absolute()}....')
        print('=' * 90)

        with open(f'{snapshotHashFile}', 'a') as hashFile:

            try:
                for file2hash in poolPath.rglob('*'): # Iterates through each item in the directory
                    # Generates the hashes of each file's contents
                    with open(file2hash, 'rb') as file:
                        fileContents = file.read()
                        sha256 = hashlib.sha256()
                        sha256.update(fileContents)
                        hashedFile = sha256.hexdigest()

                    hashFile.write(f'Directory: {hashFile}\n')
                    hashFile.write('=' * 90 + '\n')
                    hashFile.write(f'{hashFile.resolve()}: {hashedFile}\n')
                    hashFile.close()
                    print(f'Hash file created: {snapshotHashFile}') 

            except Exception as err:
                print(f'ERROR: Failed to process {hashFile} - {err}')

    except Exception as er:
        print("INVALID DIRECTORY - This directory doesn't exist.")

# --- TIME --- #
startTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f'Start Time:\t{startTime}')

# --- VARIABLE DECLARATION --- #
snapList = []
snapshotHashFile = f'SnapshotForensics-{startTime}'

# --- MAIN --- #
if os.path.isfile(snapshotHashFile): # Creates a new hash file if one already exists
    os.remove(snapshotHashFile)

while True:
    snapPath = pathlib.Path(input('What directory are snapshots located?: ')) # Requests the snapshot storage directory

    if snapPath.is_dir(): # Input validation
        zfsPath = pathlib.Path(f'/{input("(PLEASE NOTE: This pool and dataset should already be mounted)\nWhat pool and dataset would you like to use to receieve the snapshots? (ex: pool/dataset):")}') # Requests the ZFS pool & dataset
    else:
        print(f'{snapPath} is not a valid directory')
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
                            dirhashdump(zfsPath)
                            snapList.remove(item)
                            print(f'Snapshots remaining: {len(snapList)}')
                            break
                        else:
                            print(f"ERROR: Failed to receive snapshot {item}")
                            print(f"Command failed with return code {rxProcess.returncode}")
                            print(f"Error message:\n{stderr}")
                    else:
                        print(f'{item} is not a file. Skipping...')
                else:
                    print(f'All snapshots have been processed. Script completed!')
                    break

        except Exception as err:
            print(f'ERROR: {err}')
        except PermissionError as permerr:
            print(f'PERMISSION ERROR: {permerr}')
    else:
        print(f'{zfsPath} is not a pool or dataset. Did you create them prior to running this script?')

# TO FIX #
# Not walking correctly
# Ending prematurely
# Not restarting after successful completion of a snapshot receveive