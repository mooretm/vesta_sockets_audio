""" Main menu class for Vesta Audio
"""

# Import GUI packages
import tkinter as tk
from tkinter import messagebox

class MainMenu(tk.Menu):
    """ Main Menu
    """
    # Find parent window and tell it to 
    # generate a callback sequence
    def _event(self, sequence):
        def callback(*_):
            root = self.master.winfo_toplevel()
            root.event_generate(sequence)
        return callback


    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        font_size = 16


        #############
        # File menu #
        #############
        file_menu = tk.Menu(self, tearoff=False)
        # file_menu.add_command(
        #     label="Session...",
        #     command=self._event('<<FileSession>>')
        # )
        #file_menu.add_separator()
        file_menu.add_command(
            label="Quit",
            command=self._event('<<FileQuit>>')
        )
        self.add_cascade(label='File', menu=file_menu, font=("", font_size))


        ###############
        # Server Menu #
        ###############
        server_menu = tk.Menu(self, tearoff=False)
        server_menu.add_command(
            label="Start Server",
            command=self._event('<<ServerStartServer>>')
        )
        # Add Server menu to the menubar
        self.add_cascade(label="Server", menu=server_menu, font=("", font_size))


        ############## 
        # Tools menu #
        ##############
        tools_menu = tk.Menu(self, tearoff=False)
        tools_menu.add_command(
            label='Audio Settings...',
            command=self._event('<<ToolsAudioSettings>>')
        )
        tools_menu.add_command(
            label='Calibration...',
            command=self._event('<<ToolsCalibration>>')
        )
        # Add Tools menu to the menubar
        self.add_cascade(label="Tools", menu=tools_menu, font=("", font_size))


        #############
        # Help menu #
        #############
        help_menu = tk.Menu(self, tearoff=False)
        help_menu.add_command(
            label='About...',
            command=self.show_about
        )
        help_menu.add_command(
            label='Help...',
            command=self._event('<<Help>>')
        )
        # Add help menu to the menubar
        self.add_cascade(label="Help", menu=help_menu, font=("", font_size))


    ##################
    # Menu Functions #
    ##################
    # HELP menu
    def show_about(self):
        """ Show the about dialog """
        about_message = 'Socket Audio Player'
        about_detail = (
            'Written by: Travis M. Moore\n'
            'Version 1.0.0\n'
            'Created: Feb 28, 2023\n'
            'Last edited: March 09, 2023'
        )
        messagebox.showinfo(
            title='About',
            message=about_message,
            detail=about_detail
        )
