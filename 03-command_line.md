# Learn command line

Please follow and complete the free online [Bash Scripting Tutorial](https://ryanstutorials.net/bash-scripting-tutorial/) or [Codecademy's Learn the Command Line](https://www.codecademy.com/learn/learn-the-command-line). These are helpful tutorials. You should be able to go through these in a couple of hours.

**Note:** Bash is not installed on a PC. Rather, PC users must install Cygwin. Once Cygwin has been installed, the command line interface witll _emulate_ bash. You can find all information regarding Cygwin [here](https://www.cygwin.com/).

---

### Q1.  Cheat Sheet of Commands

Here's a list of items with which you should be familiar:
* show current working directory path
* creating a directory
* deleting a directory
* creating a file using `touch` command
* deleting a file
* renaming a file
* listing hidden files
* copying a file from one directory to another

Make a cheat sheet for yourself: a list of at least **ten** commands and what they do.  (Use the 8 items above and add a couple of your own.)

No. | Command | Description
---- | ------- | -------
1. | `ls` | List files in the current dir
2. | `mkdir dirname` | Create new directory
3. | `rm -r dirname` | Recursively remove a directory
4. | `touch filename` | Create an empty file
5. | `rm filename` | Remove a file
6. | `mv filename newname` | Rename a file
7. | `ls -a` | List all files in the current working dir
8. | `cp file_1 path/to/file_2` | Copy file to a new path
9. | `cat filename` | Show content of a file
10. | `diff file_1 file_2` | Show a line by line comparison of two files
11. | `man command` | Show the man page for a command (help page/documentation)
12. | `grep -inr --color=auto search_string dir` | Search recursively (`-r`) for search_string in dir, ignore case (`-i`), show line numbers (`-n`), color the result (search_string only) (`--color=auto`).
13. | `ps auxewww` | Show all (`a+x`) running processes and also display the username columns (`u`), the ENV vars (`e`) and show all the command line args (`www`).
14. | `fc` | Open the last command in an editor and execute after editing.
15. | `wc -l input` | Count lines in input. Most used with piping output to it (e.g., grep for soemthing and then count the occurances).
16. | <code>sort filename.txt &#124; uniq -c &#124; sort -nr &#124; head -n 5</code> | Sort the lines by number of appearances in file and list only the top 5 most common. (`sort -r` sort in reverse).
17. | `comm file1 file2` | Show which lines two files have in common.
18. | `tail -f filename.txt` | Show the last 10 lines and follow (`-f`, also look at `--follow ...`) if new lines are added (Useful for logfiles).
19. | `find in/this/dir --type f -name '*.pyc' -delete` | Find all files of type file (`--type f`) with the name containing '.pyc' (`-name '*.pyc'`) in this dir (`in/this/dir`) and then delete them (`-delete`). Another interesting Action is `-print`.
20. | `pwd` | Show current working directory name and path.

---

### Q2.  List Files in Unix

What do the following commands do:
Original Command | Answer
---- | ----
`ls`  | List files in the current working dir
`ls -a` | List all files in the current working dir
`ls -l` | List files and display in the 'long format'
`ls -lh` | List files and display in the 'long format' and also use unit suffixes (B for Bytes etc.,)
`ls -lah`  | Same as `ls -lh` but for all files
`ls -t` | List files but sort by time formatted
`ls -Glp` | List files and display with coloring and back-slashes for dirs

---

### Q3.  More List Files in Unix

Explore these other [ls options](http://www.techonthenet.com/unix/basic/ls.php) and pick 5 of your favorites:

No. | Command | Description
---- | ------- | -------
1. | `ls -Rlh`  | List files and files of subdirs in the long-format with unit suffixes
2. | `ls -la`  | List all files in the long-format
3. | `ls -t`  | List newest files first
4. | `ls -lG`  | List files in long-format with coloring enabled.
5. | `ls -lA`  | Same as `ls -la` except that it ignores the current (`.`) and parent (`..`) dir.


---

### Q4.  Xargs

What does `xargs` do? Give an example of how to use it.

>> `xargs` takes a whitespace separated list of strings and converts these to command line args.
>> For example: ` find . -name *.py | xargs sed -i s/some_misstipet_var/new_var_name/g` -> find all files with a .py file-extension and replace all occurrences of a variable name with a new one, within these files.
