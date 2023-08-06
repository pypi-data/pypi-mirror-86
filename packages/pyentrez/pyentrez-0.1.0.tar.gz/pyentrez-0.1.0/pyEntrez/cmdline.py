"""cmdline module:
Checks if it is user's first time running script.
Creates the argparser and interprets if user wants to run pyEntrez in cmd or tui mode.
Walks user through creation of setting directory and sets all the envars to be used by the script.
"""
# Core Python Utils
import os, sys, inspect, getpass
from shutil import copy2 as cp
from pathlib import Path

# Py_CUI Library
import py_cui

# configparser Library
import configargparse
from configargparse import YAMLConfigFileParser
import yaml

# credential managers
import keyring

# Logger
from loguru import logger
from pyEntrez.utils import logger_utils as lu

# pyEntrez
from pyEntrez import __version__, __copyright__
import pyEntrez.pyEntrezManager as entrezManager

# Default envars:

pyEnv = ['PYENT_MONGO','PYENT_TUI','PYENT_EMAIL','PYENT_USER','PYENT_DB','PYENT_SORT','PYENT_RETMAX','PYENT_RETMODE','PYENT_RETTYPE','PYENT_DBURI']

def setEnv(args):
    """Function to set envars based on input from CLI argparse.
    
    Loop iterates through the passed dict, and for each key it checks if it matches any envars. To add more envars, they need to be added to cmdline's static default envars variable.

    Args:
        args (dict): dict passed from execute function that has all args entered from cmd.
    """
        
    for key1 in args:
        for key2 in pyEnv: 
            if key1.upper() == key2.split('_')[1]:
                os.environ[key2] = str(args[key1])

def _print_version():
    """Prints version and copyright information.
    """
    
    print(f'\n\npyEntrez v{__version__}\n')
    print('MIT License')
    print(f'Copyright (c) {__copyright__} William Slattery')
    exit()

def _new_user():
    """Deprecated.
    """
    pass
    
def current_path():
    """Returns absolute installation path.

    A few core functions need to read from data files stored within the core directory tree.

    Returns:
        path: specifically returns absolute path of current working directory
    """
    
    cwd = os.path.abspath(os.getcwd())
    logger.debug(f"Absolute install path is {cwd}")
    return cwd
        
def get_parser():
    """Check if new user and then create argparser.

    Function will run check_new() function to check if this is user's first time using the script, and if it is a settings directory will be created and a copy of the default config copied to it. Additionally, the new user will be added to the core_config.yaml file, with a path to the user's my_settings.yaml file. ConfigArgParser allows for setting default config paths and will check defaults>user_settings>envar. User can also pass --INIT arg to create a new workspace.

    Returns:
        configargparse.ArgParser: instance of ConfigArgParser's ArgParser
    """
     
    path = check_new()
    logger.debug(f"In get_parser. Path is {path}")
    default = os.path.join(path, 'my_settings.yaml')
    logger.debug(f'CMD parsed: {default}')
    p = configargparse.ArgParser(description='pyEntrez can be used in either Text User Interfacce mode or directly from the command line.',
                                 config_file_parser_class = YAMLConfigFileParser, 
                                 default_config_files = [default], 
                                 formatter_class = configargparse.DefaultsRawFormatter)
    
    p.add('-c', '--credentials',        action='store_true',                                default=False,          help='Allow user to set DB credentials on application start.')
    p.add('-v', '--version',            action='store_true',                                default=False,          help='Print pyEntrez version information.')
    p.add('-m', '--mongo',              action='store_true',    env_var=pyEnv[0],           default=False,          help='Run pyEntrez in mongoDB mode. Requires user/pass.')
    p.add('-t', '--TUI',                action='store_true',    env_var=pyEnv[1],           default=False,          help='Run pyEntrez in Text User Interface mode.')
    p.add('-I', '--INIT',               action='store_true',                                default=False,           help='First time run, set workspace path.')
    
    p.add('-e', '--email',              type=str,               env_var=pyEnv[2],           default=None,           help='E-mail is required.')
    p.add('-u', '--user',               type=str,               env_var=pyEnv[3],           default=None,           help='DB username.')
    p.add('-d', '--db',                 type=str,               env_var=pyEnv[4],           default='pubmed',       help='NCBI database, default = pubmed')
    p.add('-s', '--sort',               type=str,               env_var=pyEnv[5],           default='relevance',    help='sort style, default = relevance')
    p.add('-x', '--retmax',             type=int,               env_var=pyEnv[6],           default=20,             help='max number of returns from Entrez, default = 20')
    p.add('-o', '--retmode',            type=str,               env_var=pyEnv[7],           default='txt',          help='mode that Entrez should return query in, default = txt')
    p.add('-y', '--rettype',            type=str,               env_var=pyEnv[8],           default='medline',      help='type of Entrez return, default = medline')
    p.add('-i', '--dbURI',              type=str,               env_var=pyEnv[9],           default= None,          help='Mongo URI mongodb+srv://<usr>:<pass>@<cluster>.mongodb.net/test?retryWrites=true&w=majority')
    return p

