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

Your main working directory is /scratch2/username, you should store your ongoing projects there. We use [datalad](https://handbook.datalad.org/){:target="_blank"} and [childproject](https://childproject.readthedocs.io/en/latest/introduction.html){:target="_blank"} to interact with the datasets we utilize. We want you to create a datalad directory (in appliance with the [YODA principles](http://handbook.datalad.org/en/latest/basics/101-127-yoda.html){:target="_blank"} : ie dataset nesting) for each project you lead. This will allow you to keep a record of the evolution of your project and to publish it easily to an online repository. To create your projects, you can follow the [YODA projects](./yoda-projects){:target="_blank"} instructions.

Storage space is not infinite, when you finished working on a project, clean you directories and [unload the datasets (or large files)](http://docs.datalad.org/en/latest/generated/man/datalad-drop.html){:target="_blank"} you don’t need anymore.

When working on your personal computer, it is advised most of the time to work on oberon through a ssh connection. However, if you have to work locally with non public datasets, you must have permission and store them on an encrypted drive. You should avoid carrying it around and the data should be deleted as soon as your work is finished.

You will probably use [conda](https://docs.conda.io/en/latest/) environements on the server. [Install them in your working directory](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#specifying-a-location-for-an-environment){:target="_blank"} /scratch2/username and not in the default location /home/username. Otherwise, you could run out of space quickly.

## Jobs

Read [how jobs are managed](https://wiki.cognitive-ml.fr/cluster/launching_jobs.html){:target="_blank"} on oberon (ie programs that require a lot of resources). If you are unsure of what you’re doing, Loann can help.