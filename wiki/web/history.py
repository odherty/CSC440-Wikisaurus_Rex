import os
from wiki.web import current_wiki



def update_history(url):
    directory_path = current_wiki.history_path(url)

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

    for hf in history_files:
        history_id = int(hf[:-3])  # remove .md to get the id number

        # increment id by one and rename this history file
        new_id = history_id + 1
        os.rename(directory_path+"/"+hf, directory_path+"/"+str(new_id)+".md")

    # now save the version of the page before this edit as the most recent history version

    page_path = current_wiki.path(url)
    os.rename(page_path, directory_path + "/1.md")