@lu.logger_wraps()
@logger.catch
def execute():
    """Instance argparser, interpret CMD arguments and behavior of pyEntrez script.

    Command line parsing to determine how pyEntrez should be run. Calls get_parser which will check if user is a new user and run functions to set up user directory. Determines if pyEntrez should be run in TUI or CMD mode. Functionality for an exisiting user to set up a new workspace entirely by passing --INIT argument. Function also allows for checking version.
    
    Attributes:
        credentials (list): List of user credentials returned from argparse.
        args (vars): Vars/dict of all args returned from argparse.
        p (configargparse.ArgParser): instance of ConfigArgParser's ArgParser used to parse the CMD arguments.
    """
    
    credentials = []
    p = get_parser()
    args = vars(p.parse_args())
    logger.info(args)
    if args['INIT']:
        first_run()                                                             #TODO: Set up a way for version to be called and returned before creating a new user.
                                                                                #TODO: Set up arg to modify debug mode.
    if args['version']:
        _print_version()
    setEnv(args)
    if (args['credentials'] or (args['mongo'] and args['user']=='None')):       #! Old new_user was deprecated. Come up with a new function to set up DB credentials.
        credentials.append(_new_user())
    if args['TUI']:
        startTUI(args, credentials)
    else:
        logger.info(f'TUI not selected, initializing CMD functionality.')

@logger.catch
def first_run():
    """Check if user's first time running script and call function to create workspace dir.

    Called if there is no user directory set up for the user's USERNAME envar. User is prompted to enter a desired workspace directory otherwise defaults to ~\\PyEntrez. Creates a data and settings sub-directory structure. Some built in exception processing but needs to be expanded. All directories are created with a 755 setting: wrx for user, r for all others. Sets PYENT_HOME envar to the root PyEntrez directory set up. Calls the cfg_user_add function, to update the core config file and passes the user's newly created settings file path.    

    .. todo:: Expand exception handling
  
    """
    
    
    root        =Path.home()
    path        ='pyEntrez'
    settings    ='settings'
    data        ='data'
    newPath     =input(f"\n\n\nDefault workspace will be set to '{str(root)}\\{str(path)}'.\n If you would like to select a different workspace please: \nEnter a workspace path: ")
    
    if  newPath == '':
        newPath=root
        
    if path in str(newPath):
        newPath=str(newPath).split(path)[0]
        logger.debug(f'WORKSPACE CREATION: User-input path truncated to: {newPath}')
    
    logger.debug(f"WORKSPACE CREATION: Working path is: {str(newPath)}")
    if not os.path.exists(newPath):
        md = input(f'{str(newPath)} does not exist. Should we create it (Yes, No)?\n')
        if md.lower() == 'yes' or md.lower() =='y':
            try:
                os.makedirs(newPath,0o755)
            except PermissionError:
                try_path_err(newPath)
        else:
            try_path_exist_err(newPath)
            
    if not os.access(newPath, os.W_OK):
        try_path_err(newPath)
    else:
        p1 = os.path.join(newPath,path)
        p2 = os.path.join(p1,settings)
        p3 = os.path.join(p1,data)
        os.mkdir(p1,0o755)
        if not os.path.exists(p1):
            try_path_exist_err(p1)
        os.mkdir(p2,0o755)
        if not os.path.exists(p2):
            try_path_exist_err(p2)
        os.mkdir(p3,0o755)
        if not os.path.exists(p3):
            try_path_exist_err(p3)
        logger.info(f'WORKSPACE CREATION: {str(p1)} created.')
        logger.info(f'WORKSPACE CREATION: {str(p2)} created.')
        logger.info(f'WORKSPACE CREATION: {str(p3)} created.')
        os.environ['PYENT_HOME']=p1
        cfg_user_add(p2)
        
