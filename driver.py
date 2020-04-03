import pefile as pe
from mini_auth import auth_manager
import string
import re


TAB_NAMES = ['Packed/Compiled', 'Strings', 'Imports']
TAB_COUNT = len(TAB_NAMES) - 1

  
HTML_STRING_START = ("<!DOCTYPE html>" + 
"\n <html> \n <head>" +
"<link rel='stylesheet' href='styles.css'>"+
"<script type='text/javascript' src='index.js'></script> </head>"+ 
"<body style='background-color: #1b262c; color: #bbe1fa; text-size: 20px; margin: 2px;'>" +
    "<div name='loading-div' class='loading-div'>" +
        "<div class='loading-gif'>"+
        "</div>"+ 
        "<p> Loading...</p>"+
        "<p name='hacker-text' style='text-align: center;'>" +
        "</p>" + 
    "</div>" +
"<div name='loaded-div' style='display: none;'>")

HTML_STRING_END = '</div>\n</body>\n</html>'

def file_is_packed(file):
    """
    Checks for upx packing
    :param file: pefile object
    :return: boolean
    """
    ret_val = False
    for section in file.sections:
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


def get_imports_and_functions(file):
    """
    gets the imports and the functions they use
    :param file: pefile
    :return: {[strings], {string, [string]}}
    """
    temp_imports = []
    temp_functions  = {}
    for entry in file.DIRECTORY_ENTRY_IMPORT:
        dll_name = entry.dll.decode('utf-8')
        temp_imports.append(dll_name)
        #check to make sure it exists before clearning the array
        temp_functions[dll_name] = [] if dll_name not in temp_functions else temp_functions[dll_name]
        for func in entry.imports:
            if func.name:
                temp_functions[dll_name].append(func.name.decode('utf-8'))
    return [temp_imports, temp_functions]

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

def build_tabs():
    """
    builds the div containing the buttons that act as tabs
    Returns: 
        A div with TAB_COUNT amount of buttons
    """
    temp_tab = "<div style='display: flex;margin: 0 auto;width: 100%;' name='tabHolder'>"
    for i in range(0, TAB_COUNT+1):
        # set tab 0 to selected by default
        className = 'tab-button-selected' if i ==0 else 'tab-button'
        # each button is triggers a function in the js file
        temp_tab += "<button onclick='tabChanged("+str(i)+")' name=tab-button-"+str(i)+" class='"+className+"' style='flex-grow:" +str(100/TAB_COUNT)+ "'> "+TAB_NAMES[i]+"</button>"
    temp_tab += "</div>"
    return temp_tab

def build_compiled_tab(file):
    """
    builds the tab for compiled date AND if the file is packed or not

    Arguments:
        file PEFile -- PeFile object
    
    Returns:
        div with two p tags in it
    """
    compiled_tab = "<div name='0' style='display: block;'>"
    compiled_tab += "<p style='font-size: 35px'> File is not packed</p> \n" if not file_is_packed(file) else "<p style='font-size: 35px'> File is packed</p> \n"
    compiled_tab += "<p> The file was compiled on: " + get_compiled_date(file) + "</p>\n"
    compiled_tab += "</div>"
    return compiled_tab

def build_strings_tab(dangerous_strings):
    """
    builds the tab for the strings

    Arguments:
        dangerous_strings [string] -- List of the dangerous strings for the file
    
    Returns:
        html string with the strings as a ul
    """
    strings_tab = ''
    strings_tab = "<div name='1' style='display: none;'>"
    if len(dangerous_strings) > 0:
        strings_tab += "<p>Here are the potentially malicous strings:</p>\n <ul>"
        for string in dangerous_strings:
            strings_tab += "<li>" + string + "</li>"
        strings_tab += "</ul>"
    else:
        strings_tab += '<p> No dangerous strings found. We search for anything that looks like a website or an ip address.</p>'
    strings_tab += "</div>"
    return strings_tab

def build_imports_tab(imports, functions_map):
    """
    builds the tab for the imports and lists the functions under them

    Arguments:
        imports [string] -- List of the imports for the file as a string
        functions_map {string: [string]} --  Dictionary with key being the import and the value being an array of functions
    
    Returns:
        html string with the imports as a p tag and it has a ul under it with the functions
    """
    imports_string = "<div name='2' style='display: none;'>"
    if len(imports) > 0:
        imports_string += "<p>Here are the imports and the functions they call:</p>\n"
        for import_name in imports:
            imports_string += import_name + '<ul>\n'
            for function_name in functions_map[import_name]:
                imports_string += "<li>"+function_name+"</li>"
            imports_string += '</ul>\n'
    else:
        imports_string += '<p> No imports were found </p>'
    imports_string += "</div>"
    return imports_string

def execute_project():
    potential_path = input('Enter file path or just press enter for default file: ')
    result_string = HTML_STRING_START
    exe_path = init_file(potential_path)[0]
    file = pe.PE(exe_path)
    print(exe_path)

    result_string += "<h1 style='text-align: center;' name='fileName'> Report for: "+exe_path.replace('./', '')+"</h1>\n"

    result_string += build_tabs()
    result_string += build_compiled_tab(file)
 
    #var name seperate for easy debugging
    dangerous_strings = analyze_strings(exe_path)
    result_string += build_strings_tab(dangerous_strings) 

    imports = get_imports_and_functions(file)
    result_string += build_imports_tab(imports[0], imports[1])

   
    # result_string += "<div style='position: fixed;bottom: 5px;'><button style='height: 25px; text-size: 8px;' onclick='dontPressClicked()'>Dont Press</button></div>"
    result_string += HTML_STRING_END
    write_to_html(result_string)


# super sophisticated security
if auth_manager():
    execute_project()



