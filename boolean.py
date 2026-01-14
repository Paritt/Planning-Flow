import tkinter as tk

def save():
    # Placeholder function for saving the input
    print("Saved")

# Initialize the main window
root = tk.Tk()
root.title("ROI Algebra")
root.geometry("600x400")

# Frame for ROI Algebra
frame = tk.Frame(root)
frame.pack(pady=20)

# Title
title = tk.Label(frame, text="ROI Algebra", font=('Arial', 16))
title.grid(row=0, column=0, columnspan=2)

# Frame for A and B
frame_a_b = tk.Frame(root)
frame_a_b.pack(pady=20)

# ROI A
frame_a = tk.LabelFrame(frame_a_b, text="A", padx=10, pady=10)
frame_a.grid(row=0, column=0, padx=20)
margin_label_a = tk.Label(frame_a, text="Margin")
margin_label_a.grid(row=0, column=0)

expand_a = tk.Radiobutton(frame_a, text="Expand", value=1)
expand_a.grid(row=1, column=0)
contract_a = tk.Radiobutton(frame_a, text="Contract", value=2)
contract_a.grid(row=1, column=1)

# Directional input for ROI A
directions = ['Superior', 'Inferior', 'Right', 'Left', 'Anterior', 'Posterior']
for i, direction in enumerate(directions):
    label = tk.Label(frame_a, text=f"{direction} (cm)")
    label.grid(row=i+2, column=0)
    entry = tk.Entry(frame_a)
    entry.grid(row=i+2, column=1)

# ROI B
frame_b = tk.LabelFrame(frame_a_b, text="B", padx=10, pady=10)
frame_b.grid(row=0, column=1)
margin_label_b = tk.Label(frame_b, text="Margin")
margin_label_b.grid(row=0, column=0)

expand_b = tk.Radiobutton(frame_b, text="Expand", value=1)
expand_b.grid(row=1, column=0)
contract_b = tk.Radiobutton(frame_b, text="Contract", value=2)
contract_b.grid(row=1, column=1)

# Directional input for ROI B
for i, direction in enumerate(directions):
    label = tk.Label(frame_b, text=f"{direction} (cm)")
    label.grid(row=i+2, column=0)
    entry = tk.Entry(frame_b)
    entry.grid(row=i+2, column=1)

# Operations (Union, Intersect, Subtract)
operation_label = tk.Label(root, text="Select Operation:")
operation_label.pack()
operation_frame = tk.Frame(root)
operation_frame.pack()

union_button = tk.Radiobutton(operation_frame, text="Union", value=1)
union_button.grid(row=0, column=0)
intersect_button = tk.Radiobutton(operation_frame, text="Intersect", value=2)
intersect_button.grid(row=0, column=1)
subtract_button = tk.Radiobutton(operation_frame, text="Subtract", value=3)
subtract_button.grid(row=0, column=2)

# Output section
frame_output = tk.LabelFrame(root, text="Output", padx=10, pady=10)
frame_output.pack(pady=20)

output_label = tk.Label(frame_output, text="Margin")
output_label.grid(row=0, column=0)

expand_output = tk.Radiobutton(frame_output, text="Expand", value=1)
expand_output.grid(row=1, column=0)
contract_output = tk.Radiobutton(frame_output, text="Contract", value=2)
contract_output.grid(row=1, column=1)

# Directional input for Output
for i, direction in enumerate(directions):
    label = tk.Label(frame_output, text=f"{direction} (cm)")
    label.grid(row=i+2, column=0)
    entry = tk.Entry(frame_output)
    entry.grid(row=i+2, column=1)

# Save button
save_button = tk.Button(root, text="Save", command=save)
save_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
