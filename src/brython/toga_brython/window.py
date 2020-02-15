class BrythonViewport:
    def __init__(self, native_window):
        self.native_window = native_window
        self.dpi = 96  # FIXME This is almost certainly wrong...

    @property
    def width(self):
        return self.native_window.innerWidth

    @property
    def height(self):
        return self.native_window.innerHeight

class Window():
    def __init__(self, interface):
        self.interface = interface
        self.create()
        self.configure()

    def create(self):
        # TODO: pop up a new browser window, populate self.native and self.body
        pass

    def configure(self):
        self.native.bind('resize', self.brython_on_resize)

    def brython_on_resize(self, event):
        if self.interface.content:
            self.interface.content.refresh()

    def create_toolbar(self):
        pass

    def set_content(self, widget):
        self.body.innerHTML = widget.create_html()
        widget.native = self.native.document.getElementById(widget.html_id)
        widget.viewport = BrythonViewport(self.native)

    def set_title(self, title):
        pass

    def set_position(self, position):
        pass

    def set_size(self, size):
        pass

    def set_app(self, app):
        pass

    def show(self):
        self.interface.factory.not_implemented('Window.show()')
