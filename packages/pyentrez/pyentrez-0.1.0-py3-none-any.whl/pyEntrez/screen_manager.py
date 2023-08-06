from sys import platform
import pyEntrez.commands
from loguru import logger
from pyEntrez.utils import logger_utils as lu
import py_cui.widget_set

pykey ={'a':py_cui.keys.KEY_A_LOWER,
        'b':py_cui.keys.KEY_B_LOWER,
        'c':py_cui.keys.KEY_C_LOWER,
        'd':py_cui.keys.KEY_D_LOWER,
        'e':py_cui.keys.KEY_E_LOWER,
        'f':py_cui.keys.KEY_F_LOWER,
        'g':py_cui.keys.KEY_G_LOWER,
        'h':py_cui.keys.KEY_H_LOWER,
        'i':py_cui.keys.KEY_I_LOWER,
        'j':py_cui.keys.KEY_J_LOWER,
        'k':py_cui.keys.KEY_K_LOWER,
        'l':py_cui.keys.KEY_L_LOWER,
        'm':py_cui.keys.KEY_M_LOWER,
        'n':py_cui.keys.KEY_N_LOWER,
        'o':py_cui.keys.KEY_O_LOWER,
        'p':py_cui.keys.KEY_P_LOWER,
        'q':py_cui.keys.KEY_Q_LOWER,
        'r':py_cui.keys.KEY_R_LOWER,
        's':py_cui.keys.KEY_S_LOWER,
        't':py_cui.keys.KEY_T_LOWER,
        'u':py_cui.keys.KEY_U_LOWER,
        'v':py_cui.keys.KEY_V_LOWER,
        'w':py_cui.keys.KEY_W_LOWER,
        'x':py_cui.keys.KEY_X_LOWER,
        'y':py_cui.keys.KEY_Y_LOWER,
        'z':py_cui.keys.KEY_Z_LOWER,
        'A':py_cui.keys.KEY_A_UPPER,
        'B':py_cui.keys.KEY_B_UPPER,
        'C':py_cui.keys.KEY_C_UPPER,
        'D':py_cui.keys.KEY_D_UPPER,
        'E':py_cui.keys.KEY_E_UPPER,
        'F':py_cui.keys.KEY_F_UPPER,
        'G':py_cui.keys.KEY_G_UPPER,
        'H':py_cui.keys.KEY_H_UPPER,
        'I':py_cui.keys.KEY_I_UPPER,
        'J':py_cui.keys.KEY_J_UPPER,
        'K':py_cui.keys.KEY_K_UPPER,
        'L':py_cui.keys.KEY_L_UPPER,
        'M':py_cui.keys.KEY_M_UPPER,
        'N':py_cui.keys.KEY_N_UPPER,
        'O':py_cui.keys.KEY_O_UPPER,
        'P':py_cui.keys.KEY_P_UPPER,
        'Q':py_cui.keys.KEY_Q_UPPER,
        'R':py_cui.keys.KEY_R_UPPER,
        'S':py_cui.keys.KEY_S_UPPER,
        'T':py_cui.keys.KEY_T_UPPER,
        'U':py_cui.keys.KEY_U_UPPER,
        'V':py_cui.keys.KEY_V_UPPER,
        'W':py_cui.keys.KEY_W_UPPER,
        'X':py_cui.keys.KEY_X_UPPER,
        'Y':py_cui.keys.KEY_Y_UPPER,
        'Z':py_cui.keys.KEY_Z_UPPER,
        '0':py_cui.keys.KEY_0,
        '1':py_cui.keys.KEY_1,
        '2':py_cui.keys.KEY_2,
        '3':py_cui.keys.KEY_3,
        '4':py_cui.keys.KEY_4,
        '5':py_cui.keys.KEY_5,
        '6':py_cui.keys.KEY_6,
        '7':py_cui.keys.KEY_7,
        '8':py_cui.keys.KEY_8,
        '9':py_cui.keys.KEY_9}
