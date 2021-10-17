"""
Files manager
"""
import datetime
import time
import argparse
import sys
import os

from typing import Tuple, List, Dict, Any


def file_info_generator(file_paths: List[str], dirpath: str = "") -> Tuple[int, float, str]:
    """
    iterates over a list of file names and yields a  3-tuple containing the file size, its creation date
    """
    for fn in file_paths:
        # get full path of file
        file_path: str = os.path.join(dirpath, fn)
        # get size in bytes
        file_size: int = os.path.getsize(file_path)
        file_creation_date: float = os.path.getmtime(file_path)
        yield file_size, file_creation_date, fn


def filter_size_to_logic(size: int, filter: Tuple[str, str, str]) -> bool:
    filter_size: int = int(filter[1])
    if filter[0] == "lt":
        if filter[2] == 'G':
            return (size < filter_size * 1e9)
        elif filter[2] == 'M':
            return (size < filter_size * 1e6)
        elif filter[2] == 'K':
            return (size < filter_size * 1e3)
    elif filter[0] == "gt":
        if filter[2] == 'G':
            return (size > filter_size * 1e9)
        elif filter[2] == 'M':
            return (size > filter_size * 1e6)
        elif filter[2] == 'K':
            return (size > filter_size * 1e3)
    else:
        raise ValueError


def filter_timestamp_to_logic(timestamp: float, filter: Tuple[str, str]) -> bool:
    filter_timestamp: float = check_transform_timestamp(filter[1])
    if filter[0] == "lt":
        return (timestamp < filter_timestamp)
    elif filter[0] == "gt":
        return (timestamp > filter_timestamp)
    else:
        raise ValueError


def make_tree(root: str, filter: List[str], recursion: bool = True) -> Dict[str, List[Tuple[int, float, str]]]:
    """
    Makes a dict(keys : values)
    keys: the directory full path
    values: each file of the directory
    If a filter is provided, we keep only data that is relevant to the filter's rule
    If recursion is false we only add files from the root directory
    """
    tree: Dict[str, List[Tuple[int, float, str]]] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        # If a filter is provided
        if filter:
            # check if it's a file size comparator filter
            if is_size_filter(filter):
                tree[dirpath] = [(size, timestamp, fn) for size, timestamp, fn in file_info_generator(
                    filenames, dirpath=dirpath) if filter_size_to_logic(size, filter)]
            # or a timestamp comparator filter
            elif is_timestamp_filter(filter):
                tree[dirpath] = [(size, timestamp, fn) for size, timestamp, fn in file_info_generator(
                    filenames, dirpath=dirpath) if filter_timestamp_to_logic(timestamp, filter)]
        else:
            tree[dirpath] = [*file_info_generator(filenames, dirpath=dirpath)]
        if not recursion:
            return tree
    return tree


def get_tree_values_number(tree: Dict[Any, Any]) -> int:
    return sum(len(v) for v in tree.itervalues())


def make_list_from_tree(tree: Dict[str, List[Tuple[Any, Any, str]]]) -> List[Tuple[Any, Any, str]]:
    """
    Converts from dict encoding tree to list encoding tree.
    The loop concatenates each key (dir. path) to their corresponding values (get file_name from file_info) and merge the resulting list.
    """
    files_list: List[Tuple[Any, Any, str]] = []
    for keys, values in tree.items():
        # skip empty folders
        if values:
            files_list += [(size, date, os.path.join(keys, fn))
                           for size, date, fn in values]
    return files_list


def format_file_info(file_info: Tuple[int, float, str]) -> Tuple[str, str, str]:
    """
    pretty formatting for file_info
    currently:
    - File size: puts commas for big numbers 1000000 -> 1,000,000
    - File save date: UNIX time to prettier "dd-mm-YYYY HH:MM:SS"
    - File path: full
    """
    return ("{:,d}".format(file_info[0]),
            datetime.datetime.utcfromtimestamp(
                file_info[1]).strftime('%d-%m-%Y %H:%M:%S'),
            file_info[2])


def print_tree(tree: Dict[str, List[Tuple[int, float, str]]]) -> None:
    """
    Simply iterates over the keys (folder_path) and prints the values (file_info) line by line.
    The keys are printed before each file_info chunk and we add a tab before each entry of the latter.
    """
    header: str = "%s %8s %10s %8s" % ("SIZE (byte)", "DATE", "TIME", "NAME")
    pretty_formatter: str = '%-15s %s %s'
    for key, values in tree.items():
        # skip empty folders
        if not values:
            continue
        print("Path: ", key)
        print("\t", header)
        for file_info in values:
            print("\t", pretty_formatter % (format_file_info(file_info)))
        print()


