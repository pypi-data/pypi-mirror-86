"""
usefulCommandLineTools

A Python Module with useful functions for creating a command line tool!
"""
from os import system, name
import uclt.Text

__version__ = '0.0.1'
__author__ = 'Ariel Khais'
__credits__ = 'So far, none'

def clear():
  # Credit to GeeksForGeeks for the code, I just copy pasted it
  # for windows 
  if name == 'nt': 
    _ = system('cls') 
  
  # for mac and linux(here, os.name is 'posix') 
  else: 
    _ = system('clear')

# Function to print colored text
def ucltPrint(message, fgcolor=None, bgcolor=None, bold=False, faint=False, italic=False, underline=False, blink=False, strikeout=False):
  output = (
    f'{fgcolor if fgcolor else ""}'
    f'{uclt.Text.Types.BOLD if bold else ""}'
    f'{uclt.Text.Types.FAINT if faint else ""}'
    f'{uclt.Text.Types.ITALIC if italic else ""}'
    f'{uclt.Text.Types.UNDERLINE if underline else ""}'
    f'{uclt.Text.Types.BLINK if blink else ""}'
    f'{uclt.Text.Types.CROSSED if strikeout else ""}'
    f'{message}'
    f'{uclt.Text.Types.END}'
  )
  print(output)