from __future__ import annotations
import os
import sys
from datetime import datetime

"""
PyCharm sets PythonPath to the Content Root folder, VSC does not by default, causing import failures

Hence, add this to the VSCode launch config:
"env": {"PYTHONPATH": "${workspaceFolder}:${env:PYTHONPATH}"}

ref: https://stackoverflow.com/questions/53653083/how-to-correctly-set-pythonpath-for-visual-studio-code

Or, use the function below.
"""


def add_python_path(project_dir: str, my_file: str) -> (str, str):
    """
    @param project_dir: enclosing path node (e.g., LogicBank
    @param my_file: callers __file__ variable
    @result (path_was_fixed, path)

    """
    target_last_node = project_dir.lower()
    current_path = os.path.abspath(os.path.dirname(my_file))
    each_last_node = ""
    while each_last_node != target_last_node:
        each_last_node = os.path.basename(os.path.normpath(current_path))
        each_last_node = each_last_node.lower()
        if each_last_node != target_last_node:
            current_path = os.path.dirname(current_path)
            if current_path == "/":
                raise Exception("project_dir not found: " + target_last_node)

    sys_path = ""
    required_path_present = False
    for each_last_node in sys.path:
        sys_path += each_last_node + "\n"
        if each_last_node == current_path:
            required_path_present = True
    if not required_path_present:
        result_was_fixed = "Fixing path (so can run from terminal)"
        sys.path.append(current_path)
    else:
        pass
        result_was_fixed = "NOT Fixing path (default PyCharm, set in VSC Launch Config)"
    return result_was_fixed, get_run_environment_info()


def get_sys_path():
    """
    :return: readable, multi-line output of Python Path
    """
    sys_path = ""
    for each_node in sys.path:
        sys_path += each_node + "\n"
    return sys_path


def get_run_environment_info():
    """
    @return: readable, multi-line output of Python environment
    """
    cwd = os.getcwd()   # eg, /Users/val/dev/logicbank/nw/tests
    run_environment_info = "Run Environment info...\n\n"
    run_environment_info += " Current Working Directory: " + cwd + "\n\n"
    run_environment_info += "sys.path: (Python imports)\n" + get_sys_path() + "\n"
    run_environment_info += "From: " + sys.argv[0] + "\n\n"
    run_environment_info += "Using Python: " + sys.version + "\n\n"
    run_environment_info += "At: " + str(datetime.now()) + "\n\n"
    return run_environment_info

if __name__ == "__main__":
    # execute only if run as a script
    print("\nRunning, sys_path:\n" + get_sys_path())
    add_python_path(project_dir="LogicBankUtils", my_file=__file__)
    print("\n\nCompleted: result is\n" + get_sys_path())
