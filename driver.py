
import pefile as pe
from mini_auth import auth_manager


def file_is_packed(file):
    ret_val = False
    for section in file.sections:
        if 'UPX' in str(section.Name):
            ret_val = True
            break

    return ret_val

def execute_project():
    file = pe.PE('./strings.exe')
    print('File is packed: ', file_is_packed(file))


# super sophisticated security
if auth_manager():
    execute_project()



