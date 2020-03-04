
import pefile as pe
from mini_auth import auth_manager
import string
import re


def file_is_packed(file):
    """
    Checks for upx packing
    :param file: pefile object
    :return: boolean
    """
    ret_val = False
    for section in file.sections:
        print(section.Name);
        if 'UPX' in str(section.Name):
            ret_val = True
            break

    return ret_val


def get_strings(path):
    """
    Gets strings in the file
    https://stackoverflow.com/questions/17195924/python-equivalent-of-unix-strings-utility
    :param path: string, required
    :return: string
    """
    with open(path, errors='ignore') as file:
        res = ''
        for c in file.read():
            if c in string.printable:
                res += c
                continue
            if len(res) >= 4:
                yield res
            res = ''
        if len(res) >= 4:
            yield res


def analyze_strings(path):
    """
    Puts potentially dangerous strings into an array
    :param path: string, required
    :return: list of strings
    """
    potentially_dangerous_strings = []
    for s in get_strings(path):
        # match ip address
        if re.match("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", s):
            potentially_dangerous_strings.append(s)
        # match web address
        elif re.match("www\.|http|\.com", s):
            potentially_dangerous_strings.append(s)
    return potentially_dangerous_strings


def get_compiled_date(file):
    """
    Gets the date the file was compiled
    :param file: pefile
    :return: string
    """
    date = str(file.FILE_HEADER.dump_dict()['TimeDateStamp']['Value'])
    return (date.split('['))[1].split(']')[0]


def init_file(path):
    """
    Verifies file exists at provided path and handles it
    :param path: string
    :return: [str, bool]
    """
    is_valid_file = False
    try:
        f = open(path)
        f.close()
        is_valid_file = True
    except IOError:
        print('File not found. Using default.')
        path = './strings.exe'
    return [path, is_valid_file]


def write_to_html(html_string):
    html_file = open('demo.html', 'w')
    html_file.write(html_string)
    html_file.close()


def execute_project():
    potential_path = input('Enter file path or just press enter for default file: ')
    exe_path = init_file(potential_path)[0]
    file = pe.PE(exe_path)
    print('Potentially malicious strings are: ', analyze_strings(exe_path))
    str = "<!DOCTYPE html> \n <html> \n <head> </head> <body >"
    if not file_is_packed(file):
        str += "<p style='font-size: 35px'> File is packed</p> \n"
    str += '</html>\n</body>'
    write_to_html(str)
    print('File is packed: ', file_is_packed(file))
    print('File was compiled on: ', get_compiled_date(file))


# super sophisticated security
if auth_manager():
    execute_project()



