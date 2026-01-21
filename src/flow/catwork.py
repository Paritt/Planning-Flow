import tkinter as tk
from tkinter import ttk
import os

# Try to import PIL for animated GIF support
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class CatWork:
    """Display an animated GIF with a message in a popup window."""
    
    def __init__(self, message="Working...", gif_name=None, previous_cat=None):
        """Initialize CatWork with a custom message."""
        self.message = message
        self.gif_name = gif_name
        self.window = None
        self.gif_label = None
        self.gif_frames = []
        self.frame_index = 0
        self.frame_delay = 100
        if previous_cat:
            previous_cat.stop()
        self.start()
        
    def start(self):
        """Show the popup window."""
        if self.window is not None:
            return
        
        # Create and configure window
        self.window = tk.Toplevel()
        self.window.title("Processing")
        self.window.geometry("400x450")
        self.window.resizable(False, False)
        self._center_window()
        
        # Message label
        ttk.Label(
            self.window,
            text=self.message,
            font=("Arial", 14, "bold"),
            justify="center"
        ).pack(pady=20)
        
        # GIF display area
        self.gif_label = tk.Label(self.window, bg="white")
        self.gif_label.pack(expand=True, fill="both", padx=20, pady=10)
        
        # Check if PIL is available
        if not PIL_AVAILABLE:
            self.fallback()
            self.window.attributes('-topmost', True)
            return
        
        # Load and display GIF
        gif_path = self._get_gif_path()
        print("GIF Path:", gif_path)
        if os.path.exists(gif_path):
            try:
                self._load_gif(gif_path)
                if self.gif_frames:
                    self._animate()
                else:
                    self._show_message("🐱 Working... 🐱\n\nFailed to load GIF frames")
            except Exception as e:
                self._show_message(f"🐱 Working... 🐱\n\nError loading GIF:\n{str(e)}")
        else:
            self._show_message(f"🐱 Working... 🐱\n\nGIF not found:\n{gif_path}")
        
        self.window.attributes('-topmost', True)
    
    def fallback(self):
        """Fallback behavior when PIL is not available. Override this method to customize."""
        self._show_message("🐱 Working... 🐱\n\nPIL/Pillow not installed\nPlease install: pip install Pillow")
    
    def stop(self):
        """Close the popup window."""
        if self.window:
            self.window.destroy()
            self.window = None
            self.gif_label = None
            self.gif_frames = []
    
    def _center_window(self):
        """Center the window on screen."""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() - 400) // 2
        y = (self.window.winfo_screenheight() - 450) // 2
        self.window.geometry(f"400x450+{x}+{y}")
    
    def _get_gif_path(self):
        """Get the path to the GIF file."""
        script_dir = os.path.dirname(os.path.abspath(__file__))  # src/flow/
        parent_dir = os.path.dirname(script_dir)  # src/
        grandparent_dir = os.path.dirname(parent_dir)  # Planning-Flow/
        return os.path.join(grandparent_dir, "src\\flow\\GIFs", self.gif_name) if self.gif_name else os.path.join(grandparent_dir, "src\\flow\\GIFs", "cat_work.gif")
    
    def _load_gif(self, gif_path):
        """Load all frames from the GIF file."""
        self.gif_frames = []
        gif = Image.open(gif_path)
        
        # Extract frames
        try:
            while True:
                frame = gif.copy()
                if frame.mode != 'RGBA':
                    frame = frame.convert('RGBA')
                self.gif_frames.append(ImageTk.PhotoImage(frame))
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass
        
        # Get frame delay
        try:
            self.frame_delay = gif.info.get('duration', 100)
        except:
            self.frame_delay = 100
    
    def _animate(self):
        """Animate the GIF frames."""
        if not self.window or not self.gif_frames:
            return
        
        self.gif_label.config(image=self.gif_frames[self.frame_index])
        self.frame_index = (self.frame_index + 1) % len(self.gif_frames)
        self.window.after(self.frame_delay, self._animate)
    
    def _show_message(self, text):
        """Display a text message instead of GIF."""
        self.gif_label.config(
            text=text,
            font=("Arial", 12),
            justify="center"
        )


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    cat = CatWork(message="Processing your request...")
    cat.start()
    
    def finish():
        cat.stop()
        root.quit()
    
    root.after(5000, finish)
    root.mainloop()
