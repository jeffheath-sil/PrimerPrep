# Installing and running PrimerPrep (version 3+) from source code on Linux
Fraser Bennett, SIL LEAD Inc., 24-JUL-2020

PrimerPrep is a software tool written by Jeff Heath (SIL International) that helps in preparing a literacy primer. PrimerPrep is distributed as a compiled application for Windows, but it is possible to run it under Linux. This guide describes how to install and run PrimerPrep (version 3+) from uncompiled source code in Linux.

The overall process is:

1. Make sure all the necessary packages are installed
2. Get the PrimerPrep source code from Github
3. Run the application

I'm hoping that you are comfortable issuing commands in a terminal window --- if not, don't worry, I'll start out with detailed instructions.

Since you will need to install software, make sure that you have administrator-level permissions for your computer system before you begin.

(Note: These instructions have been tested under Ubuntu LTS 18.04, Ubuntu LTS 20.04, Wasta LTS 18.04, and Fedora 32. They assume an Ubuntu-based system that uses `apt` for its package manager; if you are using a Linux variety that uses a different package manager, make the appropriate changes to the instructions for installing packages.)

## 0. First, open a Terminal Window

We'll be working with the Linux terminal window and issuing typed commands. So first, open a Terminal window. On most Linux systems, you can do this by pressing the Super key (the one that's labeled with a Windows logo, or the command key on an Apple Macintosh keyboard) typing `Terminal` in the search box, and then pressing the `Enter` key.  You should see a blank window with a line for you to enter commands.

(In case you're new to using the Terminal, the text at the beginning of the line tells you your username, the name of the computer, and which directory of the file system you are currently in. Here's what mine looks like:

```bash
fraser@vm-ubuntu20:~$ █
```
This says that my I'm logged into the account named `fraser` on a computer named `vm-ubuntu20`, and I'm currently working in the home directory for the account (`~` for short). The block `█` is the cursor where I can enter a command.

## 1. Make sure all the necessary packages are installed

A "package" is a collection of software in Linux. To install and run PrimerPrep, you'll need to have a number of software tools on your system -- happily, many of them are pre-installed on most Linux distributions.

### 1.1. Make sure `git` is installed.

[`git`](https://git-scm.com) is the program that will fetch the PrimerPrep source code from [github.com](https://github.com). In the terminal window, type the following at the command prompt in the Terminal window:
```
which git
```
If `git` is installed, you will see a response that looks like:
```
fraser@vm-ubuntu20:~$ which git
/usr/bin/git
fraser@vm-ubuntu20:~$ █
```
But if you see no response, then `git` isn't installed. That would look like this: 
```
fraser@vm-ubuntu20:~$ which git
fraser@vm-ubuntu20:~$ █
```
In that case, install `git` by typing the following:
```
sudo apt install git
```
You'll need to type your administrator password (unless you have recently used `sudo` for something else).
```
fraser@vm-ubuntu20:~$ sudo apt install git
[sudo] password for fraser:
```
If you're asked whether to install the "packages", press `Y`.

### 1.2. Make sure `python3` is installed.

Check to see whether `python3` is installed by typing:
```
which python3
```
You'll probably see a response like:
```
fraser@vm-ubuntu20:~$ which python3 
/usr/bin/python3
fraser@vm-ubuntu20:~$ █
```
If you don't see a response with a path to the `python3` file, then install `python3`:
```
sudo apt install python3
```

### 1.3. Make sure `pip3` is installed.

`pip3` is the package manager for Python 3. As before, we'll check to see whether it's installed:
```
which pip3
```
If it's not installed, install it:
```
sudo apt install python3-pip
```

### 1.4. Install `numpy`

Despite its funny name, `numpy` is a collection of highly useful mathematical functions for Python. Use `pip3` to install `numpy`:
```
pip3 install numpy
```

## 2. Get the PrimerPrep source code

Now that we have our packages installed, we can get the PrimerPrep source files. In this section we decide where we want the PrimerPrep folder (and navigate to it), download the PrimerPrep source files, and finally prepare them for use.

### 2.1 (Optional) Navigate to your preferred PrimerPrep destination folder

Navigate to the folder where you want to put the PrimerPrep folder. If you just want it in your home directory (`~`), you don't have to do anything. But if you want to put PrimerPrep, for example, into a `tools` folder, you could create the folder and navigate to it as follows:
```
mkdir tools
cd tools
```
In my case, I've chosen to do nothing, which will place the PrimerPrep folder in my home directory.

### 2.2 Clone the PrimerPrep files from Github

Now 'clone' (copy) the PrimerPrep files from the Github repository:
```
git clone https://github.com/jeffheath-sil/PrimerPrep.git
```
`git` will download the files and put them in a new folder called `PrimerPrep` in the current directory.

### 2.3 Navigate to the PrimerPrep `source` folder

After `git` has fetched all the files, navigate to the `source` directory in your new local PrimerPrep folder:

```
cd PrimerPrep/source/
```
Now my Terminal command line looks like this:
```
fraser@vm-ubuntu20:~/PrimerPrep/source$ █
```

### 2.4. Unzip the compressed directories in the `source` folder

Next, unpack the two compressed directories, `po.zip` and `Help.zip`:

```
unzip po.zip
unzip Help.zip
```
You can make sure they were unzipped by showing a directory listing of the folder contents using the `ls -1` command:
```
fraser@vm-ubuntu20:~/PrimerPrep/source$ ls -1
Help
Help.zip
po
po.zip
'PrimerPrep 18x18.ico'
PrimerPrep-Folder.spec
PrimerPrep.glade
PrimerPrep.iss
PrimerPrep.py
```
Notice the entries for `Help` and `po`: these are the unzipped folders.

## 3. Run the program from the command line

Now you're ready to use PrimerPrep! Enter the following command in the Terminal window:
```
python3 ./PrimerPrep.py
```
The PrimerPrep application window should appear. The terminal window may display some warnings, but you can safely ignore them.

When you want to quit PrimerPrep, use the `File > Exit` menu option.

When you want to start using it again, open the Terminal, navigate to the PrimerPrep folder, and launch the program again.

```
fraser~vm-ubuntu20:~$ cd PrimerPrep/source
fraser@vm-ubuntu20:~/PrimerPrep/source$ python3 ./PrimerPrep.py
```

Happy PrimerPrepping!

*Questions? Contact Fraser Bennett or Jeff Heath. There is contact information for Jeff at the bottom of the PrimerPrep Help file.*

## 4. (Optional) Delete unneeded files from the PrimerPrep repository

Most of the files that are downloaded from `git` aren't actually needed to run PrimerPrep on Linux. If you like cleaning up, enter the following commands in the Terminal window:
```
cd ~/PrimerPrep
rm -rf .git
rm -rf builds
```
NOTE that the `rm -rf` command is very dangerous, as it removes the folder with the given name and all of its subfolders without asking for any confirmation. So make sure you are deleting the right folders! The `.git` folder contains all the version control history information for the PrimerPrep repository, and the `builds` folder contains the Windows installers, neither of which are needed to run PrimerPrep on Linux. You can also delete the Help.zip and po.zip files once you've extracted those folders.

