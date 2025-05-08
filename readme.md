# .backupinfo

This tool lets you easily backup folders marked with a simple `.backupinfo` file.

--- 
## Proposal Backup Scheme

#### Selecting folders to be backed up:

1. Put the file named `.backupinfo` into the folders you want backed up.
2. Run the `mark` command to scan directories with `.backupinfo` and save paths to these directories. (example of scanning your home directory: `python3 backup.py mark ~`)
3. Verify your selected directories with the `list` command.

#### Backing up

1. Prepare your backup drive.
    - *I recommend having the disk split into 2 partitions, archive and backup. Each time you wanna make a backup, format the backup partition.*
2. Verify folders that you want to backup with the `list` command.
3. Use `backup` command to back up your selected folders *(Windows example of backing up a simple B drive (Windows): `python3 backup.py B:/`)*

# Usage

```
python3 backup.py COMMAND...
```

### Commands:

```
mark - scans the current directory to find and save paths of directories with .backupinfo files
mark FOLDER_PATH - scans this FOLDER_PATH to find and save paths of directories with .backupinfo files
mark FOLDER_PATH MAX_DEPTH - scans this FOLDER_PATH to find and save paths of directories with .backupinfo files, with a max depth scan equal to MAX_DEPTH.

list - lists saved paths with .backupinfo files

logs - prints logs

clear - clears the list and logs
clear list - clears the list
clear logs - clears logs

backup OUTPUT_PATH - backup directories from the list with paths to them into the OUTPUT_PATH
```

# Plans for the future

- Make use of content that is in `.backupinfo` files.