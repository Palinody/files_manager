# TODO
- Move the parsed files to dest (with keep structure option?)

`--move <dest>`
- Prune all the empty directories. If `--move` option enabled, move before prune in case the destination folder is empty and within the scope of `--prune` targets. 

`--prune`
- make better filters

`--filter <timestamp> < timestamp < <timestamp>`

`--filter timestamp < <timestamp>`

`--filter timestamp > <timestamp>`

`--filter <size> < size <G|M|K|B> < <size>`

`--filter size <G|M|K|B> < <size>`

`--filter size <G|M|K|B> > <size>`

- make action options trigger confirmation prompt. Add `-y` option.

# Tutorial
- Directory tree example
```bash
<root directory>
├── empty_dir
├── file_0
├── file_1
├── file_2
├── folder_0
│   ├── file_3
│   ├── file_4
│   ├── file_5
│   ├── file_6
│   ├── folder_0
│   │   └── folder_0
│   │       ├── file_7
│   │       ├── file_8
│   │       ├── folder_0
│   │       │   ├── file_10
│   │       │   ├── file_11
│   │       │   └── file_12
│   │       ├── folder_1
│   │       └── folder_2
│   │           └── file_9
│   ├── folder_1
│   │   ├── folder_0
│   │   │   ├── file_14
│   │   │   ├── file_15
│   │   │   ├── file_17
│   │   │   └── file_18
│   │   └── folder_1
│   │       ├── file_19
│   │       └── file_20
│   └── folder_2
│       └── file_13
├── folder_1
│   └── front_center
└── folder2
    └── file_21
```

- Define `root` directory
```bash
$ python3 files_manager.py --root /path/to/root/directory
```
This command will silently construct the parse tree
```bash

```

- To visualise the tree parser, use the cmd `--verbose` or `-V`
```bash
$ python3 files_manager.py --root /path/to/root/directory --verbose
```
The resulting tree will parse only the files 
```bash
Path:  /path/to/root/directory
         SIZE (byte)     DATE       TIME     PATH
         226,948,380     09-03-2021 16:46:13 file_1
         161,836,709     26-02-2021 09:27:38 file_2
         361,543,919     14-10-2021 08:07:51 file_0
```

- To parse the directories recursively use `--recursion` or `-r`
```bash
$ python3 files_manager.py --root /path/to/root/directory -V -r
```
```bash
Path:  /path/to/root/directory
         SIZE (byte)     DATE       TIME     PATH
         226,948,380     09-03-2021 16:46:13 file_1
         161,836,709     26-02-2021 09:27:38 file_2
         361,543,919     14-10-2021 08:07:51 file_0

Path:  /path/to/root/directory/folder2
         SIZE (byte)     DATE       TIME     PATH
         674,644,297     05-10-2021 08:39:22 file_21

Path:  /path/to/root/directory/folder_0
         SIZE (byte)     DATE       TIME     PATH
         176,797,703     10-03-2021 08:51:21 file_6
         146,947,693     21-05-2021 10:18:46 file_5
         175,991,234     10-03-2021 08:49:25 file_3
         173,711,458     10-03-2021 08:48:54 file_4

Path:  /path/to/root/directory/folder_0/folder_1/folder_1
         SIZE (byte)     DATE       TIME     PATH
         129,131,325     21-05-2021 13:51:23 file_20
         146,947,693     21-05-2021 13:44:18 file_19

Path:  /path/to/root/directory/folder_0/folder_1/folder_0
         SIZE (byte)     DATE       TIME     PATH
         1,170,405,832   12-03-2021 14:01:16 file_14
         1,644,261,352   10-05-2021 13:03:26 file_15
         2,155,620,073   12-03-2021 14:03:28 file_17
         1,288,557,762   12-03-2021 12:31:56 file_18

Path:  /path/to/root/directory/folder_0/folder_0/folder_0
         SIZE (byte)     DATE       TIME     PATH
         2,697           21-05-2021 13:44:35 file_7
         58,223,158      21-05-2021 13:44:35 file_8

Path:  /path/to/root/directory/folder_0/folder_0/folder_0/folder_0
         SIZE (byte)     DATE       TIME     PATH
         1,236,016,848   21-05-2021 13:50:20 file_10
         119,965,643     21-05-2021 13:50:50 file_12
         1,056,284,105   21-05-2021 13:55:51 file_11

Path:  /path/to/root/directory/folder_0/folder_0/folder_0/folder_2
         SIZE (byte)     DATE       TIME     PATH
         121,736,117     21-05-2021 13:56:22 file_9

Path:  /path/to/root/directory/folder_0/folder_2
         SIZE (byte)     DATE       TIME     PATH
         119,965,643     21-05-2021 10:46:29 file_13
```