def print_tree_with_sorting_args(tree: Dict[str, List[Tuple[int, float, str]]], sorting_rule: str = None) -> None:
    """
    rules: 
    - size: file size in bytes
    - date: date in unix time
    Each rule has its own reversed rule version.

    The lambdas specify w.r.t. which file_info entry we should sort.
    """
    if not sorting_rule:
        print_tree(tree)
    else:
        header: str = "%s %8s %10s %8s" % (
            "SIZE (byte)", "DATE", "TIME", "PATH")
        pretty_formatter: str = '%-15s %s %s'
        print(header)
        if sorting_rule == "size":
            for file_info in sorted(make_list_from_tree(tree), key=lambda x: x[0]):
                print(pretty_formatter % (format_file_info(file_info)))
        elif sorting_rule == "rSize":
            for file_info in sorted(make_list_from_tree(tree), key=lambda x: x[0], reverse=True):
                print(pretty_formatter % (format_file_info(file_info)))
        elif sorting_rule == "date":
            for file_info in sorted(make_list_from_tree(tree), key=lambda x: x[1]):
                print(pretty_formatter % (format_file_info(file_info)))
        elif sorting_rule == "rDate":
            for file_info in sorted(make_list_from_tree(tree), key=lambda x: x[1], reverse=True):
                print(pretty_formatter % (format_file_info(file_info)))


def check_transform_timestamp(timestamp: str) -> float:
    """
    Checks and transforms timestamp to unix time format.
    valid formats:
    - "DD_MM_YYYY"
    - "DD_MM_YYYY:hh_mm_ss"\n
    If valid, transforms to unix.
    """
    unix_timestamp: float = None
    try:
        try:
            date, time_ = timestamp.split(':')
            DD, MM, YYYY = tuple(int(x) for x in date.split("_"))
            hh, mm, ss = tuple(int(x) for x in time_.split("_"))
            date_time = datetime.datetime(YYYY, MM, DD, hh, mm, ss)
            unix_timestamp = time.mktime(date_time.timetuple())
        except:
            DD, MM, YYYY = tuple(int(x) for x in timestamp.split("_"))
            date_time = datetime.datetime(YYYY, MM, DD)
            unix_timestamp = time.mktime(date_time.timetuple())
    except:
        raise ValueError("Incorrect timestamp format, must be DD_MM_YYYY or DD_MM_YYYY:hh_mm_ss.\nWas: %s" % (
            timestamp))
    # adjust to local time
    return unix_timestamp + (time.mktime(datetime.datetime.now().timetuple()) - time.mktime(datetime.datetime.utcnow().timetuple()))


def is_size_filter(filter: List[str]) -> bool:
    """
    Checks if the input filter is a file size filter.
    lt, gt = less, greater than.
    """
    if len(filter) == 3 \
            and (filter[0] == "lt" or filter[0] == "gt") \
            and (filter[1].isdigit()) \
            and (filter[2] == 'G' or filter[2] == 'M' or filter[2] == 'K'):
        return True
    return False


def is_timestamp_filter(filter: List[str]) -> bool:
    """
    Checks if the input filter is a timestamp filter.
    lt, gt = less, greater than.
    """
    if len(filter) == 2 \
            and (filter[0] == "lt" or filter[0] == "gt") \
            and check_transform_timestamp(filter[1]):
        return True
    return False


def filter_check_return(filter: List[str]) -> List[str]:
    """
    Checks and returns the same filter if success.
    """
    assert is_size_filter(filter) or is_timestamp_filter(filter), \
        """Assertion failed, --filter option must be one of the following:
            <lt | gt> <integer> <G | M | T>
            <lt | gt> <DD_MM_YYYY | DD_MM_YYYY:HH_MM_SS>"""
    return filter


def remove_files(tree: Dict[str, List[Tuple[Any, Any, str]]]) -> None:
    for dirpath, values in tree.items():
        for file_info in values:
            os.remove(os.path.join(dirpath, file_info[2]))


def main():
    # Don't take script name
    args = sys.argv[1:]
    # Parser instance
    parser = argparse.ArgumentParser("Purge files from a root directory.")

    parser.add_argument(
        "--root", nargs="?", help="Root directory from which we enable purge. This option is required.", required=True)
    parser.add_argument("--recursion", "-r",
                        action="store_true", help="Recursion option.")
    parser.add_argument("--filter", "-f", nargs="+", help="""
        Catches files with specified attributes (size or date).
        """)

    parser.add_argument("--remove", action="store_true",
                        help="Will remove all the files based on the tree that has been constructed.")

    parser.add_argument("--verbose", "-V", action="store_true",
                        help="Shows which files have been selected from the chosen root dir.")
    parser.add_argument("--sort", choices=["size", "rSize", "date", "rDate"],
                        help="""
        Shows which files have been selected from the chosen root dir.
        Choices are sorting options. "r" prefix stands for reverse.

        "size": sort by increasing file size
        "rSize": sort by decreasing file size
        "date": sort by increasing date
        "rDate": sort by decreasing date
        """)
    # Move the files in tree to dest
    # TODO: --move <dest>
    # Prune all the empty directories
    # TODO: --prune
    # make better filters
    # TODO:
    # --filter <timestamp> < timestamp < <timestamp>
    # --filter timestamp < <timestamp>
    # --filter timestamp > <timestamp>
    # --filter <size> < size < <size>
    # --filter size < <size>
    # --filter size > <size>

    # TODO: make action options ask if sure. Add -y option

    args = parser.parse_args(args)
    # Constructs a tree based on the arguments: make_tree(where, parsing filter, recursion?)
    tree = make_tree(
        args.root,
        filter_check_return(args.filter) if args.filter else None,
        args.recursion)
    # Prints it to console if verbose is True with the specified sorting rules
    if args.verbose:
        print_tree_with_sorting_args(tree, args.sort)

    if args.remove:
        remove_files(tree)


if __name__ == "__main__":
    main()
