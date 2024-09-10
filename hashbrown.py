import os
import hashlib
from pathlib import Path

# Requests a file from within the current directory, hashes it, and compares it to an expected hash.
while True:
    userInput = input('Enter a file to hash (or type "q[ENTER]" to exit): ')

    if userInput == 'q':
        break
    else:
        try: 
            with open(userInput, 'rb') as target:
                fileContents = target.read()

                # Initializes SHA-256 hashing function
                sha256obj = hashlib.sha256()
                sha256obj.update(fileContents)
                hexDigest = sha256obj.hexdigest()

            expectedHash = input('Enter expected file hash: ')

            if expectedHash == hexDigest:
                print("Match! Both file hashes are the same.")
            else:
                print("Uh oh! These file hashes don't match. Ensure you selected the right file and inserted the correct hash.")
        except FileNotFoundError:
            print(f'File not found: {userInput}')