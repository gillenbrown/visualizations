"""plot_copy.py

Moves plots from the "movies/" directory into the "old_movies/
directory. The plots will have a new name of the format
"[time of copy]_[old plot name]". This allows me to save the old plots while
still cleaning up the directory with the best set of plots.

The script is recursive, so it will clean out all the subfolders too.
"""
import sys
import os
import datetime

copy_file = sys.argv[1]

# we will tag the files based on the time they were copied over
time = datetime.datetime.now()
# format the time to be in a nice format
time_str = str(time).replace(" ", "_")

# get the directories where the plots were, and where they should go
movies_dir = os.path.abspath("./movies/")
movies_old_dir = os.path.abspath("./movies_old/")

def move_file(item_name, old_directory, new_directory):
    """Move a file to the correct location. It will be tagged with the time
    the file is moved, as described in the header of this file.

    :param item_name: filename of the file to be moved. This is just the
                      filename, and does not include the directory.
    :param old_directory: directory holding the item_name file.
    :param new_directory: directory to move the file to.
    """
    # add the time to the filename, then move it.
    new_filename = time_str + "_" + item_name
    os.rename(old_directory + os.sep + item_name,
              new_directory + os.sep + new_filename)

move_file(copy_file, movies_dir, movies_old_dir)
