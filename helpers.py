from zipfile import ZipFile
import os


def get_all_file_paths(directory):
    file_paths = []
    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths


def create_zip(directory, zip_name):
    # calling function to get all file paths in the directory
    file_paths = get_all_file_paths(directory)
    print(file_paths)

    # printing the list of all files to be zipped
    print("Following files will be zipped:")
    for file_name in file_paths:
        print(file_name)

    # writing files to a zipfile
    with ZipFile(zip_name, "w") as zip:
        # writing each file one by one
        for file in file_paths:
            zip.write(file)
    print("All files zipped successfully!")
