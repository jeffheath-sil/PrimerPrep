import gi
import sys

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib

class SplashScreen(Gtk.Dialog):
    def __init__(self):
        super().__init__()
        self.set_decorated(False)  # Removes title bar and buttons
        self.connect("destroy", Gtk.main_quit)

        # Load image
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file("PrimerPrepSplash.png")
        except Exception as e:
            print(f"Error loading image: {e}")
            Gtk.main_quit()
            sys.exit()  # Image not found, just exit the script
        # Resize window to match image size
        self.set_size_request(pixbuf.get_width(), pixbuf.get_height())
        
        # Add image to dialog content area
        self.image = Gtk.Image.new_from_pixbuf(pixbuf)
        content_area = self.get_content_area()
        content_area.add(self.image)
        
        # Center the dialog on the screen and display it
        self.set_position(Gtk.WindowPosition.CENTER)
        self.show_all()

        # Close the dialog after 150 seconds
        GLib.timeout_add_seconds(150, self.close_splash)
    
    def close_splash(self):
        self.destroy()
        Gtk.main_quit()

if __name__ == "__main__":
    win = SplashScreen()
    Gtk.main()
