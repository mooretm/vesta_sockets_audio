""" Calibration dialog class
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# Import system packages
import os


#########
# BEGIN #
#########
class CalibrationDialog(tk.Toplevel):
    def __init__(self, parent, sessionpars, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.sessionpars = sessionpars

        # Window setup
        self.withdraw()
        self.focus()
        self.title("Calibration")
        self.grab_set()


        ##########
        # Frames #
        ##########
        # Options for label frames
        options = {'padx':10, 'pady':10}
        options_small = {'padx':2.5, 'pady':2.5}

        # Choose calibration file
        lf_load = ttk.LabelFrame(self, text="Calibration File")
        lf_load.grid(column=5, columnspan=10, row=5, **options)

        # Presentation controls
        lf_playback = ttk.Labelframe(self, text='Playback Controls')
        lf_playback.grid(column=5, row=10, **options, sticky='w')

        # Calibration selection controls #
        # Define variables for file path and radio button value
        self.cal_path = tk.StringVar(value='Please choose a calibration stimulus file')
        self.cal_var = tk.StringVar()
        

        ##############################
        # Calibration File Selection #
        ##############################
        # Radio buttons
        # Default white noise stimulus
        rad_wgn = ttk.Radiobutton(lf_load, text="White Noise", takefocus=0,
            variable=self.cal_var, value='wgn', command=self._cal_type)
        rad_wgn.grid(column=5, row=0, columnspan=10, sticky='w', 
            **options_small)

        # Upload custom calibration stimulus
        rad_custom = ttk.Radiobutton(lf_load, text="Custom File", takefocus=0,
            variable=self.cal_var, value='custom', command=self._cal_type)
        rad_custom.grid(column=5, row=1, columnspan=10, sticky='w', 
            **options_small)

        # File path
        self.lbl_calfile1 = ttk.Label(lf_load, text='File:', state='disabled')
        self.lbl_calfile1.grid(column=5, row=5, sticky='w', **options_small)
        self.lbl_calfile2 = ttk.Label(lf_load, textvariable=self.cal_path, borderwidth=2, 
            relief="solid", width=60, state='disabled')
        self.lbl_calfile2.grid(column=10, row=5, sticky='w', **options_small)

        # Browse button
        self.btn_browse = ttk.Button(lf_load, text="Browse", state='disabled',
            takefocus=0, command=self._load_cal)
        self.btn_browse.grid(column=10, row=10, sticky='w', 
            **options_small)
        
        # Set default calibration file type
        if self.sessionpars['Calibration File'].get() == 'cal_stim.wav':
            self.cal_var.set('wgn')
            self._set_custom_cntrls_status('disabled')
        else:
            self.cal_var.set('custom')
            self.cal_path.set(os.path.basename(
                self.sessionpars['Calibration File'].get()))
            self._set_custom_cntrls_status('enabled')


        #########################
        # Presentation controls #
        #########################
        # Scaling factor
        ttk.Label(lf_playback, text="Offset (dB FS):").grid(
            column=5, row=5, sticky='e', **options_small)
        ent_slm = ttk.Entry(lf_playback, textvariable=self.sessionpars['scaling_factor'],
            width=6)
        ent_slm.grid(column=10, row=5, sticky='w', **options_small)
 
        # Play calibration stimulus
        ttk.Label(lf_playback, text="Calibration Stimulus:").grid(
            column=5, row=10, sticky='e', **options_small)
        btn_play = ttk.Button(lf_playback, text="Play", command=self._on_play)
        btn_play.grid(column=10, row=10, sticky='w', **options_small)
        #btn_play.focus()

        # Stop calibration stimulus
        ttk.Label(lf_playback, text="Calibration Stimulus:").grid(
            column=5, row=15, sticky='e', **options_small)
        btn_play = ttk.Button(lf_playback, text="Stop", command=self._on_stop)
        btn_play.grid(column=10, row=15, sticky='w', **options_small)


        # Submit button
        # self.btn_submit = ttk.Button(lf_record, text="Submit", 
        #     command=self._on_submit, state='disabled')
        # self.btn_submit.grid(column=5, columnspan=10, row=20, **options_small)


        # Center calibration window dialog
        self.center_window()


    #############
    # FUNCTIONS #
    #############
    def center_window(self):
        """ Center calibration dialog window
        """
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        self.geometry("+%d+%d" % (x, y))
        self.deiconify()


    def _set_custom_cntrls_status(self, state):
        """ Enable or disable custom cal file controls
        """
        self.lbl_calfile1.config(state=state)
        self.lbl_calfile2.config(state=state)
        self.btn_browse.config(state=state)


    def _cal_type(self):
        """ Radio button functions for choosing cal type
        """
        # Custom calibration file
        if self.cal_var.get() == 'custom':
            # Enable file browsing controls
            self._set_custom_cntrls_status('enabled')

        # Default white noise
        elif self.cal_var.get() == 'wgn':
            # Assign default cal file
            self.sessionpars['Calibration File'].set('cal_stim.wav')
            # Update path text
            self.cal_path.set('Please choose a calibration stimulus file')
            # Disable custom file controls
            self._set_custom_cntrls_status('disabled')


    def _load_cal(self):
        """ File dialog for custom calibration file
        """
        self.sessionpars['Calibration File'].set(filedialog.askopenfilename())
        self.cal_path.set(
            os.path.basename(self.sessionpars['Calibration File'].get()))


    def _on_play(self):
        """ Send play event to controller
        """
        self.parent.event_generate('<<CalPlay>>')
        #self.btn_submit.config(state='enabled')
        #self.ent_slm.config(state='enabled')


    def _on_stop(self):
        self.parent.event_generate('<<CalStop>>')


    # def _on_submit(self):
    #     """ Send save event to controller
    #     """
    #     print("calibrationview: Sending save event to controller...")
    #     self.parent.event_generate('<<CalibrationSubmit>>')
    #     self.destroy()
