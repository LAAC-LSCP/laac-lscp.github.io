---
layout: default
title: New Dataset
nav_order: 10
description: "Create a new dataset to be published to GIN"
---

# Creating a Dataset and publishing it to GIN
{: .no_toc }

This page is here to help you create a new Dataset following the ChildProject structure using data that has not been organized this way yet. 

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Prerequisites

In order to follow this guide, you will need to have childproject installed along with datalad and git-annex. If that is not the case, follow the [installation instructions](https://childproject.readthedocs.io/en/latest/install.html#installation){:target="_blank"}. You most likely will run it in a conda environment, so make sure it is activated:
```bash
conda activate childproject
```

We use [GIN](https://gin.g-node.org/){:target="_blank"} as an online platform for storing our repositories. To publish your dataset, you will need a GIN account that has writing permissions for your dataset. You should have created an account already, if not do it [here](https://gin.g-node.org/user/sign_up){:target="_blank"}. Once you have an account, Loann/Alex should give you writing permissions on a dataset within the LAAC-LSCP organization.
For every new computer that you will use to push updates to your dataset, You have to register an SSH key to allow SSH access (you can find an explanation of what SSH keys are and how you can create one in this [tutorial](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/about-ssh){:target="_blank"}). You only need to do this once per computer, and it'll be set for all of your datasets & forever. To set SSH access, visit the [settings of your user account](https://gin.g-node.org/user/settings/ssh){:target="_blank"}. In the “SSH Keys” tab, click the button “Add Key”:
![Add your SSH key](../ressources/img/gin-add-ssh.png)
Give the key an informative name that will allow you to remember what computer it belongs to (eg “oberon-lpeurey”).

## Preparing a GIN repository

We are going to need a new repository on GIN where we will store our dataset and manage people's access to it once it is ready to be shared.
Inside the lab, we regroup our datasets in the LAAC-LSCP GIN organization, so the dataset should be created there. If you have the permissions necessary to create a new repository for the organization, follow the steps in the attached figure. If you are an intern, discuss with Alex/Loann of your need of a new repository.
Unless your dataset is public (e.g. from CHILDES), you'll need a confidential version of the repository, create two **empty** repositories in your GIN organization: `<dataset-name>` and `<dataset-name>-confidential`, e.g. `mydataset` and `mydataset-confidential`.
![Create your Gin repository](../ressources/img/create-gin-repo.png)

## Creating the base structure and datalad repository

### Installating the procedures

To create your new dataset, we will borrow some help from the `datalad-procedures` code which was created for this specific pupose. If you have already created a dataset in the past, your procedures may already be set up. 
To check your available templates, run `datalad run-procedure --discover` and explore the outputted list:
```
cfg_laac1 (/my/conda/env/lib/python3.6/site-packages/datalad/resources/procedures/cfg_laac1.py) [python_script]
cfg_yoda (/my/conda/env/lib/python3.6/site-packages/datalad/resources/procedures/cfg_yoda.py) [python_script]
cfg_el1000 (/my/conda/env/lib/python3.6/site-packages/datalad/resources/procedures/cfg_el1000.py) [python_script]
cfg_text2git (/my/conda/env/lib/python3.6/site-packages/datalad/resources/procedures/cfg_text2git.py) [python_script]
cfg_metadatatypes (/my/conda/env/lib/python3.6/site-packages/datalad/resources/procedures/cfg_metadatatypes.py) [python_script]
cfg_laac2 (/my/conda/env/lib/python3.6/site-packages/datalad/resources/procedures/cfg_laac2.py) [python_script]
```

If you spot `cfg_laac1`, `cfg_laac2` and `cfg_el1000` in the list, you are already good to go and can skip to the [next section](#using-templates). If they are not here, we will have to install them. To do so, clone the repo (or navigate to it if you already have it) and launch the installation :
```bash
git clone git@github.com:LAAC-LSCP/datalad-procedures.git
cd datalad-procedures
pip install -r requirements.txt
python install.py
```
At this point, a message may ask you if you want to establish a fingerprint; say yes.

Check again the available templates with `datalad run-procedure --discover`.
You should now have `cfg_laac1`, `cfg_laac2` and `cfg_el1000` in the outputted list.

### Using templates

We will concentrate on using the el1000 template which is the one we will use most of the time. You can read more about that configuration and the other templates available in [the repo](https://github.com/LAAC-LSCP/datalad-procedures){:target="_blank"}.

With the next set of commands, we prepare the necessary parameters by setting the GIN organization you will use and wether to create a confidential sibling or not. If you use a confidential sibling, make sure you created 2 repositories on GIN at [the previous step](#preparing-a-gin-repository)
```bash
export GIN_ORGANIZATION='LAAC-LSCP' # name of the GIN organization
export CONFIDENTIAL_DATASET=0 # set to 1 if there should be a confidential sibling
```
Now we can create the actual datalad repository, the procedure used will build the file structure according to [ChildProject standards](https://childproject.readthedocs.io/en/latest/format.html){:target="_blank"}. First change directory to where you want your new dataset created, then create it. Replace `mydataset` by the name of your GIN repository.
```bash
cd /path/to/a/folder #change directory
datalad create -c el1000 mydataset
```

The output you'll see looks like this:
```
[INFO   ] Creating a new annex repo at /scratch2/lpeurey/datasets/mydataset/
[INFO   ] Scanning for unlocked files (this may take some time) 
[INFO   ] Running procedure cfg_el1000 
[INFO   ] == Command start (output follows) ===== 
[INFO   ] Could not enable annex remote origin. This is expected if origin is a pure Git remote, or happens if it is not accessible. 
[WARNING] Could not detect whether origin carries an annex. If origin is a pure Git remote, this is expected.  
.: origin(-) [git@gin.g-node.org:/LAAC-LSCP/mydataset.git (git)]
.: origin(+) [git@gin.g-node.org:/LAAC-LSCP/mydataset.git (git)]                       
[INFO   ] Could not enable annex remote confidential. This is expected if confidential is a pure Git remote, or happens if it is not accessible. 
[WARNING] Could not detect whether confidential carries an annex. If confidential is a pure Git remote, this is expected.  
.: confidential(-) [git@gin.g-node.org:/LAAC-LSCP/mydataset-confidential.git (git)]
.: confidential(+) [git@gin.g-node.org:/LAAC-LSCP/mydataset-confidential.git (git)]    
[INFO   ] Configure additional publication dependency on "confidential"         
.: origin(+) [git@gin.g-node.org:/LAAC-LSCP/mydataset.git (git)]
[INFO   ] == Command exit (modification check follows) ===== 
create(ok): /scratch2/lpeurey/datasets/mydataset/ (dataset)
```

The procedure should also carry out the first push to your remote repository(/ies). You should have a look to the online page of your repo on GIN (eg https://gin.g-node.org/LAAC-LSCP/mydataset-confidential)
![Explore your GIN repo online](../ressources/img/first-push.png)

The content looks odd?
{: .label .label-yellow }
Your default branch may be set to 'git-annex', change this in the settings:
![Explore your GIN repo online](../ressources/img/default-branch_git-annex.png)
![Explore your GIN repo online](../ressources/img/change-default-branch.png)

Once you GIN repository is set up and correctly linked to you local directory, you should always remember to often save and push the modifications you make to the online storage. This is done by using:
```bash
# save the changes locally
datalad save . -m "message about what changes were made"

# publish
datalad push
```

## Organizing raw data

Your dataset has been created, configured and linked to GIN. But for now,
it has no contents.
The next step is thus to add raw data to the dataset in the right place.

There are two possibilites (depending on whether you created a confidential repository or not):
 1. Some data are confidential and should only be accessible from `<your-dataset>-confidential`
 2. All data can be included in the main version of the dataset

### How confidential data is organized and stored

Here is the rule: every file that is a descendant of a `confidential` folder will be restricted
to users that have read access to `<your-dataset>-confidential`; any other file will
be shared with all users who have read access to your dataset.

Here are a few examples:

#### Files that would be confidential

 - `metadata/confidential/whatever.csv`
 - `annotations/its/confidential/raw/something.its`
 - `annotations/its/confidential/converted/something.csv`
 - `annotations/eaf/confidential/raw/some/annotation.eaf`

#### Files that will not be

  - `metadata/somefile.csv`
  - `annotations/its/raw/something.csv`

It is therefore crucial to organize your data in the right place depending on its level of sensitivity.

### Audio files

TODO : Add information on how to store/convert audio files, best practice, confidentiality.

### Original Metadata

The original metadata is likely to contain sensitive information, so if you have a confidential sibling, it should be restricted to the `confidential` version of the dataset.
Therefore, most of the time, your original metadata should lie in `metadata/confidential/original`. Otherwise, store it in `metadata/original`.

```bash
# cd to your dataset
cd <your-dataset>

# create an empty folder for the original metadata
mkdir -p metadata/confidential/original
```

### LENA annotations

.its annotations contain information that may be used to identify the participants (such as their date of birth). So you should consider storing them as confidential.

```bash
# create an empty folder for the .its
mkdir -p annotations/its/confidential/raw
```

Your .its files should be saved at the root of `annotations/its/confidential/raw` or `annotations/its/raw` depending on if they are to be kept confidential or not.

If you stored them as confidentiel, an anonymized version of the .its should be created. This is done with the [ChildProject package](https://childproject.readthedocs.io/en/latest/annotations.html#its-annotations-anonymization){:target="_blank"}:

```bash
child-project anonymize . --input-set its/confidential --output-set its
```

This may take some time.
Once the command has completed, anonymized .its files should be accessible from `annotations/its/raw`:

```bash
ls annotations/its/raw
123417-0008.its	123461-0713.its	123505-1620.its	123549-2417.its ...
```

### Other data

 - VTC annotations (.rttm files) should be moved to `annotations/vtc/raw`
 - VCM annotations (.rttm files) should be moved to `annotations/vcm/raw`
 - ALICE annotations (.txt files) should be moved to `annotations/alice/output/raw`
 - Any other kind of annotation should be moved to `annotations/<location>/raw/`
 - Other files (documentation, etc.) should be moved to `extra/`

You can create empty folders with `mkdir -p`, e.g. `mkdir -p annotations/vtc/raw`.

### Save and publish

Once all your raw data have been correctly placed in the new dataset, you need to save
the changes and publish them on GIN :

```bash
# save the changes locally
datalad save . -m "message about what changes were made"

# publish
datalad push
```

## Link everything : The new metadata

We now need to create the metadata files that childproject uses to link all the files together.
For an overview of the files needed and their format, head to [ChildProject format](https://childproject.readthedocs.io/en/latest/format.html){:target="_blank"}

After the creation is finished, don't forget to save and push your changes.
```bash
datalad save . -m "message about what changes were made"
datalad push
```

### Create the metadata from the its information

One common way to create the metadata is to extract it from the its files you have. This was done in many cases, scripts were save in this [repo](https://gin.g-node.org/EL1000/tools){:target="_blank"} and instructions can be found in this [section](https://gin.g-node.org/EL1000/tools/src/master/HOWTO.md#importing-the-metadata){:target="_blank"}

You can explore those scripts but be aware that they will need some degree of adaptation for each dataset.

We recommend that you copy an example from a dataset which original data look like yours, and save it to scripts/metadata.py. Then you can make all necessary changes.

### Example of manual creation

If you can't extract the metadata from .its files, you should find another way of creating the metadata. You should prioritize methods that rely on a script that is saved in your dataset to make sure you keep a trace of where the metadata came from and maybe in the future use a similar script for another dataset.
You can have a look at this pratical [example](https://childproject.readthedocs.io/en/latest/vandam.html#create-the-metadata){:target="_blank"}. Even though this example is using information found in .its files, it can give you an idea of the steps involved and the way to procede.

## Import the annotations

Once again, like for creating metadata, the importation process can vary quite a bit depending on the annotations available to you and their format.

TODO: add instructions about importing the annotations.