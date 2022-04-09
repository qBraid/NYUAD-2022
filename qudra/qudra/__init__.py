"""
qudra: quantum energy management
"""
import os

from .optimizers import *

with open(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "VERSION.txt")), "r"
) as _ver_file:
    __version__ = _ver_file.read().rstrip()

__author__ = "Asil Qraini, Fouad Afiouni, Gargi Chandrakar, Nurgazy Seidaliev, Sahar Ben Rached, Salem Al Haddad, Sarthak Prasad Malla. Mentors: Akash Kant, Shantanu Jha."
__credits__ = "qudra dev team"
