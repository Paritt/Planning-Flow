import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class VMAT_beam_setting_Window:
    """Create a section for designing flow steps with labels for flow/user and Save Flow button."""
    """Open a new window for VMAT beam settings."""
    def __init__(self, parent, designer):
        self.designer = designer
        self.beam_window = tk.Toplevel(parent)
        self.beam_window.title("VMAT Beam Settings")
        self.beam_window.geometry("800x500")
        # Bold Title Label
        title_label = tk.Label(self.beam_window, text="VMAT Beam Settings", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Beams tree with scrollbar
        beam_tree_frame = ttk.Frame(self.beam_window)
        beam_tree_frame.pack(pady=5, fill="both", expand=True)
        
        beam_tree_scroll_y = ttk.Scrollbar(beam_tree_frame, orient="vertical")
        beam_tree_scroll_x = ttk.Scrollbar(beam_tree_frame, orient="horizontal")
        
        self.beam_tree = ttk.Treeview(beam_tree_frame, columns=("Beam name", "Energy [MV]","Gantry Start [deg]", "Gantry Stop [deg]", "Rotation", "Couch [deg]"), 
                                        show="headings", yscrollcommand=beam_tree_scroll_y.set, xscrollcommand=beam_tree_scroll_x.set)
        
        beam_tree_scroll_y.config(command=self.beam_tree.yview)
        beam_tree_scroll_x.config(command=self.beam_tree.xview)
        
        self.beam_tree.heading("Beam name", text="Beam name")
        self.beam_tree.heading("Energy [MV]", text="Energy [MV]")
        self.beam_tree.heading("Gantry Start [deg]", text="Gantry Start [deg]")
        self.beam_tree.heading("Gantry Stop [deg]", text="Gantry Stop [deg]")
        self.beam_tree.heading("Rotation", text="Rotation")
        self.beam_tree.heading("Couch [deg]", text="Couch [deg]")
        
        self.beam_tree.column("Beam name", width=100)
        self.beam_tree.column("Energy [MV]", width=50)
        self.beam_tree.column("Gantry Start [deg]", width=50)
        self.beam_tree.column("Gantry Stop [deg]", width=50)
        self.beam_tree.column("Rotation", width=50)
        self.beam_tree.column("Couch [deg]", width=50)
        
        self.beam_tree.grid(row=0, column=0, sticky="nsew")
        beam_tree_scroll_y.grid(row=0, column=1, sticky="ns")
        beam_tree_scroll_x.grid(row=1, column=0, sticky="ew")
        beam_tree_frame.grid_rowconfigure(0, weight=1)
        beam_tree_frame.grid_columnconfigure(0, weight=1)
        
        # Add Beam Button
        self.add_beam_btn = ttk.Button(self.beam_window, text="Add Beam", command=lambda: self.show_step_info("Add Beam"))
        self.add_beam_btn.pack(side="left", padx=5, pady=5)
        # Remove Beam Button
        self.remove_beam_btn = ttk.Button(self.beam_window, text="Remove Selected Beam", command=lambda: self.show_step_info("Remove Beam"))
        self.remove_beam_btn.pack(side="left", padx=5, pady=5)
        # Edit Beam Button
        self.edit_beam_btn = ttk.Button(self.beam_window, text="Edit Selected Beam", command=lambda: self.show_step_info("Edit Beam"))
        self.edit_beam_btn.pack(side="left", padx=5, pady=5)
        # Save Button
        self.save_beam_btn = ttk.Button(self.beam_window, text="Save", command=lambda: self.show_step_info("Beam Settings Saved"))
        self.save_beam_btn.pack(side="left", padx=5, pady=5)
        # Close Button
        close_btn = ttk.Button(self.beam_window, text="Close", command=self.beam_window.destroy)
        close_btn.pack(pady=10)
        
    def show_step_info(self, message):
        """Display a message box with step information."""
        messagebox.showinfo("Step Information", message)