def cfg_user_add(p2):
    """Add USERNAME and settings path to core_config file for script startup.

    The core_config.yaml file needs to be located in the config dir on the script install path. Default config is USER_CFG: {}, if this structure is not available the function will fail. New users are added as key:value pairs, using the envar USERNAME as key, and settings dir as value.

    Args:
        p2 (path): Abs path to user's settings directory.
    """
        
    usr = {os.environ['USERNAME']:str(p2)}
    logger.debug(f"Making new user: {usr}")
    users_dict={}
    default = os.path.join(current_path(),'pyEntrez\\config\\', 'default_config.yaml')
    cp_path = os.path.join(p2, 'my_settings.yaml')
    cp(default, cp_path)
    core = os.path.join(current_path(),'pyEntrez\\config\\', 'core_config.yaml')
    with open(core) as file:
        users_dict = yaml.safe_load(file)
    logger.debug(f'Updating user list: {users_dict}')
    users_dict['USER_CFG'].update(usr)
    logger.debug(f'Updated user list: {users_dict}')
    with open(core, 'w') as file:
        out = yaml.dump(users_dict, file)
        logger.info(f'Output {out} to {str(file)}')

def get_usr_path():
    """Function may be used to return the user's setting directory path.

    Initial use is to verify if a user is a first time user or not via check_new(). This is done by checking core_config and using envar USERNAME as a key, looking for a directory value. If the user is new, or if there is no valid setting path the bool TRUE is returned (syntax calling is: first_use, path = get_usr_path)
    If the user is a returning user and the search shows a valid USERNAME:dir_path pair, then FALSE and the path are returned. Path is check for existance before passing.

    Returns:
        bool: first_time is True if no USERNAME:path_to_settings exists in core_config.yaml and False otherwise.
        path: If this is user's first time using script, or if their setting is a bad path, path is set None. Otherwise, it is set to user's settings directory path.
    """
    
    d   = {}
    first_time = True
    path = None
    usr = os.environ['USERNAME']
    core = os.path.join(current_path(),'pyEntrez\\config\\', 'core_config.yaml')
    with open(core) as file:
        d = yaml.safe_load(file)
    
    if not usr in d['USER_CFG']:
        first_time = True
        path = None
    else:
        path = d['USER_CFG'][usr]
        if not os.path.exists(path):
            first_time = True
            path = None
        else:
            first_time = False
    return first_time, path

def check_new():
    """Check if a user setting directory has been created for the user running the script.

    Function runs while loop that checks if a user directory has been created for the user running the script. User is defined by envar USERNAME, and so can be changed by running script with configured envar values. If the loops determines this is the user's first run, it will call the functions to create a workspace. When the loop succeeds (checkingUser = False) it returns the user's my_settings.yaml path.

    Returns:
        path: user's my_settings.yaml path as returned by get_usr_path. 
    """
    
    path = None
    checkingUser = True
    while checkingUser == True:
        first, path = get_usr_path()
        if not first and path != None:
            logger.debug(f"New user, first is false and path found. {path}")
            checkingUser = False
        else:
            logger.debug(f"First time or no path, looping through again.")
            first_run()
    return path

def try_path_err(target):
    """Print and log permission denied error.
    
    Output error to stdout and all logger sinks.
    
    Args:
        target (path): path object to check
    """        
    
    e1=(f'ERROR - Permission denied for target directory: {str(target)}')
    print(e1)
    logger.info(e1)
    exit(-1)
    
def try_path_exist_err(target):
    """Prints and logs error for path not existing.

    Output error to stdout and all logger sinks.

    Args:
        target (path): path to non-existant file or directory.
    """
      
    e1=(f'ERROR - {str(target)} does not exist.')
    print(e1)
    logger.info(e1)
    exit(-1)
        
def startTUI(args, creds):
    """Initiate script in TUI mode.

    Sets up pyCUI root and the TUI manager. All CMD args and credentials are passed to the manager, although all config settings have been saved to envars earlier in script. This is to allow for future use case where we may need passed args to modify behavior of script.

    Args:
        args (dict): dict of all args initially passed to cmd.
        creds (list): list of creds, att just db user, as password will be saved to keyring.
    """
    
    root = py_cui.PyCUI(9, 8)
    root.toggle_unicode_borders()
    input_type = 'welcome'
    _ = entrezManager.pyEntrezManager(root, creds, input_type, args)
    _logger = logger.opt(colors=True)
    _logger.info(f'<d>Parsed args.</>')
    _logger.info(f'<y>Initial state - {input_type}</>')
    _logger.info(f'<g>Initialized manager object, starting CUI...</>')
    
    root.start()
    
    