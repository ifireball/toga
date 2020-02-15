import unittest

from webserve.wsgi import ModuleSender

class ModuleSendingTests(unittest.TestCase):
    PATH_TO_MODULE_CASES = [
        ('/', None),
        ('/foo', None),
        ('/foo/', None),
        ('/index.html', None),
        ('/toga.py', 'toga'),
        ('/toga/__init__.py', 'toga'),
        ('/toga/app.py', 'toga.app'),
        ('/toga/app/__init__.py', 'toga.app'),
        ('/__init__.py', None),
    ]

    def test_module_from_path_info(self):
        for path_info, expected_module in self.PATH_TO_MODULE_CASES:
            out = ModuleSender.module_from_path_info(path_info)
            self.assertEqual(out, expected_module)

    SAME_PY_FILE_CASES = [
        ('/home/toga/src/core/toga/__init__.py', '/toga.py', False),
        ('/home/toga/src/core/toga/__init__.py', '/toga/__init__.py', True),
    ]

    def test_is_same_py_file(self):
        for local_path, req_path, expected in self.SAME_PY_FILE_CASES:
            out = ModuleSender.is_same_py_file(local_path, req_path)
            self.assertEqual(out, expected)

    TEST_WHITELIST = ['toga', 'toga.*']
    IS_MODULE_WL_CASES = [
        (TEST_WHITELIST, 'toga', True),
        (TEST_WHITELIST, 'toga.style', True),
        (TEST_WHITELIST, 'toga_gtk', False),
        (TEST_WHITELIST, 'sys', False),
    ]

    def test_is_module_whitelisted(self):
        for whitelist, module, expected in self.IS_MODULE_WL_CASES:
            ms = ModuleSender(whitelist)
            out = ms.is_module_whitelisted(module)
            self.assertEqual(out, expected)
