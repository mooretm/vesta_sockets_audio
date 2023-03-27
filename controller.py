""" Socket Audio Player. Audio player that receives files and commands
    via TCP/IP. 

    Written for use with Vulcan interface. Necessary because Vulcan 
    requires a version of Python that is not supposed by ASIO. 

    Written by: Travis M. Moore
    Created: Feb 28, 2023
    Last edited: March 27, 2023
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk

# Import system packages
import os
import sys

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
from views import audioview
from views import calibrationview
# Server imports
from server import app_server


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

        # Load current session parameters from file
        # Or load defaults if file does not exist yet
        self.sessionpars_model = sessionmodel.SessionParsModel()
        self._load_sessionpars()

        # Load main view
        self.main_frame = mainview.MainFrame(self)
        self.main_frame.grid(row=5, column=5)

        # Load menus
        menu = mainmenu.MainMenu(self)
        self.config(menu=menu)

        # Create callback dictionary
        event_callbacks = {
            # File menu
            '<<FileQuit>>': lambda _: self._quit(),

            # Server menu
            '<<ServerStartServer>>': lambda _: self.start_server(),

            # Tools menu
            '<<ToolsAudioSettings>>': lambda _: self._show_audio_dialog(),
            '<<ToolsCalibration>>': lambda _: self._show_calibration_dialog(),

            # Help menu
            '<<Help>>': lambda _: self._show_help(),

            # Calibration dialog commands
            '<<CalPlay>>': lambda _: self.play_calibration_file(),
            '<<CalStop>>': lambda _: self.stop_calibration_file(),

            # Audio dialog commands
            '<<AudioDialogSubmit>>': lambda _: self._save_sessionpars(),
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
        self.destroy()


    def resource_path(self, relative_path):
        """ Get the absolute path to compiled resources
        """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


    ###########################
    # Session Model Functions #
    ###########################
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


    #########################
    # Server Menu Functions #
    #########################
    def start_server(self):
        """ Create server and begin listening.
        """
        self.server = app_server.Server(
            audio_device=self.sessionpars["Audio Device ID"].get()
            )


    ########################
    # Tools Menu Functions #
    ########################
    def _show_audio_dialog(self):
        """ Show audio settings dialog
        """
        print("\ncontroller: Calling audio dialog...")
        audioview.AudioDialog(self, self.sessionpars)

    def _show_calibration_dialog(self):
        """ Display the calibration dialog window
        """
        print("\ncontroller: Calling calibration dialog...")
        calibrationview.CalibrationDialog(self, self.sessionpars)


    ################################
    # Calibration Dialog Functions #
    ################################
    def _get_cal_file(self):
        """ Load specified calibration file
        """
        print("audiomodel: Locating calibration file...")
        if self.sessionpars['Calibration File'].get() == 'cal_stim.wav':
            self.cal_file = self.resource_path('cal_stim.wav')
            file_exists = os.access(self.cal_file, os.F_OK)
            if not file_exists:
                self.cal_file = '.\\assets\\cal_stim.wav'
        else: # Custom file was provided
            self.cal_file = self.sessionpars['Calibration File'].get()

        print(f"controller: Using {self.cal_file}")


    def play_calibration_file(self):
        """ Load calibration file and present
        """
        # Get calibration file
        self._get_cal_file()

        # Present calibration file
        self.cal = audiomodel.Audio(file_path=self.cal_file)
        self.cal.play(
            level=self.sessionpars['scaling_factor'].get(),
            device_id=self.sessionpars['Audio Device ID'].get()
        )


    def stop_calibration_file(self):
        """ Stop playback of calibration file
        """
        try:
            self.cal.stop()
        except AttributeError:
            print("controller: No calibration stimulus found!")
        


    #######################
    # Help Menu Functions #
    #######################
    def _show_help(self):
        """ Create html help file and display in default browser
        """
        print("\ncontroller: Looking for help file in compiled " +
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


if __name__ == "__main__":
    app = Application()
    app.mainloop()
