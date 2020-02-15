import sys
import toga
from toga.style.pack import Pack, CENTER

class WebApp(toga.App):
    def startup(self):
        print('In WebApp.startup')
        self.main_window = toga.MainWindow(title=self.name)
        label1 = toga.Label(
            'Hello from Toga!',
            style=Pack(alignment=CENTER, text_align=CENTER)
        )

        self.main_window.content = label1
        self.main_window.show()

if __name__ == '__main__':
    print('Running Toga app...')
    app = WebApp(formal_name='Web App', app_id='org.beeware.webapp')
    app.main_loop()
    print('Running All done...')
