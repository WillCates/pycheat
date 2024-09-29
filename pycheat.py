#!/home/kali/Projects/pycheat/pycheat/bin/python

#
#   pycheat - an updated command line cheat sheet tool for fast notes reference on commands and configurations right in the terminal
#   Will Cates
#   20240928
#   v1.0
#
#

import pathlib
import orjson
import argparse
import re
import base64

#Naming:
# v_xxx (variable)
# i_xxx (iterable variable)
# l_xxx (collection/list of things)
# f_xxx (fully qualified file path variable)

#Colors for output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#This function displays commands / configs from each file that matched in the index.json file
def display_cheatsheet(args, l_files):
    for i_cheatsheet in l_files:
        f_cheatsheet = args.dir / pathlib.Path("data/" + i_cheatsheet)
        if f_cheatsheet.exists():
            with f_cheatsheet.open("rb") as fh:
                #Test if the JSON loads
                try:
                    v_content = orjson.loads(fh.read())
                except:
                    print(bcolors.FAIL + "JSON Loading Error (" + i_cheatsheet + ")- check your JSON format" + bcolors.ENDC)
                print(bcolors.BOLD + "COMMANDS: " + bcolors.ENDC)
                #Test if the JSON format has all the fields, and then display all the things
                try:
                    bool(v_content["command"])
                    for i_commands in v_content["command"]:
                        verboseprint(bcolors.OKCYAN + "(" + i_cheatsheet + ") " + bcolors.ENDC + v_content["command"][i_commands]["description"])
                        for i_command in v_content["command"][i_commands]["commands"]:
                            i_command_decoded = base64.b64decode(i_command)
                            i_command_formatted = i_command_decoded.decode('utf-8')
                            print(bcolors.OKGREEN + i_command_formatted + bcolors.ENDC + "\n")
                except:
                    print("No Commands present in this topic.\n\n")
                print(bcolors.BOLD + "CONFIGURATIONS: " + bcolors.ENDC)
                #Test if the JSON format has all the fields, and then display all the things
                try:
                    bool(v_content["configuration"])
                    verboseprint(bcolors.OKCYAN + "(" + i_cheatsheet + ") " + bcolors.ENDC + v_content["configuration"]["description"])
                    for i_configuration in v_content["configuration"]["configurations"]:
                        i_configuration_decoded = base64.b64decode(i_configuration)
                        i_configuration_formatted = i_configuration_decoded.decode('utf-8')
                        print(bcolors.OKGREEN + i_configuration_formatted + bcolors.ENDC + "\n")
                except:
                    print("No Configurations present in this topic.\n\n")
                
        else:
            print(bcolors.FAIL + i_cheatsheet + " does not exist! Check to ensure your index file lists valid cheat sheets!" + bcolors.ENDC)

#This function checks the 'index.json' file for keywords, and finds the file to open and display based on the keyword being searched.
def find_cheatsheet(args):
    #Define the path to cheatsheets/index directory
    if re.match("~", args.dir):
        d_path = pathlib.Path(args.dir).expanduser()
    else:
        d_path = pathlib.Path(args.dir)
    #Test for existence of the path
    if not d_path.exists():
        print("\n" + bcolors.FAIL + "Cheatsheet and index directory " + str(d_path) + "not found!" + bcolors.ENDC + "\n")
        parser.print_help()
        exit(1)
    #Add index file to a pathlib path
    f_index = d_path / "index.json"
    #Test for existence of the index file
    if not f_index.exists():
        print("\n" + bcolors.FAIL + "Index file not found! Please create or locate 'index.json' in the cheatsheets directory" + bcolors.ENDC + "\n")
        parser.print_help()
        exit(1)
    #Open the index file and look for keywords
    with f_index.open("rb") as fh:
        try:
            v_content = orjson.loads(fh.read())
        except:
            print(bcolors.FAIL + "JSON Loading Error (index file) - check your JSON format" + bcolors.ENDC)
        l_files = []
        for i_keyword_list in v_content["name"]:
            v_data = v_content["name"][i_keyword_list]["keywords"]
            for i_keyword in v_data:
                matches = re.search(args.keyword, i_keyword)
                if matches is not None:
                    v_filepath = v_content["name"][i_keyword_list]["filename"]
                    l_files.append(v_filepath)
                    break
        if not l_files:
            print(bcolors.FAIL + "\nNo Matches Found" + bcolors.ENDC)
        elif l_files:
            verboseprint("\nThese are your matching cheat sheets: \n")
            for i_file in l_files:
                verboseprint(bcolors.WARNING + i_file + bcolors.ENDC)
            print("\n")
            display_cheatsheet(args, l_files)
        else:
            print("Other error at main.")
            exit()


#Create an argument parser object with a description
parser = argparse.ArgumentParser(
    description='''Command Line Cheat Sheet''',
    epilog="""Takes the google out of hacking.""")
#Parse the host and port arguments
parser.add_argument('keyword', type=str, nargs='?', default='.*', help='Keyword to Search. By default shows all files.') #Optional Positional
parser.add_argument('-d', '--dir', type=str, default='/home/kali/Projects/pycheat/', help='Directory where cheatsheets and index are stored')
parser.add_argument('-v', '--verbose', action='store_true', help='Print descriptions & notes. Otherwise print commands & configs only. Default False/off.') #Flag
#Create a namespace object (NOT A LIST) for the arguments. Have to access with args.NAME.
args = parser.parse_args()
verboseprint = print if args.verbose else lambda *a, **k: None
find_cheatsheet(args)