---
layout: default
title: Child Project
nav_order: 7
description: "Manipulating and utilizing scientific data: the childProject library"
---

# Manipulating and utilizing scientific data: the ChildProject library

## What is Childproject?

Childproject is a python package that is intended to help researchers organize manipulate and share their data. It has been made with the usage of long-form recordings of children in mind. Along with organization and manipulation, the aspect of versioning and sharing the data is equally important, this is handled by [datalad](https://handbook.datalad.org/){:target="_blank"} and works together with childproject.

The complete documentation of the package and explanations on how to utilize it can be found [here](https://childproject.readthedocs.io){:target="_blank"}.

## What childproject provides

Childproject provides two ways of interacting with your dataset:
- [A command line interface (CLI)](https://childproject.readthedocs.io/en/latest/tools.html){:target="_blank"} : this will give you quick and easy access to the usual operations you would want with a simple command call.
- [A python API](https://childproject.readthedocs.io/en/latest/api-annotations.html){:target="_blank"} : this will allow you to code more custom and in detail operations while having an easy access and modification of the project files.

Childproject is based on a specific file structure to organize and save your dataset. This structure is detailed [here](https://childproject.readthedocs.io/en/latest/format.html){:target="_blank"}. Once all your files are saved accordingly and your metadata files are ready, you can start running commands and writing your scripts with the API.

## Use it on oberon

In oberon, we provide a ready to use conda environment with childproject. You will likely use childproject a lot on the server when working with datasets.
To activate it, run:
```bash
conda activate /scratch2/lpeurey/conda/childproject
```
From there, you will be able able to run all the childproject features without further installs.

Please do not edit this environment (i.e. do not run `pip install` or `conda install` commands inside the environment). If you have specific needs for your project, [build a personal environment](./oberon.md#conda-environments){:target="_blank"}, if you think additional libraries should be installed in this shared environment (e.g. for bug fix, additional features), tell Loann about it.

You may want to automatically activate the childproject environment on login, to do so, refer to [this section](./oberon.md#helpful-configurations){:target="_blank"}

## Some literature:

- [Managing, storing, and sharing long-form recordings and their annotations. Language Resources and Evaluation.](https://psyarxiv.com/w8trm/download?format=pdf){:target="_blank"}(Gautheron, L., Rochat, N., & Cristia, A. (2021))

---

- [Long-form recordings: From A to Z](https://bookdown.org/alecristia/exelang-book/){:target="_blank"}(Pisani, S., Gautheron, L., & Cristia, A. (2021))

---

- [Childproject documentation](https://childproject.readthedocs.io){:target="_blank"}