- To sort the visualisation of the tree by date or by file size: `--sort size`, `--sort date`, `--sort rSize`, `--sort rDate`. The 2 first options sort in increasing order and the 2 last in reversed/decreasing order.
```bash
$ python3 files_manager.py --root /path/to/root/directory -V -r --sort date
```
The --sort command has no influence on the tree and only modifies how it is __presented in the console__.
```bash
SIZE (byte)     DATE       TIME     PATH
161,836,709     26-02-2021 09:27:38 /path/to/root/directory/file_2
226,948,380     09-03-2021 16:46:13 /path/to/root/directory/file_1
173,711,458     10-03-2021 08:48:54 /path/to/root/directory/folder_0/file_4
175,991,234     10-03-2021 08:49:25 /path/to/root/directory/folder_0/file_3
176,797,703     10-03-2021 08:51:21 /path/to/root/directory/folder_0/file_6
1,288,557,762   12-03-2021 12:31:56 /path/to/root/directory/folder_0/folder_1/folder_0/file_18
1,170,405,832   12-03-2021 14:01:16 /path/to/root/directory/folder_0/folder_1/folder_0/file_14
2,155,620,073   12-03-2021 14:03:28 /path/to/root/directory/folder_0/folder_1/folder_0/file_17
1,644,261,352   10-05-2021 13:03:26 /path/to/root/directory/folder_0/folder_1/folder_0/file_15
146,947,693     21-05-2021 10:18:46 /path/to/root/directory/folder_0/file_5
119,965,643     21-05-2021 10:46:29 /path/to/root/directory/folder_0/folder_2/file_13
146,947,693     21-05-2021 13:44:18 /path/to/root/directory/folder_0/folder_1/folder_1/file_19
58,223,158      21-05-2021 13:44:35 /path/to/root/directory/folder_0/folder_0/folder_0/file_8
2,697           21-05-2021 13:44:35 /path/to/root/directory/folder_0/folder_0/folder_0/file_7
1,236,016,848   21-05-2021 13:50:20 /path/to/root/directory/folder_0/folder_0/folder_0/folder_0/file_10
119,965,643     21-05-2021 13:50:50 /path/to/root/directory/folder_0/folder_0/folder_0/folder_0/file_12
129,131,325     21-05-2021 13:51:23 /path/to/root/directory/folder_0/folder_1/folder_1/file_20
1,056,284,105   21-05-2021 13:55:51 /path/to/root/directory/folder_0/folder_0/folder_0/folder_0/file_11
121,736,117     21-05-2021 13:56:22 /path/to/root/directory/folder_0/folder_0/folder_0/folder_2/file_9
674,644,297     05-10-2021 08:39:22 /path/to/root/directory/folder2/file_21
361,543,919     14-10-2021 08:07:51 /path/to/root/directory/file_0
```

- The tree can be filtered using the `--filter` option by date or by file size with rules. 
There are currently 2 rules:

File size filtering: `<comparator> <integer> <file size unit>`

Timestamp filtering: `<comparator> <timestamp>`

`comparator`: "lt" or "gt" meaning "less than" and "greater than" respectively.

`file size unit`: "G" or "M" or "K" meaning gigabyte, megabyte and kilobyte respectively

`timestamp`: "DD-MM-YYYY" or "DD-MM-YYYY:hh-mm-ss"

Example
```bash
python3 files_manager.py --root /path/to/root/directory -V -r --sort date --filter gt 21-05-2021:13-44-18
```
The above tree becomes:
```bash
SIZE (byte)     DATE       TIME     PATH
146,947,693     21-05-2021 13:44:18 /path/to/root/directory/folder_0/folder_1/folder_1/file_19
58,223,158      21-05-2021 13:44:35 /path/to/root/directory/folder_0/folder_0/folder_0/file_8
2,697           21-05-2021 13:44:35 /path/to/root/directory/folder_0/folder_0/folder_0/file_7
1,236,016,848   21-05-2021 13:50:20 /path/to/root/directory/folder_0/folder_0/folder_0/folder_0/file_10
119,965,643     21-05-2021 13:50:50 /path/to/root/directory/folder_0/folder_0/folder_0/folder_0/file_12
129,131,325     21-05-2021 13:51:23 /path/to/root/directory/folder_0/folder_1/folder_1/file_20
1,056,284,105   21-05-2021 13:55:51 /path/to/root/directory/folder_0/folder_0/folder_0/folder_0/file_11
121,736,117     21-05-2021 13:56:22 /path/to/root/directory/folder_0/folder_0/folder_0/folder_2/file_9
674,644,297     05-10-2021 08:39:22 /path/to/root/directory/folder2/file_21
361,543,919     14-10-2021 08:07:51 /path/to/root/directory/file_0
```

- Finally, to remove all the files that are shown after applying all the filters, use `--remove`
```bash
python3 files_manager.py --root /path/to/root/directory -V -r --sort date --filter gt 21_05_2021:13_44_18 --remove
```
Of course, you can remove the files directly using the rule without outputing in the console. Though, it's safer to visualise the tree first.
```bash
python3 files_manager.py --root /path/to/root/directory -r --filter gt 21_05_2021:13_44_18 --remove
```