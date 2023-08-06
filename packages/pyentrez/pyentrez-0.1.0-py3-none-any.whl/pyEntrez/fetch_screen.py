"""This is the main screen that is initialized when starting pyEntrez. 

Entrez requests can be made from here. From any other screen, escaping completely should return you to this screen. This should be the default status.add()

Author: William Slattery
Created: 11/24/2020
"""
    
import os
import datetime
import py_cui.widget_set

# pyEntrez
from pyEntrez import __version__, __copyright__
import pyEntrez.screen_manager as sm
import pyEntrez.commands
from pyEntrez.utils import string_utils as su

# Logger
from loguru import logger



class FetchScreen(sm.ScreenManager):
    """Class responsible for managing Fetch screen functions

    This class inherits functionality from ScreenManager and will hode code for how the main Fetch screen should appear. All commands entered through fetch should link to Biopython's Entrez tools, either directly, or by calling functions from pyEntrezManager. This class It will be the interface point between CUI widgets and the pyEntrez.commands module.add()

    Args:
        sm (class): Parent ScreenManager class
        top_manager (manager): in most cases, this is pyEntrezManager
    
    Attributes:
        menu_message (str): class-public str holder for holding the envar value in a setting after the prompt sends the input to the toggle command. pyCUI prompts only pass the input text. There is no method to also pass the string that called the prompt box up. To get around this, we save the call to this string and then reference it from the called command.
        settings (list): class-public list of tuples containing envar and plaintext settings.
        menu_choices (list): list of menu choice strings to be used from overview mode.           
    """
    
    menu_message = ''
    settings = [('E-mail','PYENT_EMAIL'),('User','PYENT_USER'),('Sort','PYENT_SORT'),('Retmax','PYENT_RETMAX'),('Retmode','PYENT_RETMODE'),('Rettype','PYENT_RETTYPE'),('Mongo','PYENT_MONGO'),('URI','PYENT_DBURI'),('DB','PYENT_DB')]
    
    @logger.catch
    def __init__(self, top_manager):
        """Constructor for the FetchScreen class
        """
        
        super().__init__(top_manager, 'fetch control')
        self.menu_choices = [   'Enter Credentials', 
                                'DB List',
                                'About',
                                'Enter Custom Command',
                                'Exit']
    @logger.catch                    
    def initialize_screen_elements(self):
        """Function that initializes the widgets for fetch control screen. 
        
        Override of base class function. This creates all initial conditions for the Fetch screen modules: including commands, layout, sizes, and format. Welcome messages, help files, etc. would be set here. Further on we are updating components created here.
        
        Attributes:
            self.entrez_query_box: Query box at bottom of screen. Takes input text and will run query command, passing input str.
            self.info_text_block: Text block with all widget configuration settings.
            self.info_panel: This object points to the text_block and allows for calls to update text displayed in the info panel.
            
        Returns:
            fetch_screen_widget_set(py_cui.widget_set.WidgetSet):  Widget set object for fetch control screen. This set will hold all text boxes, scroll boxes, buttons, labels, etc.
        """
             
        #  Fetch Control window screen widgets and key commands.                
        fetch_screen_widget_set = self.manager.root.create_new_widget_set(10, 8)
        
        # Base keyboard shortcuts.
        self.ak({fetch_screen_widget_set:  (   ['m',self.show_menu], 
                                                ['q',self.manager.clean_exit],
                                                [sm.KEY_BACKSPACE,self.manager.open_settings_window])})
        
        # Textboxes for query
        self.entrez_query_box = fetch_screen_widget_set.add_text_box('Entrez Query', 9, 0, column_span=8)
        self.ak({self.entrez_query_box:([sm.KEY_ENTER,self.query],)})       #? Need to put the trailing comma so this is seen as a tuple inside a tuple, and not a single tuple.
        self.entrez_query_box.set_focus_text('Submit Query - Enter | Return - Esc')
        
        # Main info text block listing information for all pyEntrez operations
        self.info_text_block = fetch_screen_widget_set.add_text_block('Entrez Info', 0, 4, row_span=9, column_span=4)
        #TODO: Modify colors here if you want.
        #self.info_text_block.selectable = False
        self.info_panel = self.info_text_block
        logger.info(f'Fetch Widget Returns: {fetch_screen_widget_set}')
        
    
        # Scrolling block for menu items
        self.entrez_menu_box = fetch_screen_widget_set.add_scroll_menu('Entrez Menu', 0 ,0, row_span=3, column_span=1)
        self.ak({self.entrez_menu_box:  ([sm.KEY_ENTER, self.menu_select],)})
        self.entrez_menu_box.set_focus_text('Select Menu Item - Enter')

        self.refresh_status()
        
        return fetch_screen_widget_set
    
    @logger.catch
    def refresh_status(self):
        """Clears and resets Fetch widgets

        Right now this only refreshes the menu box, but we should expand this to refresh all widgets or make the def more specific. The importance here is that the with pyCUI the str that is displayed in a menu box is often also the command passed.
        
        Attributes:
            out (str): out is a string of all settings helf in envars. 
        """
        
        # Setup on the fly setting list
        out = ''
        for i in self.settings:
            line = f'{i[0]}  :  {os.environ[i[1]]}\n'
            out += line
        logger.info(f"Refreshing....{out}")
        self.entrez_menu_box.clear()
        self.entrez_menu_box.add_item_list(out.splitlines())
    
    @logger.catch
    def menu_select(self):
        """Gets a highlighted string from the menu box and sends it to toggle function.

        The selected string will call a popup box from root_pyCUI. Whatever is entered into the prompt box will be sent to the command. This function will save the string responsible for the call to the class-public menu_message string so it can be referenced in the command as well.
        
        Attributes:
            self.menu_message (str): We save the string responsible for the popup box here for referencing in the following method.
            self.toggle_setting (func): popup box will trigger this func, passing whatever string is input.
        """
        
        self.menu_message = self.entrez_menu_box.get()
        self.manager.root.show_text_box_popup(f'Reset setting: Currently {self.menu_message}', self.toggle_setting)
    
    @logger.catch
    def toggle_setting(self, msg):
        """Swaps the envar value for msg.

        A setting is called from the menu_box and a popup prompt called. The popup triggers this function, passing the new setting as a string msg. The setting responsible for the call is saved in self.menu_message. This function will check the setting against a dict of settings and allow changing the matching key to the passed value. Popping old envar keys is necessary because you cannot update an existing envar. So if it found, pop, and then redeclare.

        Args:
            msg (str): new setting value passed.
        """
       
        #TODO This will toggle envar for current use.
        x = self.menu_message.split(' ')
        for y in self.settings:
            if y[0] == x[0]:
                logger.info(f'Envar Before: {os.environ[y[1]]}')    
                os.environ.pop(y[1])
                os.environ[y[1]] = str(msg)
                logger.info(f'Updated envar: {y[1]}:{os.environ[y[1]]}')    
                break
        self.refresh_status()
        
    @logger.catch        
    def process_menu_selection(self, selection):
        """Execute based on user menu selection
        
        Override of base class. clean_exit is necessary to make sure our logger has all info parsed and when we start passing info to and from data folders we want to gracefully shut those processes down.
        
        Args:
            selction (str): string that was highlighted when the enter key was hit. pyCUI uses the display strings as command names.
        .. todo:: Add more functions.
        """
        
        if selection == 'Enter Credentials':
            self.manager.ask_credentials()
        elif selection == 'DB List':
            self.info_panel.set_text('List of NCBI databases')              #TODO: Add function to call EInfo and pass string to panel
        elif selection == 'About':
            self.info_panel.set_text(self.manager.get_about_info())
        elif selection == 'Enter Custom Command':
            self.ask_custom_command()
        elif selection == 'Exit':
            self.manager.clean_exit()            
        else:
            self.manager.open_not_supported_popup(selection)

    @logger.catch
    def query(self):
            """Submits query to configured db
            """
            query_message = self.entrez_query_box.get()
            out = self.manager.scraper_search(query_message)
            logger.info(f'Querying: {query_message}')
            logger.debug(f'Query returned UIDs: {out}')
            self.update_info(out)
    
    @logger.catch
    def update_info(self, msg):
        """Wipes and replaces text on the main info block

        Args:
            msg (str): String of what needs to be printed on info block.
        
        .. todo:: Figure out a way to wrap text based on screen size.
        """
        
        self.info_text_block.clear()
        self.info_text_block.set_text(str(msg))
            
    @logger.catch
    def set_initial_values(self):
        """Function that initializes status bar for Fetch screen.
        """
        #self.info_text_block.set_text(self.manager.get_about_info(True))
        self.info_text_block.set_text(su.get_entrez_help())
        self.manager.root.set_status_bar_text('Settings - Backspace | Quit - q')
        self.refresh_status()
            
                
           