from os import path
import sphinx

__version__ = '1.0.0'
__version_full__ = __version__

def get_html_theme_path():
    """Return list of HTML theme paths."""
    theme_path = path.abspath(path.dirname(path.dirname(__file__)))
    return theme_path

def setup(app):
    app.add_html_theme('sphinx_dg_theme', path.abspath(path.dirname(__file__)))
