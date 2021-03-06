"""
history.py
Author: Sam Hogan
CSC440
"""

import os
import shutil
import datetime
from wiki.web import current_wiki


def update_history(url):
    # the directory containing past versions of the page
    directory_path = current_wiki.history_path(url)

    # if the path doesn't exist, create it (page is first saved/created)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    history_files = []

    for filename in os.listdir(directory_path):
        if filename.endswith(".md"):
            history_files.append(filename)
            continue
        else:
            continue

    # sort in numerical order
    history_files.sort()

    # now reverse to edit/rename the oldest files first
    history_files.reverse()

    page_path = current_wiki.path(url)

    date_time_string = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

    # copy the newest version of the page as
    shutil.copyfile(page_path, directory_path + "/" + date_time_string + ".md")


# removes .md from file name to get the history id
def get_history_id(file_name):
    return file_name[:-3]


# converts the history id of an archive page to a readable date/time
def get_date_from_id(hid):
    return hid


# formats the history id (containing date and time of edit) into a readable format for display
def format_history_id(hid):
    time_str = hid[11:].replace("-", ":")
    if time_str[0] == "0":
        time_str = time_str[1:]

    return hid[:10] + " " + time_str