class ScreenManager:
        """Main parent screen manager class.
        
        Contains common functionality for showing command results, handling credentials, commands, and long operations.

        Attributes
        ----------
        manager : pyEntrezManager
                Driver engine manager
        message : str
                A variable to store messages accross functions
        status : int
                A variable to store status codes accross functions
        utility_var : obj
                A variable that can be used to store any data across functions
        menu_choices : list of str
                Overriden by children, list of options that pop up in menu
        info_panel : py_cui.widgets.TextBlock
                The main textblock on the screen, used to display status information.
        """
        def __init__(self, top_manager, screen_type):
                """Constructor for ScreenManager
                """
                                
                self.screen_type = screen_type
                self.manager = top_manager
                self.message = ''
                self.status = 0
                self.utility_var = None
                self.menu_choices = ['About', 'Exit']
                self.info_panel = None


        def initialize_screen_elements(self):
                """Function that must be overridden by subscreen. Creates py_cui_widgets, returns widget set object.
                """

                pass


        def process_menu_selection(self, selection):
                """Processes based on selection returned from the menu
                Parameters
                ----------
                selection : str
                An element of the self.menu_choices list selected by user
                """

                if selection == 'About' and self.info_panel is not None:
                        self.info_panel.set_text(self.manager.get_about_info())
                elif selection == 'Exit':
                        self.manager.clean_exit()
                        


        def show_menu(self):
                """Opens the menu using the menu item list for screen manager instance
                """
                logger.info(f'Opening {self.screen_type} menu')
                self.manager.root.show_menu_popup('Full Control Menu', self.menu_choices, self.process_menu_selection)


        def show_command_result(self, out, err, show_on_success = True, command_name='Command', success_message='Success', error_message='Error'):
                """Function that displays the result of stdout/err for an external command.
                Parameters
                ----------
                out : str
                stdout string from command
                err : str
                stderr string from command
                show_on_success : bool
                Set to false to show no messages on success. (ex. git log doesnt need success message)
                command_name : str
                name of command run.
                success_message : str
                message to show on successful completion
                error_message : str
                message to show on unsuccessful completion
                """

                show_in_box = False
                stripped_output = out.strip()
                if len(out.splitlines()) > 1:
                        popup_message = "Check Info Box For {} Output".format(command_name)
                        show_in_box = True
                else:
                        popup_message = stripped_output
                if err != 0:
                        self.manager.root.show_error_popup(error_message, popup_message)
                elif show_on_success:
                        self.manager.root.show_message_popup(success_message, popup_message)
                if show_in_box and (err != 0 or show_on_success):
                        box_out = out
                if err != 0:
                        err_out = '\n'
                        temp = out.splitlines()
                        for line in temp:
                                err_out = err_out + '- ' + line + '\n'
                                box_out = err_out
                        self.info_panel.title = '{} Output'.format(command_name)
                        self.info_panel.set_text(box_out)


        def show_status_long_op(self, name='Command', succ_message="Success", err_message = "Error"):
                """Shows the status of a long(async) operation on success completion
                Parameters
                ----------
                name : str
                name of command run.
                succ_message : str
                message to show on successful completion
                err_message : str
                message to show on unsuccessful completion
                """

                self.show_command_result(self.message, self.status, command_name=name, success_message=succ_message, error_message=err_message)
                self.message = ''
                self.status = 0


        def refresh_status(self):
                """Function that is fired after each git operation. Implement in subclasses.
                """

                pass


        def clear_elements(self):
                """Function that clears entries from widgets for reuse
                """

                pass


        def set_initial_values(self):
                """Function that sets initial values for widgets in screen
                """

                pass


        def handle_user_command(self, command):
                """Handles custom user command.
                Parameters
                ----------
                command : str
                The string command entered by the user
                """

                out, err = pyEntrez.commands.handle_custom_command(command)
                self.show_command_result(out, err, command_name=command)
                self.refresh_status()


        def ask_custom_command(self):
                """Function that prompts user to enter custom command
                """

                shell='Bash'
                if platform == 'win32':
                        shell='Batch'
                        self.manager.root.show_text_box_popup('Please Enter A {} Command:'.format(shell), self.handle_user_command)

        
        def execute_long_operation(self, loading_messge, long_op_function, credentials_required=False):
                """Wrapper function that allows for executing long operations w/ credential requirements.
                Parameters
                ----------
                loading_message : str
                Message displayed while async op is performed
                long_op_function : no-arg or lambda function
                Function that is fired in an async second thread
                credentials_required : bool
                If true, prompts to enter credentials before starting async op
                """
                
                if credentials_required and not self.manager.were_credentials_entered():
                        self.manager.ask_credentials(callback=lambda : self.manager.perform_long_operation(loading_messge, long_op_function, self.show_status_long_op))
                else:
                        self.manager.perform_long_operation(loading_messge, long_op_function, self.show_status_long_op)
                        
        
        def ak(self, key_add):
                """Function that takes a key_add dict in the form of a
                {func:([str(key),func(command)])}
                """
             
                for key in key_add:
                        for value in key_add[key]:
                                if type(value) is list:
                                        if type(value[0]) is str:
                                                key.add_key_command(pykey[value[0]],value[1])
                                        else:
                                                key.add_key_command(value[0],value[1])
     
from sys import platform
import curses

# Some simple helper functions

def get_ascii_from_char(char):
        """Function that converts ascii code to character

        Parameters
        ----------
        char : character
                character to convert to ascii
        
        Returns
        -------
        ascii_code : int
                Ascii code of character
        """

        return ord(char)


def get_char_from_ascii(key_num):
        """Function that converts a character to an ascii code

        Parameters
        ----------
        ascii_code : int
                Ascii code of character

        Returns
        -------
        char : character
                character converted from ascii
        """
        
        return chr(key_num)


