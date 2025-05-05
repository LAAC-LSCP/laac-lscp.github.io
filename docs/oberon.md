---
layout: default
title: Oberon
nav_order: 6
description: "Working on the lab server: Oberon"
---

# Working on the lab server: Oberon

## Access

Oberon is used to give everybody a server to work on, store ongoing projects and access the lab's datasets. The server runs a linux system (centOS), which means that the usual way of using it is via the command line. 

Set up your SSH connection to oberon following the [CoML wiki](https://wiki.cognitive-ml.fr/resources/ssh.html#ssh-configuration-file){:target="_blank"} (you will need your oberon username and password).

## Directories and usage

Read how [data storage](https://wiki.cognitive-ml.fr/resources/cluster/architecture.html?highlight=storage#data-storage){:target="_blank"} is organized on oberon. By default, your `/scratch2/username` directory is readable by everyone.
You must organize your directory in different folders with suitable permissions: see [recommended set up](#recommended-set-up-for-personal-directory)

Most of the laac datasets are stored in `/scratch1/data/laac_data` as backups. You can explore it and use the datasets as needed but you should not have to edit them. If you notice any fault with the datasets please inform a member of the team to enforce the required changes.

Your main working directory is `/scratch2/username`, you should store your ongoing projects there. We use [datalad](https://handbook.datalad.org/){:target="_blank"} and [childproject](https://childproject.readthedocs.io/en/latest/introduction.html){:target="_blank"} to interact with the datasets we utilize. We want you to create a datalad directory (in appliance with the [YODA principles](http://handbook.datalad.org/en/latest/basics/101-127-yoda.html){:target="_blank"} : ie dataset nesting) for each project you lead. This will allow you to keep a record of the evolution of your project and to publish it easily to an online repository. To create your projects, you can follow the [YODA projects](./yoda-projects) instructions.

Storage space is not infinite, when you finished working on a project, clean you directories and [unload the datasets (or large files)](http://docs.datalad.org/en/latest/generated/man/datalad-drop.html){:target="_blank"} you don’t need anymore.

When working on your personal computer, it is advised most of the time to work on oberon through a ssh connection. However, if you have to work locally with non public datasets, you must have permission and store them on an encrypted drive. You should avoid carrying it around and the data should be deleted as soon as your work is finished.

## Conda environments

In order to use libraries and programms that are not by default installed on oberon, we use [conda](https://docs.conda.io/en/latest/){:target="_blank"} environments. The conda CLI can be used but we recommend using micromamba instead (works the same way), both can be loaded with `module load` commands (run `module avail` for a list of available modules).
A list of useful environments is made available to laac members. Those environments cannot be modified and aim at providing members with the commonly used environments without requiring them to install their own. They can be found in the `/scratch1/data/laac_data/conda` folder. The following environments are available:
- CP-laac (`/scratch1/data/laac_data/conda/CP-laac`) : Contains the most common packages we use when interacting with datasets (childproject, datalad, git-annex). It is intended to be the default environment to use when working on the server. Add the line `conda activate /scratch1/data/laac_data/conda/CP-laac` to the bottom of your `~/.bashrc` file to activate it by default when you log in the server.
- ALICE-laac (`/scratch1/data/laac_data/conda/ALICE-laac`) : Contains the required packages to run the ALICE model on the cluster. It is intended to be used only in jobs submitted to slurm (ad running models outside of slurm jobs is proscribed). Add the line `micromamba activate /scratch1/data/laac_data/conda/ALICE-laac` in your job script running ALICE.

For specific projects and when you need specific packages, you may need to set up your own conda environment (once not useful anymore, you should remove it). [Install the environment in your working directory](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#specifying-a-location-for-an-environment){:target="_blank"} `/scratch2/username` and not in the default location `~/.conda/envs` by using the `-p` option. Otherwise, you could run out of space quickly. For example if creating an environment from a yaml file named `env.yml` , I can use the command `conda env create -f env.yml -p /scratch2/lpeurey/conda/projectX-env` to create a new environment named projectX-env in my personal space.

## Jobs

Read [how jobs are managed](https://wiki.cognitive-ml.fr/resources/cluster/launching_jobs.html){:target="_blank"} on oberon (ie programs that require a lot of resources). Once a job is launched, it will continue running even if you close your connection to oberon. This is a good way to launch computation for times you are not able to be connected.
If you are unsure of what you’re doing, Loann can help.

## Helpful configurations

To facilitate using those different principles, here is an example of a bashrc file (file executed upon entering a session) along with descriptions of its content. Your file should be in `/home/username/.bashrc` (replace username by your username).

breakdown:
 - lines 1 to 18 are default content, leave it unchanged unless you know what you are doing
 - lines 20 to 30 are to set up colored terminal, the color can be changed with color codes
 - lines 32 to 39 configures the prompt to be user@host:dir
 - lines 41 to 48 includes auto coloring for usual commands
 - lines 50 and 51 will automatically change your working directory to your workspace upon login, this is useful to not accidentally use /home for work projects (see [directories usage](#directories-and-usage)), change the username in this line to be yours.
 - lines 53 to 56 edits the default permissions given to new files. This umask (0007) will give write permissions to the group but no permission to other users. This is good for collaborative work in the team, on data that should not be accessible to everyone. When using this, all your work is accessible to the team, so if you have folders you don't want shared within the team, remember to edit the permissions for those
 - lines 58 to 73 loads automatically the conda/micromamba commands and activate the shared ChildProject environment, this will save you time at login, steps are different for each node, feel free to add node specific setups there

You can use this entire file or parts of it in your own setup. Remember to change placeholders (like usernames) when needed.
```bash
# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions
if [ -f ~/.firstlog ]
then
  ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa
  cp ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys
  chmod 600 ~/.ssh/authorized_keys
  rm -f ~/.firstlog;
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;35m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls="ls --color=auto"
    alias grep="grep --color=auto"
    alias fgrep="fgrep --color=auto"
    alias egrep="egrep --color=auto"
fi

#go to scratch2/lpeurey by default
if [ $(pwd) = "/home/lpeurey" ] ; then cd /scratch2/lpeurey/ ; fi

#umask to 0007 to:
# - give write permissions to group
# - remove all permisions to other
umask 0007

if [ $(hostname) = "oberon2" ]; then
  # oberon2 config
  module load micromamba/1.4.2-jnhh
  eval "$(micromamba shell hook --shell=bash)"
  alias conda="echo 'Using micromamba instead of conda' && micromamba"
  micromamba activate /scratch1/data/laac_data/conda/CP-laac
elif [ $(hostname) = "habilis" ]; then
  # habilis config
  load_conda
  conda activate /scratch1/data/laac_data/conda/CP-laac
elif [[ $(hostname) == "puck"* ]]; then
  # compute nodes setup
  module load micromamba/1.4.2-jnhh
  eval "$(micromamba shell hook --shell=bash)"
  alias conda="echo 'Using micromamba instead of conda' && micromamba"
fi
```

## Recommended set up for personal directory

### Structure

At the root of the directory, we have 3 folders with different permissions for different use:
- `personal` will contain anything that should not be shared with anyone.
- `laac` is accessible by the laac users who have been granted access to the data. You can store private data here.
- `shared` is accessible by everybody on the cluster. You can use it for non sensitive projects.

You can also create folders for other teams if you work with them and should restrict the access to only their members.

### Creating it

Replace \<username\> by your actual username in all the commands.

First navigate to your working directory:
```bash
[username@oberon ~]$ cd /scratch2/username
[username@oberon username]$
```

Create the 3 directories:
```bash
[username@oberon username]$ mkdir personal laac shared
[username@oberon username]$ ls
laac  personal  shared
```

Set the permissions for each of them:
```bash
[username@oberon username]$ chown :laac laac
[username@oberon username]$ chmod 750 laac
[username@oberon username]$ chmod g+s laac
[username@oberon username]$ chmod 700 personal
[username@oberon username]$ chmod 755 shared
```

Check the new permissions:
```bash
[username@oberon username]$ ls -la
total 8
drwxr-xr-x  5 username bootphon   64 Sep 23 13:28 .
drwxr-xr-x 62 root     root     4096 Jan  3 10:58 ..
drwxr-s--- 14 username laac     4096 Nov 28 14:02 laac
drwx------  4 username bootphon   90 Oct 13 15:19 personal
drwxr-xr-x  3 username bootphon   34 Oct 26 11:47 shared
```

The permissions listed in the left should be the same for each directory.

You now have a ready to use structure to organize and store your projects and data :)
