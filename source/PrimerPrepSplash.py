import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib

class SplashScreen(Gtk.Dialog):
    def __init__(self):
        super().__init__()
        self.set_decorated(False)  # Removes title bar and buttons
        self.connect("destroy", Gtk.main_quit)
        self.set_icon_from_file('PrimerPrep.ico')

        # Load image
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file("PrimerPrepSplash.png")
        except Exception as e:
            print(f"Error loading image: {e}")
            Gtk.main_quit()
            sys.exit()  # Exit the script

        self.image = Gtk.Image.new_from_pixbuf(pixbuf)

        # Resize window to match image size
        self.set_size_request(pixbuf.get_width(), pixbuf.get_height())

        # Get monitor resolution
        display = Gdk.Display.get_default()
        monitor = display.get_primary_monitor()
        geometry = monitor.get_geometry()
        width_px = geometry.width
        height_px = geometry.height

        # Calculate position to center window
        window_x = (width_px - pixbuf.get_width()) // 2
        window_y = (height_px - pixbuf.get_height()) // 2

        # Set dialog position
        self.move(window_x, window_y)

        # Add image to dialog content area
        content_area = self.get_content_area()
        content_area.add(self.image)
        self.show_all()

        # Close the dialog after 150 seconds
        GLib.timeout_add_seconds(150, self.close_splash)

    def close_splash(self):
        self.destroy()
        Gtk.main_quit()

if __name__ == "__main__":
    win = SplashScreen()
    Gtk.main()
