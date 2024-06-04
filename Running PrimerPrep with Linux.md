# Installing and running PrimerPrep (version 3+) from source code on Linux
Fraser Bennett, SIL LEAD Inc., 24-JUL-2020 (rev. 09-MAY-2024)

PrimerPrep is a software tool written by Jeff Heath (SIL International) that helps in preparing a literacy primer. PrimerPrep is distributed as a compiled application for Windows but it is possible to run it under Linux. This guide describes how to install and run PrimerPrep (version 3+) from uncompiled source code in Linux.

The overall process is:

1. Make sure all the necessary packages are installed
2. Get the PrimerPrep source code from Github
3. Run the application

To do this, you should be comfortable issuing commands in a terminal window. If you haven't used the terminal window before, don't worry, we'll start out with detailed instructions.

You will need to install software. Make sure that you have administrator-level permissions for your computer system before you begin.

> [!NOTE]
> These instructions have been tested under Ubuntu LTS 22.04, Ubuntu LTS 20.04, Wasta LTS 18.04, and Fedora 32. They assume an Ubuntu-based system that uses `apt` for its package manager. If you are using a Linux variety that uses a different package manager, make the appropriate changes to the instructions for installing packages.

## 0. Open a Terminal Window

We will be working with the Linux terminal window and issuing typed commands, so first, open a Terminal window. On most Linux systems, you can do this by pressing the Super key (the one that's labeled with a Windows logo, or the command key on an Apple Macintosh keyboard), typing `Terminal` in the search box, and then pressing the `Enter` key.  You should see a blank window with a line for you to enter commands.

> [!TIP]
> In case you're new to using the Terminal, the text at the beginning of the line tells you your username, the name of the computer, and which directory of the file system you are currently in. Here's what mine looks like:  
> ```
> fraser@vm-ubuntu20:~$ █
> ```
> This says that my I'm logged into the account named `fraser` on a computer named `vm-ubuntu20`, and I'm currently working in the home directory for the account (`~` for short). The block `█` is the cursor where I can enter a command.

## 1. Make sure all the necessary packages are installed

A _package_ is a collection of software in Linux. To install and run PrimerPrep, you need to have a number of software tools on your system. Happily, many of the packages with these tools are pre-installed on most Linux distributions.

### 1.1. Make sure `git` is installed.

[`git`](https://git-scm.com) is the program that will fetch the PrimerPrep source code from [github.com](https://github.com). In the terminal window, type the following at the command prompt in the Terminal window, then press `ENTER`:
```
which git
```
If `git` is installed, you will see a response showing the path to the `git` file --- like this:
```
fraser@vm-ubuntu20:~$ which git
/usr/bin/git
fraser@vm-ubuntu20:~$ █
```
If you see no response, then `git` isn't installed. That would look like this: 
```
fraser@vm-ubuntu20:~$ which git
fraser@vm-ubuntu20:~$ █
```
If `git` is not installed, install `git` by typing the following:
```
sudo apt install git
```
You will need to type your administrator password (unless you have recently used the `sudo` command for something else).
```
fraser@vm-ubuntu20:~$ sudo apt install git
[sudo] password for fraser:
```
If you are asked whether to install the "packages", press `Y`.

### 1.2. Make sure `python3` is installed.

Check to see whether `python3` is installed by typing:
```
which python3
```
You will probably see a response like this:
```
fraser@vm-ubuntu20:~$ which python3 
/usr/bin/python3
fraser@vm-ubuntu20:~$ █
```
If you do not see a response with a path to the `python3` file, then install `python3`:
```
sudo apt install python3
```

### 1.3. Make sure `pip3` is installed.

`pip3` is the package manager for Python3. As before, we'll check to see whether it is installed:
```
which pip3
```
If pip3 is not installed, install it with this command:
```
sudo apt install python3-pip
```

### 1.4. Install `numpy`

`numpy` is a collection of useful mathematical functions for Python. Use `pip3` to install `numpy`:
```
pip3 install numpy
```

## 2. Get the PrimerPrep source code

Now that we have our packages installed, we can get the PrimerPrep source files. In this section we will first decide where we want the PrimerPrep folder (and navigate to it). Then we will download the PrimerPrep source files and get ready to use them.

### 2.1 (Optional) Decide where to store the PrimerPrep files and navigate there

First you need to decide where to store the folder (or directory) of PrimerPrep source files in your computer's file system. I've chosen to put the PrimerPrep folder in my home directory (`~`), which happens to be my Terminal window's current working directory. 

> [!TIP]
> If you want to put PrimerPrep somewhere else, you can do so. For example, if you want to put PrimerPrep in a new folder called `tools`, you can do so by navigating to the folder where you want the new folder to be. Then type: 
> ```
> mkdir tools
> ```
> After you have created the new folder, set it as your current working directory: 
> ```
> cd tools
> ```

### 2.2 Clone the PrimerPrep files from Github

Now 'clone' (copy) the PrimerPrep files from the Github repository:
```
git clone https://github.com/jeffheath-sil/PrimerPrep.git
```
`git` will download the files and put them in a new folder called `PrimerPrep` in the current working directory.

### 2.3 Navigate to the PrimerPrep folder

After `git` has fetched all the files, navigate to your new local PrimerPrep folder:
```
cd PrimerPrep
```
Now my Terminal command line looks like this:
```
fraser@vm-ubuntu20:~/PrimerPrep$ █
```

## 3. Run the program from the command line

Now you're ready to use PrimerPrep! Enter the following command in the Terminal window:
```
python3 ./PrimerPrep.py
```
The PrimerPrep application window should appear. The terminal window may display some warnings, but you can safely ignore them.

When you want to quit PrimerPrep, use the **File > Exit** menu option in the PrimerPrep application window. 

When you want to start using PrimerPrep again, open the Terminal, navigate to the PrimerPrep folder, and launch the program again.

```
fraser@vm-ubuntu20:~$ cd PrimerPrep
fraser@vm-ubuntu20:~/PrimerPrep$ python3 ./PrimerPrep.py
```

Happy PrimerPrepping!

## 4. (Optional) Delete unneeded files from the PrimerPrep repository

Most of the files that are downloaded from `git` aren't actually needed to run PrimerPrep on Linux. In particular, the `.git` folder contains all the version control history information for the PrimerPrep repository, which is not needed to run PrimerPrep. If you need to save storage space, you can navigate to the PrimerPrep folder in a Terminal window (`~/PrimerPrep` in my case): 
```
cd ~/PrimerPrep
```
Then CAREFULLY type the following command: 
```
rm -rf .git
```
> [!WARNING]
> The `rm -rf` command is VERY dangerous, as it removes the folder with the given name and all of its subfolders _without asking for any confirmation_. So make sure you are deleting the right folder!

*Questions? Contact Fraser Bennett or Jeff Heath. There is contact information for Jeff at the bottom of the PrimerPrep Help file.
Or you can report issues on the [GitHub issue tracker](https://github.com/jeffheath-sil/PrimerPrep/issues)*.
