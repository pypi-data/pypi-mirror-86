#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" get_vencodes_fantom.py: Script used to generate VEnCodes from the FANTOM5 data. """

import sys
import argparse
from pathlib import Path
import ast

file_dir = str(Path(__file__).resolve().parents[2])
sys.path.append(file_dir)

from VEnCode import internals_extensions as iext
from VEnCode.utils import validation_utils as val


def main(cell_type, number_vencodes=1, algorithm="heuristic", number_of_re=4, thresholds=None,
         sample_type="primary cells", data_type="promoters", parsed=False, n_samples=10000,
         stop=5, files_path="outside", out="VEnCodesFantom"):
    """
    Gets VEnCodes from the FANTOM5 CAGE-seq data.

    Parameters
    ----------
    cell_type : str
    number_vencodes : int, str
    algorithm : str
    number_of_re : int, str
    thresholds : str, tuple, None
    sample_type : str
    data_type : str
    parsed : bool, str
    n_samples : int, str
    stop : int, str
    files_path : str, None
    out : str
    """
    def export(data_, path):
        """
        Export the E values and VEnCode data to a file.
        """
        data_.export("vencodes", "e-values", path=path)

    # Handle wrong data types, usually from process.py
    number_vencodes, number_of_re, n_samples, stop = (int(i) for i in [number_vencodes, number_of_re, n_samples, stop])

    if parsed == "False":
        parsed = False
    if files_path == "None":
        files_path = None

    if isinstance(thresholds, (list, tuple)) or thresholds is None:
        pass
    elif thresholds == "None":
        thresholds = None
    else:
        thresholds = ast.literal_eval(thresholds)

    # Apply some tried and tested thresholds if the user didn't specify any
    if thresholds is None:
        non_target_celltypes_inactivity = 0
        if data_type == "enhancers":
            target_celltype_activity = 0.1
        elif data_type == "promoters":
            target_celltype_activity = 0.5
        else:
            raise AttributeError("data_type - {} - not supported".format(data_type))

        if algorithm == "heuristic":
            reg_element_sparseness = 0
        elif algorithm == "sampling":
            reg_element_sparseness = 90  # For some, you probably have to reduce sparseness to 0.
        else:
            raise AttributeError("Algorithm - {} - currently not supported".format(algorithm))
        thresholds = (target_celltype_activity, non_target_celltypes_inactivity, reg_element_sparseness)

    if parsed is None:
        parsed = val.status_parsed(cell_type)

    data_obj = iext.GetVencodesFantom(cell_type=cell_type,
                                      data_type=data_type, algorithm=algorithm,
                                      n_regulatory_elements=number_of_re,
                                      number_vencodes=number_vencodes,
                                      parsed=parsed,
                                      thresholds=thresholds, n_samples=n_samples, stop=stop,
                                      sample_type=sample_type, files_path=files_path)

    export(data_obj, out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Searches for VEnCodes in the FANTOM5 data.
        Exports the VEnCodes and their E values to files, which path you can set with -out.
        Example on how to use in command-line:
        >python get_vencodes_fantom.py Hepatocyte --algorithm heuristic --number_vencodes 2
        """)
    parser.add_argument("cell_type", help="Celltype to search for VEnCodes.")

    parser.add_argument("--number_vencodes", "-n", type=int, help="Number of VEnCodes to retrieve.", default=1)
    parser.add_argument("--algorithm", "-a", type=str, help="Algorithm to use in the search.", default="heuristic")
    parser.add_argument("--number_of_re", "-k", type=int, help="Number of REs (k) that comprise a VEnCode.", default=4)
    parser.add_argument('--thresholds', '-t', type=str,
                        help="Thresholds to apply to the data. Supply a list or tuple of 3 values: first the target "
                             "cell type activity threshold, then the non-target cell types inactivity threshold. "
                             "Finally the sparseness threshold, that filters the data retaining only the sparsest REs.",
                        default=None)
    parser.add_argument("--sample_type", "-s", type=str, help="The type of celltypes to search VEnCodes against."
                                                              "'primary cells' or 'cell lines'.",
                        default="primary cells")
    parser.add_argument("--data_type", "-d", type=str, help="The type of regulatory element data for the VEnCode "
                                                            "search. 'promoters' or 'enhancers'.", default="promoters")
    parser.add_argument("--out", "-o", type=str, help="Path or partial path to a folder to store the result files."
                                                      "Creates a new folder if non-existent.", default="VEnCodesFantom")
    parser.add_argument("--parsed", "-p", type=str, help="Set True to use pre-parsed data, which can be generated by "
                                                         "using the script 'generate_datasets.py'.", default=False)
    parser.add_argument("--n_samples", "-c", type=int, help="Optional for sampling method. Number of samples to take "
                                                            "before giving up finding a VEnCode.", default=10000)
    parser.add_argument("--stop", "-w", type=int, help="Optional for heuristic method. Depth of nodes to go before "
                                                            "giving up finding a VEnCode.", default=5)
    parser.add_argument("--files_path", "-f", type=str, help="Folder where the FANTOM5 files are located."
                                                             "One shortcut is to use 'outside' if you place the data in"
                                                             " a folder called Files just outside the VEnCode module.",
                        default="outside")

    args = parser.parse_args()
    main(args.cell_type, number_vencodes=args.number_vencodes, algorithm=args.algorithm, number_of_re=args.number_of_re,
         thresholds=args.thresholds, sample_type=args.sample_type, data_type=args.data_type, parsed=args.parsed,
         n_samples=args.n_samples, stop=args.stop, files_path=args.files_path, out=args.out)
