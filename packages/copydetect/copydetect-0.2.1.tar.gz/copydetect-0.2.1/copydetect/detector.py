"""This module contains functions for detecting overlap between
a set of test files (files to check for plagairism) and a set of
reference files (files that might have been plagairised from).
"""

import json
from pathlib import Path
import time
import numpy as np
import hashlib
import os
import pickle
import sys
import logging
from .utils import (filter_code, highlight_overlap, get_copied_slices,
                    get_document_fingerprints, find_fingerprint_overlap)
import matplotlib.pyplot as plt
import webbrowser
import pkg_resources
from jinja2 import Template
from tqdm import tqdm
import shutil

class CodeFingerprint:
    """Class for tokenizing, filtering, fingerprinting, and winnowing
    a file. Maintains information about fingerprint indexes and token
    indexes to assist code highlighting for the output report.

    Parameters
    ----------
    file : str
        Path to the file fingerprints should be extracted from.
    k : int
        Length of k-grams to extract as fingerprints.
    win_size : int
        Window size to use for winnowing (must be >= 1).
    boilerplate : array_like, optional
        List of fingerprints to use as boilerplate. Any fingerprints
        present in this list will be discarded from the hash list.
    filter : bool
        If set to to False, code will not be tokenized & filtered.
        Default: True

    Attributes
    ----------
    filename : str
        Name of the originally provided file.
    raw_code : str
        Unfiltered code.
    filtered_code : str
        Code after tokenization and filtering. If filter=False, this is
        the same as raw_code.
    offsets : Nx2 array of ints
        The cumulative number of characters removed during filtering at
        each index of the filtered code. Used for translating locations
        in the filtered code to locations in the unfiltered code.
    hashes : 1D array of ints
        List of fingerprints extracted from the filtered code.
    hash_idx : 1D array of ints
        List of indexes of the selected fingerprints. Used for
        translating hash indexes to indexes in the filtered code.
    k : int
        Value of provided k argument.
    language : str
        If set, will force the tokenizer to use the provided language
        rather than guessing from the file extension.
    """
    def __init__(self, file, k, win_size, boilerplate=[], filter=True,
                 language=None):
        with open(file) as code_fp:
            code = code_fp.read()
        if filter:
            filtered_code, offsets = filter_code(code, file, language)
        else:
            filtered_code, offsets = code, np.array([])
        hashes, idx = get_document_fingerprints(filtered_code, k, win_size,
                                                boilerplate)

        self.filename = file
        self.raw_code = code
        self.filtered_code = filtered_code
        self.offsets = offsets
        self.hashes = hashes
        self.hash_idx = idx
        self.k = k

def compare_files(file1_data, file2_data):
    """Computes the overlap between two CodeFingerprint objects
    using the generic methods from copy_detect.py. Returns the
    number of overlapping tokens and two tuples containing the
    overlap percentage and copied slices for each unfiltered file.

    Parameters
    ----------
    file1_data : CodeFingerprint
        CodeFingerprint object of file #1.
    file2_data : CodeFingerprint
        CodeFingerprint object of file #2.

    Returns
    -------
    token_overlap : int
        Number of overlapping tokens between the two files.
    similarities : tuple of 2 ints
        For both files: number of overlapping tokens divided by the
        total number of tokens in that file.
    slices : tuple of 2 2xN int arrays
        For both files: locations of copied code in the unfiltered
        text. Dimension 0 contains slice starts, dimension 1 contains
        slice ends.
    """
    if file1_data.k != file2_data.k:
        raise ValueError("Code fingerprints must use the same noise threshold")
    idx1, idx2 = find_fingerprint_overlap(
        file1_data.hashes, file2_data.hashes,
        file1_data.hash_idx, file2_data.hash_idx)
    slices1 = get_copied_slices(idx1, file1_data.k)
    slices2 = get_copied_slices(idx2, file2_data.k)
    if len(slices1[0]) == 0:
        return 0, (0,0), (np.array([]), np.array([]))

    token_overlap1 = np.sum(slices1[1] - slices1[0])
    token_overlap2 = np.sum(slices2[1] - slices2[0])

    if len(file1_data.filtered_code) > 0:
        similarity1 = token_overlap1 / len(file1_data.filtered_code)
    else:
        similarity1 = 0
    if len(file2_data.filtered_code) > 0:
        similarity2 = token_overlap2 / len(file2_data.filtered_code)
    else:
        similarity2 = 0

    if len(file1_data.offsets) > 0:
        slices1 += file1_data.offsets[:,1][np.clip(
            np.searchsorted(file1_data.offsets[:,0], slices1),
            0, file1_data.offsets.shape[0] - 1)]
    if len(file2_data.offsets) > 0:
        slices2 += file2_data.offsets[:,1][np.clip(
            np.searchsorted(file2_data.offsets[:,0], slices2),
            0, file2_data.offsets.shape[0] - 1)]

    return token_overlap1, (similarity1,similarity2), (slices1,slices2)

