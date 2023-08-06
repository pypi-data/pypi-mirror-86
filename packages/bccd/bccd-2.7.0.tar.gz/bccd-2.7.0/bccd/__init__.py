import os 

__all__ = ['gui','backend']
__version__ = '2.7.0'
__author__ = 'Derek Fujimoto'

from bccd.backend.fits import fits

logger_name = 'bccd'
icon_path = os.path.join(os.path.dirname(__file__),'images','icon.gif')

from bccd.gui.bccd import bccd

def main():
    bccd()
