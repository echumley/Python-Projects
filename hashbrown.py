import os
import hashlib
from pathlib import Path

def hashFile(target, algorithm):
    fileContents = target.read()
    md5obj = algorithm()
    md5obj.update(fileContents)
    return md5obj.hexdigest()

algorithms = {
     'MD5': hashlib.md5,
     'SHA1': hashlib.sha1,
     'SHA256': hashlib.sha256
}

# Requests a file from within the current directory, hashes it, and compares it to an expected hash.
while True:
    algorithm = input('Pick a hashing algorithm (MD5, SHA1, or SHA256) or enter "q" to exit: ').upper()
    if algorithm == 'Q':
        break

    userInput = input('Enter a file to hash or enter "q" to exit: ')
    if userInput.lower() == 'q':
        break

    if algorithm in algorithms:
        try: 
            with open(userInput, 'rb') as target:
                    hexDigest = hashFile(target, algorithms[algorithm])
                    print(f'{algorithm} hash: {hexDigest}')
        except FileNotFoundError:
            print(f"File: {userInput} does not exist. Please try again.")
        except Exception as err:
            print(f'Error: {err}')
    else:
        print('Invalid hash algorithm.')
        
    expectedHash = input('Enter expected file hash: ')

    if expectedHash == hexDigest:
        print("Match! Both file hashes are the same.")
    else:
        print("Uh oh! These file hashes don't match. Ensure you selected the right file and inserted the correct hash.")