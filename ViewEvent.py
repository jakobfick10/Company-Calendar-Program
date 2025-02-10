#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 23:06:57 2024

@author: jakobfick
"""

import tkinter as tk

class viewEventFrame(tk.Frame):
    
    # Constructor
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.event_id = None
        
        # Creating the label that will display the event information to the user
        self.instructions = tk.Label(self, justify='left', text='')
        self.instructions.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        
        #The button that will cremove the selected event from the database
        self.remove_Button = tk.Button(self, text="Remove")
        self.remove_Button.grid(row=1, column=0, padx=10, pady=10)
        
        #The button that will let the user exit the current screen
        exit_Button = tk.Button(self, text="Exit", command=self.controller.show_dashboard)
        exit_Button.grid(row=1, column=2, padx=10, pady=10)
        
    def set_info(self, event_info, event_id):
        print("set_info")
        self.instructions.config(text=event_info)
        self.event_id = event_id
        print(self.event_id)
        self.remove_Button.config(command=lambda e_id=self.event_id: self.controller.delete_event_by_id(e_id))
        
        