from method import *
from apiclient import errors


def get_method(methods):
    print('Methods: ', end='')
    for method in methods:
        print(method, end='\t')
    print()
    method = input('Please choose which method to operate: ')
    return method.lower().strip()


def main():
    methods = ['list file', 'upload file', 'download file',
               'create folder', 'search file', 'delete file']
    method = get_method(methods)
    while method not in methods:
        print('Invalid method.\n')
        method = get_method(methods)
    if 'list file' in method:
        size = input('Please enter the size: ')
        list_file(size)
    elif 'upload file' in method:
        file_name = input('Please enter the file name: ')
        file_path = input('And the path of the file you want to upload: ')
        mimetype = input('And the type of the file: ')
        upload_file(file_name, file_path, mimetype)
    elif 'download file' in method:
        file_id = input('Please enter the file id: ')
        destination = input('Where you want to store the file: ')
        download_file(file_id, destination)
    elif 'create folder' in method:
        name = input('Please enter the folder name: ')
        create_folder(name)
    elif 'search file' in method:
        size = input('How many file do you want me to search: ')
        operator = input('Please enter the querry: ')
        search_file(size, operator)
    elif 'delete file' in method:
        id = input('Please enter the file id you want to delete: ')
        delete_file(id)


if __name__ == '__main__':
    try:
        main()
    except errors.HttpError as error:
        print('An error occurred: {}'.format(error))