---
layout: default
title: Oberon
nav_order: 6
description: "Working on the lab server: Oberon"
---

# Working on the lab server: Oberon

## Access

Oberon is used to give everybody a server to work on, store ongoing projects and access the lab's datasets. The server runs a linux system (centOS), which means that the usual way of using it is via the command line. 

Set up your SSH connection to oberon following the [CoML wiki](https://wiki.cognitive-ml.fr/servers/ssh.html){:target="_blank"} (you will need your oberon username and password).

## Directories and usage

Read how [data storage](https://wiki.cognitive-ml.fr/cluster/architecture.html#data-storage){:target="_blank"} is organized on oberon. By default, your `/scratch2/username` directory is readable by everyone.
You must organize your directory in different folders with suitable permissions: see [recommended set up](#recommended-set-up-for-personal-directory)

Most of the laac datasets are stored in `/scratch1/data/laac_data` as backups. You can explore it and use the datasets as needed but you should not have to edit them. If you notice any fault with the datasets please inform a member of the team to enforce the required changes.

Your main working directory is `/scratch2/username`, you should store your ongoing projects there. We use [datalad](https://handbook.datalad.org/){:target="_blank"} and [childproject](https://childproject.readthedocs.io/en/latest/introduction.html){:target="_blank"} to interact with the datasets we utilize. We want you to create a datalad directory (in appliance with the [YODA principles](http://handbook.datalad.org/en/latest/basics/101-127-yoda.html){:target="_blank"} : ie dataset nesting) for each project you lead. This will allow you to keep a record of the evolution of your project and to publish it easily to an online repository. To create your projects, you can follow the [YODA projects](./yoda-projects) instructions.

Storage space is not infinite, when you finished working on a project, clean you directories and [unload the datasets (or large files)](http://docs.datalad.org/en/latest/generated/man/datalad-drop.html){:target="_blank"} you don’t need anymore.

When working on your personal computer, it is advised most of the time to work on oberon through a ssh connection. However, if you have to work locally with non public datasets, you must have permission and store them on an encrypted drive. You should avoid carrying it around and the data should be deleted as soon as your work is finished.

## Conda environments

In order to use libraries and programms that are not by default installed on oberon, we use [conda](https://docs.conda.io/en/latest/){:target="_blank"} environments. A list of useful environments is made available to laac members. Those environments cannot be modified and aim at providing members with the commonly used environments without requiring them to install their own. They can be found in the `/scratch1/data/laac_data/conda` folder. The following environments are available:
- CP-laac (`/scratch1/data/laac_data/conda/CP-laac`) : Contains the most common packages we use when interacting with datasets (childproject, datalad, git-annex). It is intended to be the default environment to use when working on the server. Add the line `conda activate /scratch1/data/laac_data/conda/CP-laac` to the bottom of your `~/.bashrc` file to activate it by default when you log in the server.

For specific projects and when you need specific packages, you may need to set up your own conda environment (once not useful anymore, you should remove it). [Install the environment in your working directory](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#specifying-a-location-for-an-environment){:target="_blank"} `/scratch2/username` and not in the default location `~/.conda/envs` by using the `-p` option. Otherwise, you could run out of space quickly. For example if creating an environment from a yaml file named `env.yml` , I can use the command `conda env create -f env.yml -p /scratch2/lpeurey/conda/projectX-env` to create a new environment named projectX-env in my personal space.

## Jobs

Read [how jobs are managed](https://wiki.cognitive-ml.fr/cluster/launching_jobs.html){:target="_blank"} on oberon (ie programs that require a lot of resources). Once a job is launched, it will continue running even if you close your connection to oberon. This is a good way to launch computation for times you are not able to be connected.
If you are unsure of what you’re doing, Loann can help.

## Helpful configurations

To facilitate using those different principles, here are some operations you can conduct to configure your workspace.

- Landing in your working directory (`/scratch2/username`) when logging in oberon (dont forget to change <username> by your actual oberon username):
  ```bash
  echo -e "\n#land in your working directory when logging in\ncd /scratch2/username" >>~/.bashrc
  ```
- Activate the childproject environment when logging in (to activate another environment by default, change the environment name in the command):
  ```bash
  echo -e "\n#activate childproject environment when logging in\nconda activate /scratch2/lpeurey/conda/childproject" >>~/.bashrc
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
