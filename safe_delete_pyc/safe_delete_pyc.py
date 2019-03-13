#!/usr/bin/env python3

"""
safe_delete_pyc.py
"""

import argparse
import logging
import os
from collections import defaultdict
from pathlib import Path


class UserConfirm(object):

    def __init__(self):
        self.delete_all = False

    def __call__(self, file_path):

        if self.delete_all:
            return True

        prompt = (
            "Are you sure you want to delete '{}'? [yes/no/all]\n"
            "> ".format(file_path))

        line = input(prompt)

        line_clean = line.strip().lower()

        delete_all = line_clean.startswith('a')
        self.delete_all |= delete_all

        delete_current = delete_all or line_clean.startswith('y')

        return delete_current


user_confirm = UserConfirm()


def _parse_args():

    parser = argparse.ArgumentParser(
        usage=(
            "Delete *.pyc files. If there is not a matching .py file "
            "with the same file name stem in the same directory, you "
            "will be prompted before deletion."),
    )

    parser.add_argument(
        'dir',
        nargs='?',
        default=Path(os.getcwd()),
        type=Path,
        help="Directory to recursively search for *.pyc files",
    )

    parser.add_argument(
        '-s',
        '--follow-symlinks',
        action='store_true',
        help="Follow symbolic links",
    )

    parser.add_argument(
        '-o',
        '--no-prompt-on-orphan',
        action='store_true',
        help="Do not prompt before deleting orphaned *.pyc files",
    )

    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help="Print files deleted and orphaned .pyc files",
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Print file paths instead of deleting them",
    )

    args = parser.parse_args()

    return (
        args.dir,
        args.follow_symlinks,
        args.no_prompt_on_orphan,
        args.verbose,
        args.dry_run,
    )


def _walk_path(
        root_path,
        seen_dir_path_set,
        follow_symlinks,
        verbose,
        dry_run,
):
    file_path_tree = defaultdict(
        lambda: {'.py': [], '.pyc': []},
    )

    for path in root_path.iterdir():

        if path.is_dir():

            if path.name == '__pycache__':
                logging.warning("'{}' ignored".format(path))
                continue

            abs_path = path.resolve()

            if path.is_symlink():
                if (
                        not follow_symlinks or
                        abs_path in seen_dir_path_set):

                    continue

            if follow_symlinks:
                seen_dir_path_set.add(abs_path)

            _walk_path(
                abs_path,
                seen_dir_path_set,
                follow_symlinks,
                verbose,
                dry_run,
            )

        suffix_lower = path.suffix.lower()
        if suffix_lower in ('.py', '.pyc'):
            file_path_tree[path.stem][suffix_lower].append(path)

    for file_paths_by_suffix in file_path_tree.values():

        py_file_paths = file_paths_by_suffix['.py']
        pyc_file_paths = file_paths_by_suffix['.pyc']

        is_orphan = len(py_file_paths) == 0

        for pyc_file_path in pyc_file_paths:

            if not dry_run:

                if is_orphan and not user_confirm(pyc_file_path):
                    continue

                try:
                    pyc_file_path.unlink()
                except PermissionError:
                    logging.warning(
                        "Permission error: '{}'".format(pyc_file_path),
                        exc_info=True,
                    )

            if verbose or dry_run:
                print(pyc_file_path)


def safe_delete_pyc(
        dir_path,
        follow_symlinks=False,
        verbose=False,
        dry_run=False,
):
    abs_dir_path = dir_path.resolve(strict=True)

    if not abs_dir_path.is_dir():
        raise NotADirectoryError

    seen_dir_path_set = set() if follow_symlinks else None

    _walk_path(
        abs_dir_path,
        seen_dir_path_set,
        follow_symlinks,
        verbose,
        dry_run,
    )


def main():

    (dir_path,
     follow_symlinks,
     no_prompt_on_orphan,
     verbose,
     dry_run) = _parse_args()

    user_confirm.delete_all = no_prompt_on_orphan

    safe_delete_pyc(
        dir_path,
        follow_symlinks=follow_symlinks,
        verbose=verbose,
        dry_run=dry_run,
    )


if __name__ == '__main__':
    main()
