from tkinter import messagebox
import json
from src.PlanningFlowApp import PlanningFlowApp

try:
    from raystation import *
except ImportError:
    from connect import *
except ImportError:
    messagebox.showerror("RayStation API not found", "Please run this script within RayStation.")

settings_file = 'src/setting.json'

try:
    with open(settings_file, 'r') as f:
        settings = json.load(f)
    machine_options = settings["machine_options"]
    beam_energy_list = settings["beam_energy_list"]
except FileNotFoundError:
    messagebox.showwarning("Settings file not found", f"{settings_file} not found. Using default settings.")
    
    # Default Machine options - modify these to match your RayStation treatment rooms
    machine_options = ['Agility', 'P1']
    
    # Default Beam energy options - modify these to match your RayStation beam energies
    beam_energy_list = ['6', '10', '6 FFF', '10 FFF']


if __name__ == "__main__":
    app = PlanningFlowApp(machine_options=machine_options, beam_energy_list=beam_energy_list)
    app.mainloop()
