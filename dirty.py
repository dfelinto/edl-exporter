#!/usr/bin/python3
"""
Use dirty [--run] folder
"""
import sys
import os
import fnmatch

def get_arguments(arguments):
    len_arguments = len(arguments)

    if "--help" in arguments or "-h" in arguments:
        print ("dirty.py [--run] /full/path/to/images/base/folder")
        sys.exit(0)

    if (len_arguments not in (1,2)) or \
        (len_arguments == 2 and arguments[0] != '--run'):
        print("Invalid number of arguments, "
              "expect `dirty.py [--run] /full/path/to/images/base/folder`")
        print("Got: {0}".format(arguments))
        sys.exit(-1)

    use_dry_run = len_arguments == 1
    base_folder = arguments[-1]

    if not os.path.isdir(base_folder):
        print("Path is not a directory: \"{0}\"".format(base_folder))
        sys.exit(-2)

    return use_dry_run, base_folder


def process_folder(root, files, dry_run):
    includes = {
        '*.jpg',
        }

    for pat in includes:
        len_files = 0

        for f in fnmatch.filter(files, pat):
            # See if number mismatch.
            len_files = max(len_files, len(f))

        for f in fnmatch.filter(files, pat):
            if len_files != len(f):
                filepath = os.path.join(root, f)
                print("Deleting: {filepath}".format(filepath=filepath))

                if not dry_run:
                    try:
                        os.remove(filepath)
                    except Exception as E:
                        print(E)


def all_folders_walk(base_folder, dry_run):
    excludes = {
        '.git',
        '.svn',
        }

    for root, dirs, files in os.walk(base_folder, topdown=True):
        # Excludes can be done with fnmatch.filter and complementary set,
        # But it's more annoying to read.
        dirs[:] = [d for d in dirs if d not in excludes]
        process_folder(root, files, dry_run)


def main(arguments):
    use_dry_run, base_folder = get_arguments(arguments)
    if use_dry_run:
        print("Dry run, run with --run for deleting the files")
    all_folders_walk(base_folder, use_dry_run)


if __name__ == '__main__':
    main(sys.argv[1:])
