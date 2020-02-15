from wsgiref.simple_server import make_server

from webserve.wsgi import app

def main():
    httpd = make_server('', 8000, app)
    print("Serving HTTP on port 8000...")

    # Respond to requests until process is killed
    httpd.serve_forever()