class CopyDetector:
    """Main plagairism detection class. Searches provided directories
    and uses detection parameters to calculate similarity between all
    files found in the directories

    Parameters
    ----------
    config : dict
        Dictionary containing configuration parameters. Note that this
        uses the verbose version of each of the parameters listed
        below. If provided, parameters set in the configuration
        dictionary will overwrite default parameters and other
        parameters passed to the initialization function.
    test_dirs : list
        (test_directories) A list of directories to recursively search
        for files to check for plagiarism.
    ref_dirs: list
        (reference_directories) A list of directories to search for
        files to compare the test files to. This should generally be a
        superset of test_directories
    boilerplate_dirs : list
        (boilerplate_directories) A list of directories containing
        boilerplate code. Matches between fingerprints present in the
        boilerplate code will not be considered plagiarism.
    extensions : list
        A list of file extensions containing code the detector should
        look at.
    noise_t : int
        (noise_threshold) The smallest sequence of matching characters
        between two files which should be considered plagiarism. Note
        that tokenization and filtering replaces variable names with V,
        function names with F, object names with O, and strings with S
        so the threshold should be lower than you would expect from the
        original code.
    guarantee_t : int
        (guarantee_threshold) The smallest sequence of matching
        characters between two files for which the system is guaranteed
        to detect a match. This must be greater than or equal to the
        noise threshold. If computation time is not an issue, you can
        set guarantee_threshold = noise_threshold.
    display_t : float
        (display_threshold) The similarity percentage cutoff for
        displaying similar files on the detector report.
    same_name_only : bool
        If true, the detector will only compare files that have the
        same name
    ignore_leaf : bool
        If true, the detector will not compare files located in the
        same leaf directory.
    autoopen : bool
        If true, the detector will automatically open a webbrowser to
        display the results of generate_html_report
    disable_filtering : bool
        If true, the detector will not tokenize and filter code before
        generating file fingerprints.
    force_language : str
        If set, forces the tokenizer to use a particular programming
        language regardless of the file extension.
    truncate : bool
        If true, highlighted code will be truncated to remove non-
        highlighted regions from the displayed output
    silent : bool
        If true, all logging output will be supressed.
    """
    def __init__(self, config=None, test_dirs=[], ref_dirs=[],
                 boilerplate_dirs=[], extensions=["*"],
                 noise_t=25, guarantee_t=30, display_t=0.33,
                 same_name_only=False, ignore_leaf=False, autoopen=True,
                 disable_filtering=False, force_language=None,
                 truncate=False, silent=False):
        self.silent = silent
        self.test_dirs = test_dirs
        if len(ref_dirs) == 0:
            self.ref_dirs = test_dirs
        else:
            self.ref_dirs = ref_dirs
        self.boilerplate_dirs = boilerplate_dirs
        self.extensions = extensions
        self.noise_t = noise_t
        self.guarantee_t = guarantee_t
        self.display_t = display_t
        self.same_name_only = same_name_only
        self.ignore_leaf = ignore_leaf
        self.autoopen = autoopen
        self.disable_filtering = disable_filtering
        self.force_language = force_language
        self.truncate = truncate

        if config is not None:
            self._load_config(config)

        self._check_arguments()

        self.window_size = self.guarantee_t - self.noise_t + 1

        self.test_files = self._get_file_list(self.test_dirs, self.extensions)
        self.ref_files = self._get_file_list(self.ref_dirs, self.extensions)
        self.boilerplate_files = self._get_file_list(self.boilerplate_dirs,
                                                     self.extensions)

    def _load_config(self, config):
        """Sets member variables according to a configuration
        dictionary.
        """
        self.noise_t = config["noise_threshold"]
        self.guarantee_t = config["guarantee_threshold"]
        self.display_t = config["display_threshold"]
        self.test_dirs = config["test_directories"]
        if "reference_directories" in config:
            self.ref_dirs = config["reference_directories"]
        if "extensions" in config:
            self.extensions = config["extensions"]
        if "boilerplate_directories" in config:
            self.boilerplate_dirs = config["boilerplate_directories"]
        if "force_language" in config:
            self.force_language = config["force_language"]
        if "same_name_only" in config:
            self.same_name_only = config["same_name_only"]
        if "ignore_leaf" in config:
            self.ignore_leaf = config["ignore_leaf"]
        if "disable_filtering" in config:
            self.disable_filtering = config["disable_filtering"]
        if "disable_autoopen" in config:
            self.autoopen = not config["disable_autoopen"]
        if "truncate" in config:
            self.truncate = config["truncate"]

    def _check_arguments(self):
        """type/value checking helper function for __init__"""
        if not isinstance(self.test_dirs, list):
            raise TypeError("Test directories must be a list")
        if not isinstance(self.ref_dirs, list):
            raise TypeError("Reference directories must be a list")
        if not isinstance(self.extensions, list):
            raise TypeError("extensions must be a list")
        if not isinstance(self.boilerplate_dirs, list):
            raise TypeError("Boilerplate directories must be a list")
        if not isinstance(self.same_name_only, bool):
            raise TypeError("same_name_only must be true or false")
        if not isinstance(self.ignore_leaf, bool):
            raise TypeError("ignore_leaf must be true or false")
        if not isinstance(self.disable_filtering, bool):
            raise TypeError("disable_filtering must be true or false")
        if not isinstance(self.autoopen, bool):
            raise TypeError("disable_autoopen must be true or false")
        if self.force_language is not None:
            if not isinstance(self.force_language, str):
                raise TypeError("force_language must be a string")
        if not isinstance(self.truncate, bool):
            raise TypeError("truncate must be true or false")
        if not isinstance(self.noise_t, int):
            if int(self.noise_t) == self.noise_t:
                self.noise_t = int(self.noise_t)
                self.window_size = int(self.window_size)
            else:
                raise TypeError("Noise threshold must be an integer")
        if not isinstance(self.guarantee_t, int):
            if int(self.guarantee_t) == self.guarantee_t:
                self.guarantee_t = int(self.guarantee_t)
                self.window_size = int(self.window_size)
            else:
                raise TypeError("Guarantee threshold must be an integer")

        # value checking
        if self.guarantee_t < self.noise_t:
            raise ValueError("Guarantee threshold must be greater than or "
                             "equal to noise threshold")
        if self.display_t > 1 or self.display_t < 0:
            raise ValueError("Display threshold must be between 0 and 1")

    def _get_file_list(self, dirs, exts, unique=True):
        """Recursively collects list of files from provided
        directories. Used to search test_dirs, ref_dirs, and
        boilerplate_dirs
        """
        file_list = []
        for dir in dirs:
            for ext in exts:
                if ext == "*":
                    matched_contents = Path(dir).rglob("*")
                else:
                    matched_contents = Path(dir).rglob("*."+ext.lstrip("."))
                files = [str(f) for f in matched_contents if f.is_file()]

                if len(files) == 0:
                    logging.warning("No files found in " + dir)
                file_list.extend(files)

        return set(file_list)

    def add_file(self, filename, type="testref"):
        """Adds a file to the list of test files, reference files, or
        boilerplate files. The "type" parameter should be one of
        ["testref", "test", "ref", "boilerplate"]. "testref" will add
        the file as both a test and reference file.
        """
        if type == "testref":
            self.test_files.add(filename)
            self.ref_files.add(filename)
        elif type == "test":
            self.test_files.add(filename)
        elif type == "ref":
            self.ref_files.add(filename)
        elif type == "boilerplate":
            self.boilerplate_files.add(filename)

    def _get_boilerplate_hashes(self):
        """Generates a list of hashes of the boilerplate text. Returns
        a set containing all unique k-gram hashes across all files
        found in the boilerplate directories.
        """
        boilerplate_hashes = []
        for file in self.boilerplate_files:
            try:
                with open(file) as boilerplate_fp:
                    boilerplate = boilerplate_fp.read()
            except UnicodeDecodeError:
                logging.warning(f"Skipping {file}: file not ASCII text")
                continue
            fingerprint = CodeFingerprint(file, self.noise_t, 1,
                                          filter=not self.disable_filtering,
                                          language=self.force_language)
            boilerplate_hashes.extend(fingerprint.hashes)

        return np.unique(np.array(boilerplate_hashes))

    def _preprocess_code(self, file_list):
        boilerplate_hashes = self._get_boilerplate_hashes()

        file_data = {}
        for code_f in tqdm(file_list, bar_format= '   {l_bar}{bar}{r_bar}',
                disable=self.silent):
            try:
                file_data[code_f] = CodeFingerprint(
                    code_f, self.noise_t, self.window_size,
                    boilerplate_hashes, not self.disable_filtering,
                    self.force_language)

            except UnicodeDecodeError:
                logging.warning(f"Skipping {code_f}: file not ASCII text")
                continue

        return file_data

    def _comparison_loop(self):
        """The core code used to determine code overlap. The overlap
        between each test file and each compare file is computed and
        stored in similarity_matrix. Token overlap information and the
        locations of copied code are stored in slice_matrix and
        token_overlap_matrix, respectively.
        """
        start_time = time.time()
        if not self.silent:
            print("  0.00: Generating file fingerprints")
        test_f_list = sorted(list(self.test_files))
        self.all_files = (test_f_list
            + sorted([f for f in self.ref_files if f not in self.test_files]))
        self.file_data = self._preprocess_code(self.all_files)

        self.similarity_matrix = np.full((
            len(self.all_files), len(self.all_files)), -1, dtype=np.float64)
        self.token_overlap_matrix = np.full((
            len(self.all_files), len(self.all_files)), -1)
        self.slice_matrix = [[np.array([]) for _ in range(len(self.all_files))]
                             for _ in range(len(self.all_files))]

        if not self.silent:
            print(f"{time.time()-start_time:6.2f}: Beginning code comparison")

        for i, test_f in enumerate(tqdm(test_f_list,
                bar_format= '   {l_bar}{bar}{r_bar}', disable=self.silent)):
            for j, ref_f in enumerate(self.all_files):
                if test_f not in self.file_data or ref_f not in self.file_data:
                    continue
                elif test_f == ref_f:
                    continue
                elif self.similarity_matrix[i,j] != -1:
                    continue
                elif (self.all_files[i] not in self.test_files or
                      self.all_files[j] not in self.ref_files):
                    continue

                if self.same_name_only:
                    if os.path.basename(test_f) != os.path.basename(ref_f):
                        continue
                if self.ignore_leaf:
                    if os.path.dirname(test_f) == os.path.dirname(ref_f):
                        continue

                overlap, (sim1,sim2), (slices1,slices2) = compare_files(
                    self.file_data[test_f], self.file_data[ref_f])

                self.similarity_matrix[i,j] = sim1
                self.slice_matrix[i][j] = [slices1, slices2]
                self.similarity_matrix[j,i] = sim2
                self.slice_matrix[j][i] = [slices2,slices1]

                self.token_overlap_matrix[i,j] = overlap
                self.token_overlap_matrix[j,i] = overlap

        if not self.silent:
            print(f"{time.time()-start_time:6.2f}: Code comparison completed")

    def run(self):
        """User-facing code overlap computing function. Checks for a
        session that can be resumed from then calls _comparison_loop to
        generate results.
        """
        if len(self.test_files) == 0 or len(self.ref_files) == 0:
            err_folder = "test"
            if len(self.test_files) > len(self.ref_files):
                err_folder = "reference"

            logging.error("Copy detector failed: No files found in "
                          f"{err_folder} directories")
            self.similarity_matrix = np.array([])
            self.token_overlap_matrix = np.array([])
            self.slice_matrix = np.array([])
            return

        self._comparison_loop()

    def get_copied_code_list(self):
        """Get a list of copied code to display on the output report.
        Returns a list of tuples containing the similarity score, the
        test file name, the compare file name, the highlighted test
        code, and the highlighted compare code,
        """
        if len(self.similarity_matrix) == 0:
            logging.error("Cannot generate code list: no files compared")
            return []
        x,y = np.where(self.similarity_matrix > self.display_t)

        code_list = []
        selected_pairs = set([])
        for idx in range(len(x)):
            test_f = self.all_files[x[idx]]
            ref_f = self.all_files[y[idx]]
            if test_f + ref_f in selected_pairs:
                continue

            selected_pairs.add(test_f + ref_f)
            selected_pairs.add(ref_f + test_f)
            test_sim = self.similarity_matrix[x[idx], y[idx]]
            ref_sim = self.similarity_matrix[y[idx], x[idx]]
            slices_test = self.slice_matrix[x[idx]][y[idx]][0]
            slices_ref = self.slice_matrix[x[idx]][y[idx]][1]

            if self.truncate:
                truncate = 10
            else:
                truncate = -1
            hl_code_1, _ = highlight_overlap(
                self.file_data[test_f].raw_code, slices_test,
                "<span class='highlight-red'>", "</span>",
                truncate=truncate, escape_html=True)
            hl_code_2, _ = highlight_overlap(
                self.file_data[ref_f].raw_code, slices_ref,
                "<span class='highlight-green'>", "</span>",
                truncate=truncate, escape_html=True)
            overlap = self.token_overlap_matrix[x[idx], y[idx]]

            code_list.append([test_sim, ref_sim, test_f, ref_f,
                              hl_code_1, hl_code_2, overlap])

        code_list.sort(key=lambda x: -x[0])
        return code_list

    def generate_html_report(self, dir="report", page_name="report",
                             output_mode="save"):
        """Generates an html report listing all files with similarity
        above the display_threshold, with the copied code segments
        highlighted.
        """
        if len(self.similarity_matrix) == 0:
            logging.error("Cannot generate report: no files compared")
            return

        code_list = self.get_copied_code_list()
        data_dir = pkg_resources.resource_filename('copydetect', 'data/')

        if output_mode == "save":
            # make output directory, figures
            if not os.path.exists(f"{dir}/figures/"):
                os.makedirs(f"{dir}/figures/")

            plot_mtx = np.copy(self.similarity_matrix)
            plot_mtx[plot_mtx == -1] = np.nan
            plt.imshow(plot_mtx)
            plt.colorbar()
            plt.tight_layout()
            plt.savefig(f"{dir}/figures/sim_matrix.png")
            plt.close()

            scores = self.similarity_matrix[self.similarity_matrix != -1]
            plt.hist(scores, bins=20)
            plt.tight_layout()
            plt.savefig(f"{dir}/figures/sim_histogram.png")
            plt.close()

        # render template with jinja and save as html
        with open(data_dir + "report.html") as template_fp:
            template = Template(template_fp.read())

        flagged = self.similarity_matrix > self.display_t
        flagged_file_count = np.sum(np.any(flagged, axis=1))

        output = template.render(test_count=len(self.test_files),
                                 compare_count=len(self.ref_files),
                                 flagged_file_count=flagged_file_count,
                                 code_list=code_list,
                                 style_path="style/style.css")

        if output_mode == "save":
            with open(f"{dir}/{page_name}.html", "w") as report_f:
                report_f.write(output)

            if not os.path.exists(f"{dir}/style/"):
                os.makedirs(f"{dir}/style/")
            shutil.copy(data_dir + "style.css", f"{dir}/style/style.css")

            if not self.silent:
                print(f"Output saved to {dir}/{page_name}.html")
            if self.autoopen:
                webbrowser.open('file://'
                                + os.path.realpath(f"{dir}/{page_name}.html"))
        elif output_mode == "return":
            return output
        else:
            raise ValueError("output_mode not supported")
