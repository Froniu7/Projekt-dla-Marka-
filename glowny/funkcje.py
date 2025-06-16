
import os
import sys


def resource_path_all(relative_path):
    if getattr(sys, 'frozen', False):  # [1]
        base_path = os.path.dirname(sys.executable)  # [2]

    else:
        base_path_all = os.path.dirname(os.path.abspath(__file__))  # [3]
        base_path = os.path.dirname(base_path_all)

    return  os.path.join(base_path, relative_path) # [4]

def resource_path():
    if getattr(sys, 'frozen', False):  # [1]
        base_path = os.path.dirname(sys.executable)  # [2]
    else:
        base_path_all = os.path.dirname(os.path.abspath(__file__))  # [3]
        base_path = os.path.dirname(base_path_all)
    return os.path.join(base_path)  # [4]
