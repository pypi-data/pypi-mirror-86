"""
Utility script for easy access to most of the VEnCode scripts and tests.
Example on how to use in command-line:
>python process.py run_tests
"""

import sys
sys.path.append("..")

import argparse
from difflib import get_close_matches

from VEnCode import tests
from VEnCode.scripts import get_vencodes as get_v
from VEnCode.scripts import get_vencodes_fantom as get_v_f


def run_tests(args=None):
    """
    Runs the test suite for the module.
    """
    kwargs_new = parse_unknown_args(args, 0)
    tests.run_all_tests(**kwargs_new)


def get_vencodes(args=None):
    kwargs_new = parse_unknown_args(args, 2)
    get_v.main(args[0], args[1], **kwargs_new)


def get_vencodes_fantom(args=None):
    kwargs_new = parse_unknown_args(args, 1)
    get_v_f.main(args[0], **kwargs_new)


def parse_unknown_args(args, n_args):
    list_to_parse = args[n_args:]
    iterator = iter(list_to_parse)
    dict_parsed = {item.replace("--", ""): next(iterator) for item in iterator}
    return dict_parsed


def main(process, unknown_arguments, possibilities):
    """
    Checks the parameters input by the user and passes them along the pipeline to the correct function.

    Parameters
    ----------
    process : str
    unknown_arguments : list
    possibilities : list

    """
    close_matches = get_close_matches(process, possibilities, n=3, cutoff=0.6)
    if process not in close_matches:
        if close_matches:
            print(f"Process {process} does ot exist. Did you mean one of the following:\n", "\n ".join(close_matches))
        else:
            print(f"Process {process} does ot exist.")
        return
    eval(f"{process}(args={unknown_arguments})")


if __name__ == "__main__":
    list_of_processes = ["run_tests", "get_vencodes", "get_vencodes_fantom"]
    parser = argparse.ArgumentParser(description="""Utility script for easy access to most of the VEnCode scripts and
    tests. For the list of arguments to use, refer to this module's documentation or check the help for the script you 
    are trying to use, which is located in the scripts folder.
    Example on how to use in the command-line:
    >python process.py run_tests --verbosity 1
    """)
    parser.add_argument("process", help="The process/script to run.")

    args_, unknown_args = parser.parse_known_args()
    main(args_.process, unknown_args, list_of_processes)
