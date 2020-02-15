from browser import window

from .window import Window


class MainWindow(Window):
    def create(self):
        self.native = window
        self.body = window.document.body

class App:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        self.create()

    def create(self):
        pass

    def set_on_exit(self, value):
        pass

    def main_loop(self):
        self.interface.startup()

    def set_main_window(self, window):
        pass

