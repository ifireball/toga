class Icon:
    EXTENSIONS = ['.png', '.ico']
    SIZES = None

    def __init__(self, interface, path):
        super().__init__()
        self.interface = interface
        self.path = path
