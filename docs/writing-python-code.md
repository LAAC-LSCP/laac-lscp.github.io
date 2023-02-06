---
layout: default
title: Writing python code
nav_order: 9
description: "Good practices and standardized way of writing python scripts in the team"
---

# Writing you python scripts in a reusable way
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

{: .label .label-yellow }
WIP

This page is intended for people who are writing simple callable python scripts to be run on their data. 
It does not apply to writing entire python packages with multiple use cases. 

## Documenting your script

It is extremely important when writing a new script to document its purpose and actions to make sure
anybody wanting to reuse it will be quickly able to tell what it was intended for and how it goes
about doing it in broad terms.

### Naming your file

The naming of the file matters as it is supposed to give a hint on what the script does but cannot
be too long or explanatory. You scripts shoud be stored under a `code` or `scripts` folder

Use a verb in the name to characterize the action of the script. You should try to limit the length 
of the names to 5 words max.
Never use the ' ' blank space character in your names and separate words by using underscores '_'. 
Preferably write everything in lowercase and of course, your python files should end with the '.py' 
extension.

### Docstrings

Docstrings are a way of documenting your script by attaching an explanation to code modules, 
functions, classes etc. You can read more about them [here](https://peps.python.org/pep-0257/){:target="_blank"}.

You should try to use docstrings as much as possible to describe what each of your functions, 
modules and so on do.

The first step is giving a docstring to your entire script, place it at the very top and give
at least the date it was created on and the author (yourself), you can also add any relevant 
general info. Then describe the general goal and actions of the script.

Secondly, remember to give a docstring to every function or class you write. We are mostly using
the reST format for our documentation, you can read more on how to use this format [here](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html){:target="_blank"}.

## Our recommended sctructure

The code structure we propose here is designed for the code to be easily callable as a script 
but also to be imported by other programs if need be.

### Separate the code between callable and importable

The script we write must be both importable and runnable
Do not write code outside of functions and classes unless it has to run everytime in all 
situations.
Create a argparse function where you specify the arguments when calling the function.
Create the "if __name__ == '__main__' :" section that will run only when called.
Create a main function to be called with the arguments for dfining the behaviour when used as 
a callable script.

### the logger

The `logger` module in python is used to log information about how the program is running and 
potential warnings, errors it encounters. Whereas the `print` statement should only be used as 
a text output for a running program.