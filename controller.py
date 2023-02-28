""" Socket Audio Player. Audio player that receives files and commands
    via TCP/IP. 

    Written for use with Vulcan interface. Necessary because Vulcan 
    requires a version of Python that is not supposed by ASIO. 

    Written by: Travis M. Moore
    Created: Feb 28, 2023
    Last edited: Feb 28, 2023
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
#from PIL import Image, ImageTk

# Import system packages
import os
import sys
from pathlib import Path
import gc
import time

# Import misc packages
import webbrowser
import markdown

# Import custom modules
# Menu imports
from menus import mainmenu
# Model imports
from models import sessionmodel
from models import audiomodel
# View imports
from views import mainview
#from views import sessionview
from views import audioview
from views import calibrationview
# Server imports
import app_server


#########
# BEGIN #
#########
class Application(tk.Tk):
    """ Application root window
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ######################################
        # Initialize Models, Menus and Views #
        ######################################
        # Setup main window
        self.withdraw() # Hide window during setup
        self.resizable(False, False)
        self.title("Socket Audio")

        # Increase font size globally
        # style = ttk.Style()
        # default_font = tkFont.nametofont('TkDefaultFont')
        # default_font.configure(size=14)

        # Load current session parameters from file
        # Or load defaults if file does not exist yet
        self.sessionpars_model = sessionmodel.SessionParsModel()
        self._load_sessionpars()

        # Load CSV writer model
        #self.csvmodel = csvmodel.CSVModel(self.sessionpars)

        # Load main view
        self.main_frame = mainview.MainFrame(self)
        self.main_frame.grid(row=5, column=5)

        # Create trial counter
        self.counter = None

        # Create and update date trial label
        # self.trial_var = tk.StringVar(value='Trial:')
        # ttk.Label(self, textvariable=self.trial_var, 
        #     style='trial.TLabel').grid(row=10, column=5, sticky='w',
        #     padx=10, pady=10)

        # Load menus
        menu = mainmenu.MainMenu(self)
        self.config(menu=menu)

        # Create response and outcome trackers
        self.response = None
        self.outcome = None

        # Create callback dictionary
        event_callbacks = {
            # File menu
            '<<FileSession>>': lambda _: self._show_session_dialog(),
            '<<FileQuit>>': lambda _: self._quit(),

            # Tools menu
            '<<ToolsAudioSettings>>': lambda _: self._show_audio_dialog(),
            '<<ToolsCalibration>>': lambda _: self._show_calibration_dialog(),
            '<<ToolsStartServer>>': lambda _: self.start_server(),

            # Help menu
            '<<Help>>': lambda _: self._show_help(),

            # Session dialog commands
            '<<SessionSubmit>>': lambda _: self._save_sessionpars(),

            # Calibration dialog commands
            '<<PlayCalStim>>': lambda _: self._play_calibration(),
            '<<CalibrationSubmit>>': lambda _: self._calc_level(),

            # Audio dialog commands
            '<<AudioDialogSubmit>>': lambda _: self._save_sessionpars(),

            # Main View commands
            '<<MainPlay>>': lambda _: self.play(),
            '<<MainStop>>': lambda _: self.stop(),
        }

        # Bind callbacks to sequences
        for sequence, callback in event_callbacks.items():
            self.bind(sequence, callback)

        # Center main window
        self.center_window()


    #####################
    # General Functions #
    #####################
    def center_window(self):
        """ Center the root window 
        """
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        self.geometry("+%d+%d" % (x, y))
        self.deiconify()


    def _quit(self):
        """ Exit the application.
        """
        # Quit app
        quit()
        #self.destroy()


    def resource_path(self, relative_path):
        """ Get the absolute path to compiled resources
        """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


    ########################
    # Main Frame Functions #
    ########################
    def play(self):
        """ Begin session. Load and randomize stimulus presentation 
            list. Clean up buttons.
        """
        print("controller: Play func called")
        # Create audio object
        # try:
        #     self.a = audiomodel.Audio(file_path=audio_filepath,
        #         device_id=self.sessionpars['Audio Device ID'].get())
        # except FileNotFoundError:
        #     print("\ncontroller: Audio file does not exist!")
        #     return

        # # Present audio
        # self.a.play(level=self.stim_master.iloc[self.counter, 1])



    def stop(self):
        print("controller: Stop func called")
        # try:
        #     self.a.stop()

        #     # Manually remove current audio object from memory
        #     # This is required due to the 32bit/64bit issue in numpy
        #     del(self.a)
        #     gc.collect()
        # except AttributeError:
        #     print("controller: Stimuli not loaded yet!")
        #     messagebox.showerror(title="File Not Found!",
        #         message="Stimuli not loaded yet!",
        #         detail="You must start the session by clicking the START " +
        #             "button to load the audio files.")


    #######################
    # Help Menu Functions #
    #######################
    def _show_help(self):
        """ Create html help file and display in default browser
        """
        print("controller: Looking for help file in compiled " +
            "version temp location...")
        help_file = self.resource_path('README\\README.html')
        file_exists = os.access(help_file, os.F_OK)
        if not file_exists:
            print('controller: Not found!\nChecking for help file in ' +
                'local script version location')
            # Read markdown file and convert to html
            with open('README.md', 'r') as f:
                text = f.read()
                html = markdown.markdown(text)

            # Create html file for display
            with open('.\\assets\\README\\README.html', 'w') as f:
                f.write(html)

            # Open README in default web browser
            webbrowser.open('.\\assets\\README\\README.html')
        else:
            help_file = self.resource_path('README\\README.html')
            webbrowser.open(help_file)


    ############################
    # Session Dialog Functions #
    ############################
    # def _show_session_dialog(self):
    #     """ Show session parameter dialog
    #     """
    #     print("\ncontroller: Calling session dialog...")
    #     sessionview.SessionDialog(self, self.sessionpars)


    def _load_sessionpars(self):
        """ Load parameters into self.sessionpars dict 
        """
        vartypes = {
        'bool': tk.BooleanVar,
        'str': tk.StringVar,
        'int': tk.IntVar,
        'float': tk.DoubleVar
        }

        # Create runtime dict from session model fields
        self.sessionpars = dict()
        for key, data in self.sessionpars_model.fields.items():
            vartype = vartypes.get(data['type'], tk.StringVar)
            self.sessionpars[key] = vartype(value=data['value'])
        print("\ncontroller: Loaded sessionpars model fields into " +
            "running sessionpars dict")


    def _save_sessionpars(self, *_):
        """ Save current runtime parameters to file 
        """
        print("\ncontroller: Calling sessionpar model set and save funcs...")
        for key, variable in self.sessionpars.items():
            self.sessionpars_model.set(key, variable.get())
            self.sessionpars_model.save()


    ########################
    # Tools Menu Functions #
    ########################
    def start_server(self):
        self.server = app_server.Server()


    ##########################
    # Audio Dialog Functions #
    ##########################
    def _show_audio_dialog(self):
        """ Show audio settings dialog
        """
        print("\ncontroller: Calling audio dialog...")
        audioview.AudioDialog(self, self.sessionpars)


    ################################
    # Calibration Dialog Functions #
    ################################
    def _show_calibration_dialog(self):
        """ Display the calibration dialog window
        """
        print("\ncontroller: Calling calibration dialog...")
        calibrationview.CalibrationDialog(self, self.sessionpars)


    def _calc_level(self):
        """ Calculate and save adjusted presentation level
        """
        # Calculate SLM offset
        print("\ncontroller: Calculating new presentation level...")
        slm_offset = self.sessionpars['SLM Reading'].get() - self.sessionpars['raw_lvl'].get()
        # Provide console feedback
        print(f"SLM reading: {self.sessionpars['SLM Reading'].get()}")
        print(f"raw_lvl: {self.sessionpars['raw_lvl'].get()}")
        print(f"SLM offset: {slm_offset}")

        # Calculate new presentation level
        self.sessionpars['Adjusted Presentation Level'].set(
            self.sessionpars['Presentation Level'].get() - slm_offset)
        print(f"New presentation level: " +
            f"{self.sessionpars['Adjusted Presentation Level'].get()}")

        # Save SLM offset and updated level
        self._save_sessionpars()


    def _play_calibration(self):
        """ Load calibration file and present
        """
        # Check for default calibration stimulus request
        if self.sessionpars['Calibration File'].get() == 'cal_stim.wav':
            # Create calibration audio object
            try:
                # If running from compiled, look in compiled temporary location
                cal_file = self.resource_path('cal_stim.wav')
                cal_stim = audiomodel.Audio(
                    file_path = cal_file,
                    device_id = self.sessionpars['Audio Device ID'].get()
                    )
            except FileNotFoundError:
                # If running from command line, look in assets folder
                cal_file = '.\\assets\\cal_stim.wav'
                cal_stim = audiomodel.Audio(
                    file_path = cal_file,
                    device_id = self.sessionpars['Audio Device ID'].get()
                    )

            # Get presentation level from calibration dialog
            # Convert from db to magnitude
            cal_lvl = cal_stim.db2mag(self.sessionpars['raw_lvl'].get())

            # Present calibration stimulus
            cal_stim.play(level=cal_lvl)

        else: # Custom calibration file was provided
            print("controller: Reading provided calibration file...")
            cal_stim = audiomodel.Audio(
                file_path = self.sessionpars['Calibration File'].get(),
                device_id = self.sessionpars['Audio Device ID'].get()
            )

        # Present calibration stimulus
        cal_lvl = cal_stim.db2mag(self.sessionpars['raw_lvl'].get())
        cal_stim.play(level=cal_lvl)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
