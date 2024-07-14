import sys


def resource_path(relative_path):
    try:
        return sys._MEIPASS + relative_path[1::]
    except Exception:
        return relative_path
