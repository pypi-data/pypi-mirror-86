""" pyEntrezManager and TUI entry point.
This will contain the code that drives most actions by each of the components, including the swapping
between components, refreshing the screens, and calling IO functions. This will initialize after selection
from commandline argparse.

Author: Will Slattery
Created: 11/23/2020
"""

# Py_CUI Library
import py_cui

# Logger
from loguru import logger
from pyEntrez.utils import logger_utils as lu

# This is where we will import all sub-component modules
from pyEntrez import __version__, __copyright__
import pyEntrez.settings_screen as SETTINGS
import pyEntrez.fetch_screen as FETCH
import pyEntrez.entrez.entrez_scraper as SCRAPE

#Main pyEntrez manager class
logger.opt(colors=True)
class pyEntrezManager:
    @logger.catch
    def __init__(self, root, credentials, current_state, args):
        self.root               = root
        self.fetch_manager      = FETCH.FetchScreen(self)
        self.settings_manager   = SETTINGS.SettingsScreen(self)
        self.scraper            = SCRAPE.Scraper()
        logger.info(f"Initialized subscreen managers: {self.fetch_manager} and {self.settings_manager} and {self.scraper}")
        
        # Helper objects and default variables
        self.current_state  = current_state
        
        # Credentials for keyring use.
        self.credentials = credentials
        
        # Clean_close method to use
        self.root.run_on_exit(self.close_cleanup)
        
        # User input token
        self.user_message = None
        
        # Initialize CUI elements for subscreens
        self.fetch_widget_set           = self.fetch_manager.initialize_screen_elements()
        self.settings_widget_set        = self.settings_manager.initialize_screen_elements()
        logger.info("Initialized CUI elements.")
        
        self.open_fetch_window()
     
    @lu.logger_wraps()
    @logger.catch
    def scraper_search(self, query):
        self.scraper.term = query
        return self.scraper.search()
    
    def open_fetch_window(self):
        logger.info("Opening fetch window.")
        #self.settings_manager.clear_elements()
        self.fetch_manager.set_initial_values()
        
        self.root.apply_widget_set(self.fetch_widget_set)
        self.root.set_title(f'pyEntrez v{__version__} Fetch')
        self.current_state = 'fetch'
        self.fetch_manager.refresh_status()
    @lu.logger_wraps()    
    def open_settings_window(self):
        logger.info("Opening settings window.")
        self.root.apply_widget_set(self.settings_widget_set)
        self.root.set_title(f'pyEntrez v{__version__} Settings')
        self.current_state = 'settings'
        
    def close_cleanup(self):
        """Function is called when pyEntrez is closed.
        """
        logger.info("Exiting pyEntrez.")
        logger.info("-----------------------------------------------------")
        pass
    
    @lu.logger_wraps()
    @logger.catch
    def clean_exit(self):
        self.close_cleanup
        exit()
        
    def error_exit(self):
        """Function that exits CUI with error code.
        """
        
        logger.error("Exiting pyEntrez with error!")
        self.close_cleanup()
        exit(-1)
        
    def open_not_supported_popup(self, operation):
        """Function that displays warning for a non-supported operation

        Parameters
        ----------
        operation : str
            The name of the non-supported operation
        """

        self.root.show_warning_popup(f'Warning - Not Supported', 'The {operation} operation is not yet supported.')
        logger.info(f"Unsupported command request - {operation}")
        # Subscreen opening functions ---------------------------------------
        
    #def open_settings_window(self):
        """Function for opening the settings window
        """

        logger.info('Opening settings window')
        # Clear out any previously open screen first.
        self.settings_manager.set_initial_values()
        self.root.apply_widget_set(self.settings_widget_set)
        self.root.set_title(f'pyEntrez v{__version__} Settings')
        self.current_state = 'settings'
        self.settings_manager.refresh_status()
        
    def get_about_info(self, with_logo=True):
        """Generates some about me information

        Parameters
        ----------
        with_logo : bool
            flag to show logo or not.
        
        Returns
        -------
        about_info : str
            string with about information
        """

        if with_logo:
            about_info = self.get_logo_text()
        else:
            about_info = '\n'
        about_info = about_info + '\n\nAuthor:      William Slattery\n'
        about_info = about_info + 'pyEntrez:    https://github.com/BGASM/pyEntrez\n\n\n'
        about_info = about_info + 'Powered by:  py_CUI Python Command Line UI library:\n\n'
        about_info = about_info + '             https://github.com/jwlodek/py_cui\n\n\n'
        about_info = about_info + '             Biopython library:\n\n'
        about_info = about_info + '             https://github.com/biopython/biopython\n\n\n'
        about_info = about_info + 'Documentation available here:\n\n'
        about_info = about_info + 'py_cui:      https://jwlodek.github.io/py_cui-docs\n\n\n'
        about_info = about_info + 'Biopython:   https://biopython.org/\n\n\n'
        about_info = about_info + '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nStar me on Github!\n\n'
        about_info = about_info + f'Copyright (c) {__copyright__} William Slattery'
        return about_info

    def get_logo_text(self):
            """Generates ascii-art version of pyautogit logo

            Returns
            -------
            logo : str
                ascii-art logo
            """

            logo =          '                 ______      __                 \n'
            logo = logo +   '    ____  __  __/ ____/___  / /_________  ____  \n'
            logo = logo +   '   / __ \\/ / / / __/ / __ \\/ __/ ___/ _ \\/_  /  \n'
            logo = logo +   '  / /_/ / /_/ / /___/ / / / /_/ /  /  __/ / /_  \n'
            logo = logo +   ' / .___/\\__, /_____/_/ /_/\\__/_/   \\___/ /___/  \n'
            logo = logo +   '/_/    /____/                                      \n'    
            return logo                     