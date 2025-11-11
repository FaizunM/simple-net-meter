import pystray, time, psutil
from PIL import Image, ImageDraw
from threading import Thread


class TrayApp:
    def __init__(self):
        self.icon = pystray.Icon(
            "Tray App",
            self._create_icon(color=(0, 100, 255)),
            "Aplikasi Tray",
            self._create_menu(),
        )
        self.running = True

        thread = Thread(target=self.background_task, daemon=True)
        thread.start()

    def _create_icon(self, color):
        """Membuat ikon sederhana berbentuk lingkaran biru."""
        image = Image.new("RGB", (128, 128), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((8, 8, 56, 56), fill=color)
        return image

    def _create_menu(self):
        return pystray.Menu(
            pystray.MenuItem("Show", self.show_message),
            pystray.MenuItem("About", self.about),
            pystray.MenuItem("Exit", self.exit_app),
        )

    def show_message(self):
        print("Show Message")

    def about(self):
        print("About")

    def exit_app(self):
        self.running = False
        self.icon.stop()
        print("Exit App")

    def speed_cat(self, number):
        if number > (1024 * 1024 * 1024 * 1024):
            result = number / (1024 * 1024 * 1024 * 1024)
            return f"{result:0.2f} TB/s"
        if number > (1024 * 1024 * 1024):
            result = number / (1024 * 1024 * 1024)
            return f"{result:0.2f} GB/s"
        if number > (1024 * 1024):
            result = number / (1024 * 1024)
            return f"{result:0.2f} MB/s"
        if number > (1024):
            result = number / (1024)
            return f"{result:0.2f} KB/s"
        if number < 1024:
            return f"{number:0.2f} B/s"

    def background_task(self):
        while self.running:
            old_net = psutil.net_io_counters()
            time.sleep(1)
            new_net = psutil.net_io_counters()
            download = new_net.bytes_recv - old_net.bytes_recv
            upload = new_net.bytes_sent - old_net.bytes_sent

            if download > upload:
                self.icon.icon = self._create_icon(color=(0, 180, 0))
            else:
                self.icon.icon = self._create_icon(color=(180, 0, 0))


            self.icon.title = f"""Network Speed: 
-> Download: {self.speed_cat(download)}
-> Upload: {self.speed_cat(upload)}
Today: {self.speed_cat(new_net.bytes_recv + new_net.bytes_sent)}"""

    def run(self):
        self.icon.run()


if __name__ == "__main__":
    try:
        app = TrayApp()
        app.run()
    except KeyboardInterrupt:
        app.exit_app()