# Supported py_cui keys
KEY_ENTER       = get_ascii_from_char('\n')
# Escape character is ascii #27
KEY_ESCAPE      = 27
KEY_SPACE       = get_ascii_from_char(' ')
KEY_DELETE      = curses.KEY_DC
KEY_TAB         = get_ascii_from_char('\t')

# Arrow Keys
KEY_UP_ARROW    = curses.KEY_UP
KEY_DOWN_ARROW  = curses.KEY_DOWN
KEY_LEFT_ARROW  = curses.KEY_LEFT
KEY_RIGHT_ARROW = curses.KEY_RIGHT


if platform == 'linux' or platform == 'darwin':

        # Modified arrow keys
        KEY_SHIFT_LEFT  = 393
        KEY_SHIFT_RIGHT = 402
        KEY_SHIFT_UP    = 337
        KEY_SHIFT_DOWN  = 336
        
        KEY_CTRL_LEFT   = 560
        KEY_CTRL_RIGHT  = 545
        KEY_CTRL_UP     = 566
        KEY_CTRL_DOWN   = 525

elif platform == 'win32':

        KEY_SHIFT_LEFT  = 391
        KEY_SHIFT_RIGHT = 400
        KEY_SHIFT_UP    = 547
        KEY_SHIFT_DOWN  = 548
        
        KEY_CTRL_LEFT   = 443
        KEY_CTRL_RIGHT  = 444
        KEY_CTRL_UP     = 480
        KEY_CTRL_DOWN   = 481



# Page navigation keys
KEY_PAGE_UP     = curses.KEY_PPAGE
KEY_PAGE_DOWN   = curses.KEY_NPAGE
KEY_HOME        = curses.KEY_HOME
KEY_END         = curses.KEY_END

# Control Keys
KEY_CTRL_A      = 1
KEY_CTRL_B      = 2
KEY_CTRL_C      = 3
KEY_CTRL_D      = 4
KEY_CTRL_E      = 5
KEY_CTRL_F      = 6
KEY_CTRL_G      = 7
KEY_CTRL_H      = 8
KEY_CTRL_I      = 9
KEY_CTRL_J      = 10
KEY_CTRL_K      = 11
KEY_CTRL_L      = 12
KEY_CTRL_M      = 13
KEY_CTRL_N      = 14
KEY_CTRL_O      = 15
KEY_CTRL_P      = 16
KEY_CTRL_Q      = 17
KEY_CTRL_R      = 18
KEY_CTRL_S      = 19
KEY_CTRL_T      = 20
KEY_CTRL_U      = 21
KEY_CTRL_V      = 22
KEY_CTRL_W      = 23
KEY_CTRL_X      = 24
KEY_CTRL_Y      = 25
KEY_CTRL_Z      = 26


_ALT_MODIFIER = 0
if platform == 'win32':
        _ALT_MODIFIER = 320

# Alt-modified keys
KEY_ALT_A       = 97 + _ALT_MODIFIER
KEY_ALT_B       = 98 + _ALT_MODIFIER
KEY_ALT_C       = 99 + _ALT_MODIFIER
KEY_ALT_D       = 100 + _ALT_MODIFIER
KEY_ALT_E       = 101 + _ALT_MODIFIER
KEY_ALT_F       = 102 + _ALT_MODIFIER
KEY_ALT_G       = 103 + _ALT_MODIFIER
KEY_ALT_H       = 104 + _ALT_MODIFIER
KEY_ALT_I       = 105 + _ALT_MODIFIER
KEY_ALT_J       = 106 + _ALT_MODIFIER
KEY_ALT_K       = 107 + _ALT_MODIFIER
KEY_ALT_L       = 108 + _ALT_MODIFIER
KEY_ALT_M       = 109 + _ALT_MODIFIER
KEY_ALT_N       = 110 + _ALT_MODIFIER
KEY_ALT_O       = 111 + _ALT_MODIFIER
KEY_ALT_P       = 112 + _ALT_MODIFIER
KEY_ALT_Q       = 113 + _ALT_MODIFIER
KEY_ALT_R       = 114 + _ALT_MODIFIER
KEY_ALT_S       = 115 + _ALT_MODIFIER
KEY_ALT_T       = 116 + _ALT_MODIFIER
KEY_ALT_U       = 117 + _ALT_MODIFIER
KEY_ALT_V       = 118 + _ALT_MODIFIER
KEY_ALT_W       = 119 + _ALT_MODIFIER
KEY_ALT_X       = 120 + _ALT_MODIFIER
KEY_ALT_Y       = 121 + _ALT_MODIFIER
KEY_ALT_Z       = 122 + _ALT_MODIFIER

# Pressing backspace returns 8 on windows?
if platform == 'win32':
        KEY_BACKSPACE   = 8
# Adds support for 'delete/backspace' key on OSX
elif platform == 'darwin':
        KEY_BACKSPACE   = 127
else:
        KEY_BACKSPACE   = curses.KEY_BACKSPACE