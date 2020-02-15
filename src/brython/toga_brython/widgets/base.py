class Widget:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.viewport = None
        self.native = None
        self.html_id = 'pyo{}'.format(id(self))

    def set_app(self, app):
        pass

    def set_window(self, window):
        pass

    @property
    def container(self):
        pass

    @container.setter
    def container(self, container):
        print('{} container is set to {}'.format(self, container))

    # APPLICATOR

    def set_bounds(self, x, y, width, height):
        self.native.style.position = 'absolute'
        self.native.style.left = '{}px'.format(x)
        self.native.style.top = '{}px'.format(y)
        self.native.style.width = '{}px'.format(width)
        self.native.style.height = '{}px'.format(height)

    def set_alignment(self, alignment):
        self.interface.factory.not_implemented('Widget.set_alignment()')

    def set_hidden(self, hidden):
        self.interface.factory.not_implemented('Widget.set_hidden()')

    def set_font(self, font):
        self.interface.factory.not_implemented('Widget.set_font()')

    def set_color(self, color):
        self.interface.factory.not_implemented('Widget.set_color()')

    def set_background_color(self, color):
        self.interface.factory.not_implemented('Widget.set_background_color()')

    # BACKEND SPECIFIC

    def create_html(self):
        return (
            '<div id="{}" style="background: lightgreen;">'
            'Widget not implemented'
            '</div>'
        ).format(self.html_id)
