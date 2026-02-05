from tkinter import messagebox
import json
import os
import sys

path = f"//zkh/appdata/Raystation/Research/ML/Paritt/Planning_Flow🍃/Planning-Flow" # Change this to where you save Planning-Flow

def setupPath(path):
    """ Set the path and environment """
    sys.path.insert(0, path)
    os.environ["SCRIPT_PATH"] = path

try:
    setupPath(path)
except Exception as e:
    messagebox.showerror("Path Error", f"Error setting up path: {e}")

from src.PlanningFlowApp import PlanningFlowApp

try:
    from raystation import *
except ImportError:
    from connect import *
except ImportError:
    messagebox.showerror("RayStation API not found", "Please run this script within RayStation.")

settings_file = os.path.join(path,'src/setting.json')

try:
    with open(settings_file, 'r') as f:
        settings = json.load(f)
    machine_options = settings["machine_options"]
    beam_energy_list = settings["beam_energy_list"]
    flow_collection_path = settings["flow_collection_path"]
except FileNotFoundError:
    messagebox.showwarning("Settings file not found", f"{settings_file} not found. Using default settings.")
    
    # Default Machine options - modify these to match your RayStation treatment rooms
    machine_options = ['Agility', 'P1']
    
    # Default Beam energy options - modify these to match your RayStation beam energies
    beam_energy_list = ['6', '10', '6 FFF', '10 FFF']
    
    # Default Flow collection path
    flow_collection_path = os.path.join(path,'flow_collection')

if __name__ == "__main__":
    app = PlanningFlowApp(machine_options=machine_options, beam_energy_list=beam_energy_list, flow_collection_path=flow_collection_path)
    app.mainloop()