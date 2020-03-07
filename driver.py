import pefile as pe
from mini_auth import auth_manager
import string
import re

  
HTML_STRING_START = ("<!DOCTYPE html>" + 
"\n <html> \n <head>" +
"<link rel='stylesheet' href='styles.css'>"+
"<script type='text/javascript' src='index.js'></script> </head>"+ 
"<body> " +
    "<div name='loading-div' class='loading-div'>" +
        "<div class='loading-gif'>"+
        "</div>"+ 
        "<p name='hacker-text' style='text-align: center;'>" +
        "</p>"
    "</div>" +
"<div name='loaded-div' style='display: none;'>")
HTML_STRING_END = '</div></body>\n</html>'

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


def get_imports(file):
    for entry in file.DIRECTORY_ENTRY_IMPORT:
        dll_name = entry.dll.decode('utf-8')
        if dll_name == "KERNEL32.dll":
            for func in entry.imports:
                print(func.name.decode('utf-8'))


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
    html_file = open('index.html', 'w')
    html_file.write(html_string)
    html_file.close()


def execute_project():
    potential_path = input('Enter file path or just press enter for default file: ')
    result_string = HTML_STRING_START
    exe_path = init_file(potential_path)[0]
    file = pe.PE(exe_path)
    print(exe_path)
    get_imports(file)
    result_string += "<h1 style='text-align: center;'> Report for: "+exe_path.replace('./', '')+"</h1>\n"
    result_string += "<p style='font-size: 35px'> File is not packed</p> \n" if not file_is_packed(file) else "<p style='font-size: 35px'> File is packed</p> \n"
    result_string += "<p> The file was compiled on: " + get_compiled_date(file) + "</p>\n"
    dangerous_strings = analyze_strings(exe_path)
    if len(dangerous_strings) > 0:
        result_string += "<p>Here are the potentially malicous strings:</p>\n <ul>"
        for string in dangerous_strings:
            result_string += "<li>" + string + "</li>"
        result_string += "</ul>"
    result_string += HTML_STRING_END
    write_to_html(result_string)


# super sophisticated security
if auth_manager():
    execute_project()



