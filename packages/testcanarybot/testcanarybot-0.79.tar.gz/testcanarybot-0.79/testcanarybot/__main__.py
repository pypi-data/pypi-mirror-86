import argparse
import os
import string as sr
import random

from .objects import copy_sample, module_cover, \
        package_events, \
        package_handler, \
        error_handler

parser = argparse.ArgumentParser(description='manager for testcanarybot')
parser.add_argument("-s", dest="copy_sample", action = 'store_true', help='copy a sample project to your library folder')
parser.add_argument("-c", dest="create_module", action = 'store_true', help='create a testcanarybot 0.7 module')
parser.add_argument("-f", dest="folder", action = 'store_true', help='create module in a folder')
parser.add_argument("-package", dest="package_handler", action = 'store_true', help='parser for package')
parser.add_argument("-error", dest="error_handler", action = 'store_true', help='parser for errors')
# parser.add_argument("-command", dest="command_handler", action = 'store_true', help='parser for commands')

args = parser.parse_args()

def write(file_dest, var):
    if file_dest.endswith("main.py"):
        folder = file_dest[:file_dest.rfind("\\")]
        if not os.path.exists(folder): os.mkdir(folder)

    with open(file_dest, mode="w+", encoding="utf-8") as new_file:
        new_file.write(var)

def bool_str(string: str):
    if string.lower() in ['true', '1', 'правда', 'y', 'yes', 'да']:
        return True
    elif string.lower() in ['false', '1', 'ложь', 'n', 'no', 'нет']:
        return False
    else:
        raise ValueError("Wrong string")


def gen_str(test = None):
    result, num = "", random.randint(5, 25)

    if isinstance(test, int):
        num = test

    for i in range(num):
        result += random.choice([
                *sr.ascii_lowercase,
                *sr.digits]
        )
    return result


if args.copy_sample:
    try:
        os.mkdir(os.getcwd() + '\\library\\sampleplugin')
    except:
        pass

    if args.folder:
        dest = '\\library\\sampleplugin\\main.py'
    
    else:
        dest = '\\library\\sampleplugin.py'

    test = os.getcwd() + dest
    write(test, copy_sample)

    print(f"Executed! [{test}]")

elif args.create_module:

    render = module_cover
    codename = gen_str(16)

    if args.folder:
        dest = f'\\library\\{codename}\\main.py'
    
    else:
        dest = f'\\library\\{codename}.py'

    print(f"Hello! it's a manager for testcanarybot! Your module will be saved at {dest[1:]}")
    name = input("Enter a name for your plugin: ")
    print("Enter a description for your plugin: ")

    descr, descr_line = str(), "test"

    while descr_line != "":
        descr_line = input("\t")
        descr += descr_line

        if descr_line != "":
            descr += '\n' +  " " * 12
            
    if name == '': name = "module" + gen_str()
    if descr == '': descr = 'Look at this string, you can you it like a password: ' + gen_str() + '\n' +  " " * 12

    render = render.replace("{name}", name)
    render = render.replace("{descr}", descr)

    if args.package_handler:
        render = render.replace("{package_events}", package_events)
        render = render.replace("{package_handler}", package_handler)

    else:
        render = render.replace("{package_events}", "")
        render = render.replace("{package_handler}", "")

    if args.error_handler:
        render = render.replace("{error_handler}", error_handler)

    else:
        render = render.replace("{error_handler}", "")


    test = os.getcwd() + dest
    write(test, render)
        
    print(f"Executed! [{test}]")


