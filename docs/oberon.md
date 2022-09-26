---
layout: default
title: Oberon
nav_order: 6
description: "Working on the lab server: Oberon"
---

# Working on the lab server: Oberon

## Access

Set up your SSH connection to oberon following the [CoML wiki](https://wiki.cognitive-ml.fr/servers/ssh.html){:target="_blank"} (you will need your oberon username and password).

## Directories and usage

Read how [data storage](https://wiki.cognitive-ml.fr/cluster/architecture.html#data-storage){:target="_blank"} is organized on oberon. By default, your /scratch2/username directory is readable by everyone. If you are familiar with linux permissions, restrict the access to anyone not in the laac group. If not, ask Loann.

Most of the laac datasets are stored in /scratch1/data/laac_data as backups. You can explore it and get the datasets you need from there but you should not have to edit them.

Your main working directory is /scratch2/username, you should store your ongoing projects there. We use [datalad](https://handbook.datalad.org/){:target="_blank"} and [childproject](https://childproject.readthedocs.io/en/latest/introduction.html){:target="_blank"} to interact with the datasets we utilize. We want you to create a datalad directory (in appliance with the [YODA principles](http://handbook.datalad.org/en/latest/basics/101-127-yoda.html){:target="_blank"} : ie dataset nesting) for each project you lead. This will allow you to keep a record of the evolution of your project and to publish it easily to an online repository. To create your projects, you can follow the [YODA projects](./yoda-projects) instructions.

Storage space is not infinite, when you finished working on a project, clean you directories and [unload the datasets (or large files)](http://docs.datalad.org/en/latest/generated/man/datalad-drop.html){:target="_blank"} you don’t need anymore.

When working on your personal computer, it is advised most of the time to work on oberon through a ssh connection. However, if you have to work locally with non public datasets, you must have permission and store them on an encrypted drive. You should avoid carrying it around and the data should be deleted as soon as your work is finished.

## Conda environments

In order to use libraries and programms that are not by default installed on oberon, we use [conda](https://docs.conda.io/en/latest/){:target="_blank"} environments. The usual environments we use (mostly the childproject environment which contains all the software to interact with childproject datasets) are stored in `/scratch2/lpeurey/conda`. You should use those environments when working on oberon.

On rare occasions, you may need to set up your own conda environment (once not useful anymore, you should remove it). [Install the environment in your working directory](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#specifying-a-location-for-an-environment){:target="_blank"} /scratch2/username and not in the default location /home/username by using the `-p` option. Otherwise, you could run out of space quickly.

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