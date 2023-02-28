""" Main view for Socket Audio Player
"""

###########
# Imports #
###########
# Import GUI packages
from tkinter import ttk


#########
# BEGIN #
#########
class MainFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Populate frame with widgets
        self.draw_widgets()


    def draw_widgets(self):
        """ Populate the main view with all widgets
        """
        ##########
        # Styles #
        ##########
        style = ttk.Style()
        style.configure('B.TLabel', font=("", 14))
        style.configure('trial.TLabel', font=("", 12))
        style.configure('start.TButton', font=("", 14), foreground='green')
        style.configure('B.TButton', font=("", 14))
        style.configure('B.TLabelframe.Label', font=("", 14), foreground='blue')
        style.configure('B.TLabelframe', font=("", 14), foreground='blue')
        style.configure('white.TLabel', font=("", 12), background='white')


        ##################
        # Create Widgets #
        ##################
        options = {'padx':10, 'pady':10}

        # Main container
        frm_main = ttk.Frame(self)
        frm_main.grid(column=5, row=5, **options)

        ttk.Label(frm_main, text="Socket Audio Player", style='B.TLabel'
                  ).grid(row=5, column=5)

        lfrm_note = ttk.LabelFrame(frm_main, text="Note:")
        lfrm_note.grid(row=10, column=5, pady=10)

        ttk.Label(lfrm_note, text="This window must remain open for audio playback!", 
                  style='TLabel'
                  ).grid(row=5, column=5, **options)
