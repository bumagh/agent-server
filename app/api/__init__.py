from flask import Blueprint
from werkzeug.utils import find_modules, import_string


def register_blueprint(folder, app):
    for name in find_modules(folder, recursive=True):
        module = import_string(str(name))
        n = name.split('.')[-1]
        if hasattr(module, n) and isinstance(getattr(module, n), Blueprint):
            app.register_blueprint(getattr(module, n))
