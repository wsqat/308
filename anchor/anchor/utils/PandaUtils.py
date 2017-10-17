import re
import os
import json
import glob
import datetime

RE_ADDRESS = r"province=(.*?)\&"
RE_ROOM_DETAIL = r"'roominfo': ({.*?})"
RE_HTML_MARKER = r"<[^>]*>"

def get_address(url):

    return re.search(RE_ADDRESS, url).group(1)


def get_room_detail_json(text):
    return json.loads(re.findall(RE_ROOM_DETAIL, text)[0] + "}")


def replace_html_marker(text):
    return re.sub(RE_HTML_MARKER, "", text, flags=re.DOTALL)


def get_file_name(save_path):

    filename = datetime.datetime.now().strftime('%Y-%m-%d')

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_count = len(glob.glob(save_path + r"%s*" % filename))

    filename = save_path + filename + "-" + str(file_count).zfill(3) + ".csv"

    return filename
