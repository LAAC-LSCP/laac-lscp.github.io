---
layout: default
title: Writing your codes
nav_order: 9
description: "Good practices and standardized way of codes in the team"
---
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

# Advantages of implementing Coding Standards

1. Offers uniformity to the code created by different engineers.
2. Enables the creation of reusable code.
3. Makes it easier to detect errors.
4. Make code simpler, more readable, and easier to maintain.
5. Boost programmer efficiency and generate faster results.

# Good practices

## Focus on code readability
1. Readable code is easy to follow, optimizes space and time. Here are a few ways to achieve that:
2. Write as few lines as possible.
3. Use appropriate naming conventions.
4. Segment blocks of code in the same section into paragraphs.
5. Use indentation to marks the beginning and end of control structures. Clearly specify the code between them.
6. Don’t use lengthy functions. Ideally, a single function should carry out a single task.
7. Use the DRY (Don’t Repeat Yourself) principle. Automate repetitive tasks whenever necessary. The same piece of code should not be repeated in the script.
8. Avoid Deep Nesting. Too many nesting levels make code harder to read and follow.
9. Avoid long lines. It is easier for humans to read blocks of lines that are horizontally short and vertically long.

## Standardize headers for different modules

It is easier to understand and maintain code when the headers of different modules align with a singular format. For example, each header should contain:

- Module Name
- Date of creation
- Name of creator of module
- History of modification
- Summary of what the module does
- Functions in that module
- Variables accessed by the module

## Don’t use a single identifier for multiple purposes - Naming conventions

Ascribe a name to each variable that clearly describes its purpose. Naturally, a single variable can’t be assigned multiple values or used for numerous functions. This would confuse everyone reading the code and would make future enhancements more difficult to implement. Always assign unique variable names.

### Naming your file

The naming of the file matters as it is supposed to give a hint on what the script does but cannot be too long or explanatory. You scripts shoud be stored under a `code` or `scripts` folder. 
Use a verb in the name to characterize the action of the script. You should try to limit the length 
of the names to 5 words max.

Never use the ' ' blank space character in your names and separate words by using underscores '_'. 

Preferably write everything in lowercase and of course, your python files should end with the '.py' 
extension.

## Turn daily backups into an instinct

Multiple events can trigger data loss – system crash, dead battery, software glitch, hardware damage, etc. To prevent this, save code daily, and after every modification, no matter how minuscule it may be. Backup everything on github/Gin.

## Leave comments and prioritize documentation

Don’t assume that just because everyone else viewing the code is your fellow colleague/researcher, they will instinctively understand it without clarification. People reading your code are human, and it is a lot easier for them to read comments describing code functions rather than scanning the code and making speculations.

Take an extra minute to write a comment describing the code function at various points in the script. Ensure that the comments guide any readers through the algorithm and logic implemented. Of course, this is only required when the code’s purpose is not apparent. Don’t bother leaving comments on self-explanatory code.

It is extremely important when writing a new script to document its purpose and actions to make sure anybody wanting to reuse it will be quickly able to tell what it was intended for and how it goes about doing it in broad terms.

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

## Make your code portable
Portability is a key aspect that ensures functionality of your program. If your code contains literal (hard-coded) values of environmental parameters, such as usernames, directory paths, it will not run on a host having a different configuration than yours.


In order to tackle this, you would have to ‘parametrize’ variables and configure them before running your software in different environments. This can be controlled with property files, databases, or application servers.

-can provide example of shutil package-
 
## Writing your codes in a reusable and scalable way

<a href="/images/myw3schoolsimage.jpg" download>
  <img src="/images/myw3schoolsimage.jpg" alt="W3Schools">
</a>
In coding, reusability is an essential design goal.
Because if modules and components have been tested already, a lot of time can be saved by reusing them. By reusing existing software components and modules, you can cut down on development time and resources.
Another key aspect to pay attention to is the ‘scalability’ of code. New features and improvements can be easily added to your code and other projects can be built upon it. Therefore, the ability to incorporate updates is an essential part of the software design process.

