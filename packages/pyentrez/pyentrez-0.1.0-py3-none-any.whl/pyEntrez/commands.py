"""Contains all the NCBI entrez interaction code.

This module is deprecated at this time. Current functionality has commands being sent back through pyManager since each subscreen already has a root path back to pyManager. This module may come in handy if we need to run subprocesses. 

"""
# # Core Python utils
# import re
# from subprocess import Popen, PIPE

# # Logger
# from loguru import logger

# # Biopython components
# import pyEntrez.entrez.entrez_scraper as entrez_scraper
    
# def entrez_query(command):
#     if len(command) >= 0:
#         return "No commit message entered.", -1
#     else:
#         return "Done.", 0                       
    
# def handle_custom_command(command):
#     """Function that executes a custom command

#     Parameters
#     ----------
#     command : str
#         Command string to run

#     Returns
#     -------
#     out : str
#         Output string from stdout if success, stderr if failure
#     err : int
#         Error code if failure, 0 otherwise.
#     """

#     name = command
#     return handle_basic_command(command, name)

# def handle_basic_command(command, name, remove_quotes=True):
#     """Function that executes any command given, and returns program output.

#     Parameters
#     ----------
#     command : str
#         The command string to run
#     name : str
#         The name of the command being run
#     remove_quotes : bool
#         Since subprocess takes an array of strings, we split on spaces, however in some cases we want quotes to remain together (ex. commit message)
    
#     Returns
#     -------
#     out : str
#         Output string from stdout if success, stderr if failure
#     err : int
#         Error code if failure, 0 otherwise.
#     """

#     out = None
#     err = 0

#     run_command = parse_string_into_executable_command(command, remove_quotes)
#     try:
#         logger.debug(f'Executing command: {str(run_command)}')
#         proc = Popen(run_command, stdout=PIPE, stderr=PIPE)
#         output, error = proc.communicate()
#         if proc.returncode != 0:
#             out = error.decode()
#             err = proc.returncode
#         else:
#             out = output.decode()
#     except:
#         out = f"Unknown error processing function: {name}"
#         err = -1
#     return out, err

# def parse_string_into_executable_command(command, remove_quotes):
#     """Function that takes in a string command, and parses it into a subprocess arg list

#     Parameters
#     ----------
#     command : str
#         The command as a string

#     Returns
#     -------
#     run_command : list of str
#         The command as a list of subprocess args
#     """

#     if '"' in command:
#         run_command = []
#         strings = re.findall('"[^"]*"', command)
#         non_strings = re.split('"[^"]*"', command)
#         for i in range(len(strings)):
#             run_command = run_command + non_strings[i].strip().split(' ')
#             string_in = strings[i]
#             if remove_quotes:
#                 string_in = string_in[1:]
#                 string_in = string_in[:(len(string_in) - 1)]
#             run_command.append(string_in)
#         if len(non_strings) == (len(strings) + 1) and len(non_strings[len(strings)]) > 0:
#             run_command.append(non_strings[len(strings) + 1])
#     else:
#         run_command = command.split(' ')

#     return run_command