""""
This module contains all the auxillary and/or miscellaneous functions
used by the application. For example datetime functions
"""
from datetime import datetime
import pytz


def current_date():
    """Returns current date formatted as 'Month Day, Year' """
    jamaica = pytz.timezone("America/Jamaica")
    date    = datetime.now(jamaica).strftime("%B %d, %Y")
    return date



