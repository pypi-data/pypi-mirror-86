"""Subscreen that allows for toggling pyEntrez settings.
"""

import os
import datetime
import py_cui.widget_set

# pyEntrez
from pyEntrez import __version__, __copyright__
import pyEntrez.screen_manager as sm

# Logger
from loguru import logger

class SettingsScreen(sm.ScreenManager):
        """Class for settings subscreen in pyEntrez
        """

        @logger.catch
        def __init__(self, top_manager):
                super().__init__(top_manager, 'settings screen')
                logger.debug("Inside setting screen class, inside the inherited subclass.")
        
        @logger.catch
        def initialize_screen_elements(self):
                """Override of parent class. Initialize widgets and returns widget set
                
                Returns
                ------
                settins_widget_set : py_cui.widget_set.WidgetSet
                        Widget set object for seetings screen
                """
                # Output widget set
                settings_widget_set = self.manager.root.create_new_widget_set(9, 6)
                
                # Base keyboard shortcuts.
                self.ak({settings_widget_set:           ([sm.KEY_BACKSPACE, self.manager.open_fetch_window],
                                                         ['q', self.manager.clean_exit],
                                                         ['m', self.show_menu])})
                
                # Info Panel
                self.settings_info_panel = settings_widget_set.add_text_block('Settings Info', 2, 3, row_span=7, column_span=3)
                self.settings_info_panel.set_selectable(False)
                self.info_panel = self.settings_info_panel
                
                # Logo and link labels
                logo_label = settings_widget_set.add_block_label(self.get_settings_ascii_art(), 0, 0, row_span=2, column_span=3, center=True)
                logo_label.set_color(py_cui.RED_ON_BLACK)
                link_label = settings_widget_set.add_label(f'Settings Screen - pyEntrez v{__version__}', 0, 3, row_span=2, column_span=3)
                link_label.add_text_color_rule('Settings Screen*', py_cui.CYAN_ON_BLACK, 'startswith', match_type='line')
                
                # Info panel
                self.settings_info_panel = settings_widget_set.add_text_block('Settings Info Log', 2, 3, row_span=7, column_span=3)
                self.settings_info_panel.set_selectable(False)
                self.info_panel = self.settings_info_panel
                
                return settings_widget_set
                
                
                
        def get_settings_ascii_art(self):
                """Gets ascii art settings logo

                Returns
                -------
                settings_message : str
                Block letter ascii art settings logo
                """

                settings_message =                      ' ____  ____  ____  ____  __  __ _   ___   ____  \n '
                settings_message = settings_message +   '/ ___)(  __)(_  _)(_  _)(  )(  ( \\ / __) / ___) \n'
                settings_message = settings_message +   '\\___ \\ ) _)   )(    )(   )( /    /( (_ \\ \\___ \\ \n'
                settings_message = settings_message +   '(____/(____) (__)  (__) (__)\\_)__) \\___/ (____/ '
                return settings_message