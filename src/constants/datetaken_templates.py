""" The files whose name coincides with this format will be taken into account to fix their metadata, as long as the "auto" parameter is passed to the script. 

The files whose name coincides with this format will be taken into account to fix their metadata, as long as the "auto" parameter is passed to the script. The file suffix is not taken into account, that is, if we have, for example, the format VID_%Y%m%d, the files "VID_20150618 copy.jpg", "VID_20150618(1).jpg", "VID_20150618jkcdkjjkd.jpg" will also be valid to get its dates.

It is appropriate that the list always go from the most precise format to least one, since the first format that matches will be the one used for the file. It should also be noted that the algorithm is not case sensitive.

To check the possible options to parse, check the table here https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
"""
from datetime import datetime

FILENAMES = [
    "Screenshot-%Y-%m-%d-%H-%M-%S",
    "Screenshot-%Y%m%d-%H%M%S",
    "Screenshot_%Y-%m-%d-%H-%M-%S",
    "Screenshot_%Y%m%d-%H%M%S",
    "IMG_%Y%m%d_%H%M%S",
    "IMG-%Y%m%d-WA",
    "VID-%Y%m%d-WA",
    "VID_%Y%m%d_%H%M%S",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H.%M.%S",
    "IMG_%Y%m%d",
    "VID_%Y%m%d",
]

FILENAME_DATE_MIN = 1820
FILENAME_DATE_MAX = datetime.now().year + 5
