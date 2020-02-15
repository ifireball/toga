from pkg_resources import resource_string as resource_bytes
from pathlib import PurePath
from importlib.util import find_spec
from fnmatch import fnmatchcase

def app(environ, start_response):
    path = environ['PATH_INFO']
    if path == '/' or path == '':
        return send_index(environ, start_response)
    elif path.startswith('/client_python/'):
        return send_client(environ, start_response)
    try:
        return module_sender(environ, start_response)
    except ModuleNotFoundError:
        pass
    return send_404(environ, start_response)

def send_index(environ, start_response):
    status = '200 OK'  # HTTP Status
    headers = [('Content-type', 'text/html; charset=utf-8')]  # HTTP Headers
    start_response(status, headers)

    index_page = resource_bytes('webserve', 'index.html')
    return [index_page]

def send_client(environ, start_response):
    resource = environ['PATH_INFO']
    if resource.startswith('/'):
        resource = resource[1:]
    try:
        page = resource_bytes('webserve', resource)
    except FileNotFoundError:
        return send_404(environ, start_response)

    status = '200 OK'  # HTTP Status
    headers = [('Content-type', 'text/plain; charset=utf-8')]  # HTTP Headers
    start_response(status, headers)
    return [page]

def send_404(environ, start_response):
    status = '404 NOT FOUND'  # HTTP Status
    headers = [('Content-type', 'text/html; charset=utf-8')]  # HTTP Headers
    start_response(status, headers)

    return [b"<h1>Not found!</h1>"]

class ModuleSender:
    """WSGI app that sens Python modules from the local host to a Brython
    instance running in a remote broswer
    """
    def __init__(self, module_whitelist=None):
        self.module_whitelist = module_whitelist or []

    def __call__(self, environ, start_response):
        """Send the Python module references by given path if white listed

        If module is not found or not whitelisted, will raise a
        ModuleNotfoundError
        """
        path_info = environ['PATH_INFO']
        mod_name = self.module_from_path_info(path_info)
        if mod_name is None or not self.is_module_whitelisted(mod_name):
            raise ModuleNotFoundError(path_info)
        mod_spec = find_spec(mod_name)
        if mod_spec is None or not self.is_same_py_file(mod_spec.origin, path_info):
            raise ModuleNotFoundError(path_info)
        return self.stream_module(mod_spec, start_response)

    def stream_module(self, mod_spec, start_response):
        data = mod_spec.loader.get_data(mod_spec.origin)
        status = '200 OK'  # HTTP Status
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        return [data]

    def is_module_whitelisted(self, module):
        """Returns wither a given module name is white listed
        """
        return next((
            True for pattern in self.module_whitelist if fnmatchcase(module, pattern)
        ), False)

    @staticmethod
    def is_same_py_file(local_path, req_path):
        """Return wither a local module file is indeed the file requested by
        Brython
        """
        if not req_path.startswith('/'):
            req_path = '/' + req_path
        return local_path.endswith(req_path)

    @staticmethod
    def module_from_path_info(path):
        """For a given path_info coming for a web request, return the name of
        the desired Python module, or None if path is not pointing at a module
        """
        po = PurePath(path)
        if po.suffix != '.py':
            return
        if po.stem == '__init__':
            po = po.parent
        if not po.stem:
            return
        pparts = po.parent.parts
        if po.is_absolute():
            pparts = pparts[1:]
        return '.'.join(pparts + (po.stem,))

module_sender = ModuleSender([
    'toga', 'toga.*',
    'travertino', 'travertino.*',
    'toga_brython', 'toga_brython.*'
])
