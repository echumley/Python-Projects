import hashlib
import pathlib

dirPath = input('What directory would you like to scan?: ')
dirPath = pathlib.Path(dirPath)
fileNum = 0

try:
	if dirPath.is_dir(): # Checks to see if the directory is valid before continuing script
		print(f'Walking: {dirPath.absolute()}....')
		print('=' * 90)
		try:
			for item in dirPath.rglob('*'): # Iterates through each item in the directory
				if fileNum >= 100: # Breaks out of the loop if the file count reaches 100
					print("File limit reached. Exiting loop...")
					break

				if item.is_file():
					fileNum += 1

					# Generates the hashes of each file's contents
					with open(item, 'rb') as file:
						fileContents = file.read()
						sha256 = hashlib.sha256()
						sha256.update(fileContents)
						hashedFile = sha256.hexdigest()
					print(f'{item.resolve()}: {hashedFile}')

		except Exception as err:
			print(f'ERROR: Failed to process {item} - {err}')
		except PermissionError as permerr:
			print(f'ERROR: Cannot access {item} - {permerr}')

	else:
		print("INVALID DIRECTORY - This directory doesn't exist.")
except Exception as er:
	print("INVALID DIRECTORY - This directory doesn't exist.")
