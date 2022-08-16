---
layout: default
title: running models
nav_order: 9
description: "Running model analysis on your data"
---

# Run models to obtain automated annotations for your project
{: .no_toc }

This guides assume you are using the childproject data structure and that you store you project in the **oberon** server.
They are meant to guide you run the models in the cluster to obtain automated annotations, import those new annotations to the childproject dataset and then upload the changes made to the dataset to gin.

We will be using your personal working directory on oberon a lot. Throughout this guide, we use the name `/scratch2/username`, always remember to put your own directory path by replacing 'username' with your actual oberon username.

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Prepare your audio files

All the models presented here were built to use audio files with a sampling rate of 16000 Hz. So before you go ahead and launch your computations, you should make sure that the audio files of the dataset have a 16kHz sampling rate or that a converted version of them exists in another audio profile (usually in recordings/converted/standard).

The very first step is to change your working directory to the root of the dataset as we will run most commands from there:
```bash
cd /path/to/dataset
```

### Check that audio files content is present

First make sure that you have the audio content present locally.
```bash
ls recordings/raw # or other profile recordings/converted/standard
```
should show you the audio in a blue color. If they appear red, the audio files are not present locally. Be careful downloading audio can be extremely lengthy and can take a lot of storage space. You should not have to do this for large datasets, you can refer to Loann or Alex in those occasions.
If you proceed with downloading the files, make sure datalad is available (activate your childproject environment with `conda activate childproject` if it is not) then use `datalad get recordings/raw/rec1.wav` for your files. Probably don't use `datalad get recordings/raw` on the whole folder as that would take forever and you would not be able able to close your connection to the cluster without stopping the command. Alternatively, use an oberon [job](https://wiki.cognitive-ml.fr/cluster/launching_jobs.html#launching-jobs){:target="_blank"} that will run separately to get all the files.

### Check the sampling rates (and other info about the audio)

To check what the sampling rate is, use `soxi` on your files:
```bash
[me@oberon]$ soxi recordings/raw/rec1.wav
->
Input File     : 'recordings/raw/rec1.wav'
Channels       : 1
Sample Rate    : 16000
Precision      : 16-bit
Duration       : 00:00:06.54 = 104640 samples ~ 490.5 CDDA sectors
File Size      : 209k
Bit Rate       : 256k
Sample Encoding: 16-bit Signed Integer PCM
```
You can run
```
p=recordings/raw ; echo  $(ls ${p}/*.wav | wc -l) wav files with $(soxi ${p}/*.wav | grep "Sample Rate    : 16000" | wc -l) of them having a 16kHz Sample Rate
```
Change the path to your recordings folder and run the command to see in one go how many files out of the total are sampled in 16kHz.

### Convert audio if necessary

In the event that your audios are not in 16KHz and that there are no existing converted profile in that rate, we will need to create that new audio profile.
We will use childproject's command so make sure that your environment is activated.
Use the [process command](https://childproject.readthedocs.io/en/latest/processors.html#basic-audio-conversion){:target="_blank"} of childproject and use slurm to give the job to the processing nodes of the cluster to convert your files.
```bash
sbatch --mem=64G --time=5:00:00 --cpus-per-task=4 --ntasks=1 -o convert-audio.log child-project process --threads 4 /path/to/dataset standard basic --format=wav --sampling=16000 --codec=pcm_s16le
```
This is a template command that usually is all we will need for conversion, don't forget to change the path to the root of your dataset.
You can also choose to modify the different options, for example provide a list of the recordings to process with `--recordings` or change the ressources you are asking for in the cluster. Use the [slurm user guide](https://slurm.schedmd.com/quickstart.html){:target="_blank"} and [childproject documentation](https://childproject.readthedocs.io/en/latest/processors.html#basic-audio-conversion){:target="_blank"} to see the available options.
Depending on the number of audio files you are converting and their durations, launching a conversion can take several minutes.

Once the conversion is done, you will most likely want those converted audio files saved in the dataset and published to the online repositories.
```bash
datalad save -m "converted audio to 16kHz" #to run from the root of the dataset
datalad push
```
Be aware that:
- the `save` command can take time because it encodes the audio files. If you have a large amount of data, consider asking for ressources on the cluster to do that.
- the `push` command will upload the content of the newly created files online, like for downloading, it will require a lot of time, if you want to close your session without interrupting your upload, once again consider using a job on the cluster to take care of it.

## Running the models

Everytime you add new annotations to a dataset, you need to organize them correctly for childproject. First, they will need to be in the annotations folder from the root of the dataset, then you must choose a name for this set of annotations, the name of the set is there to specify that all the annotations inside are of the same format and were produced together or serve the same purpose.

### Voice type classifier (VTC)

If you want both VTC and ALICE annotations, go directly to the ALICE section as ALICE can run both models in one go.
{: .label .label-yellow }

VTC is currently being reworked by the CoML team so a new version (and easier way to run the model) should soon replace this tutorial.
{: .label .label-red }

#### Installation

You should only install the repo and conda environment the first time. If you ran the model in the past, just reuse the same folder and conda environment.

The code for VTC is stored in [this github repo](https://github.com/MarvinLvn/voice-type-classifier/){:target="_blank"}. So the first step is to clone the repository in oberon, in a `/scratch2/username` subdirectory (don't forget to replace 'username' with your own username on oberon).
We made the choice here to store our VTC in a directory `modules` meant to store the different model repositories. You can create that folder if you want: `mkdir /scratch2/username/modules`.
```bash
cd /scratch2/username/modules
git clone --recurse-submodules https://github.com/MarvinLvn/voice-type-classifier.git #should take a dozens of seconds
cd voice-type-classifier
```
You now need to create the conda environment that will allow you to run the model and activate it. One easy way to keep everything together is to create that environment in the same directory and name it accordingly, so this is what we will do.
```bash
conda env create -p ./conda-vtc-env -f vtc.yml
```
The creation should last a few minutes. It happens more often than not that oberon is slowed down by other users, in that case this could take up to an hour.

You don't even need to activate the environment, the job used will take care of that itself.

#### Running it

We can't run the model directly on oberon as we need more ressources, so we will launch a [slurm job on oberon](https://wiki.cognitive-ml.fr/cluster/launching_jobs.html){:target="_blank"}.
You can use on of these script templates as a good starting point that you can then customize to your needs. Save the file in your vtc folder as `job-vtc.sh` for example and modify it for how you want to run vtc.

**To edit in the script:**
{: .label .label-green }
- conda environment path : change the `conda activate` line with the path of your brand new environment
- dataset_path : give the path to the root of your dataset
- profile : if had to convert your audios, put `converted/standard` or the name of the profile to use, otherwise keep the default `raw`

One output file per audio
{: .label .label-blue }
This script will list all .wav files in the audio_path given, run VTC on each of them and move the results into the vtc/raw folder as default, renaming them with the name of the audio file they came from but as a rttm files instead of a wav one. 
```bash
#!/bin/bash
#SBATCH --job-name=vtc-mydata         # Job name
#SBATCH --partition=gpu               # Take a node from the 'gpu' partition
#SBATCH --cpus-per-task=2             # 2 CPU cores is fine as we use a GPU 
#SBATCH --gres=gpu:1                  # Ask for 1 gpu, usually a good idea for VTC
#SBATCH --time=48:00:00               # Time limit hrs:min:sec, default is 2h, which can be short for long form recordings
#SBATCH --output=%x-%j.log            # Standard output and error log

echo "Running job on $(hostname)"

# load conda environment
source /shared/apps/anaconda3/etc/profile.d/conda.sh
conda activate /scratch2/username/modules/voice-type-classifier/conda-vtc-env #!!!! EDIT THIS !!!!

# set the paths
dataset_path="/scratch2/username/datasets/mydata" #!!!! EDIT THIS !!!!
profile="raw" #!!!! EDIT THIS IF YOUR AUDIOS WERE CONVERTED !!!!

dataset_path=${dataset_path%/}
audio_path=${dataset_path}/recordings/${profile%/}
output_path=${dataset_path}/annotations/vtc/raw
mkdir -p ${output_path} #create output dir if does not exist

files=($(ls ${audio_path}/*.wav))
for c in "${!files[@]}"
do
  basename=$(basename ${files[$c]%.*})
  ./apply.sh ${files[$c]} --device=gpu
  mv output_voice_type_classifier/${basename}/all.rttm ${output_path}/${basename}.rttm #copy all.rttm into the output_path and rename it
  rm -r output_voice_type_classifier/${basename} #clean up other results for this audio
  echo "${basename} finished, $((c + 1))/${#files[@]} files"
done
```

Only one file for all audio
{: .label .label-blue }
This script will run VTC on the directory given in audio_path, this will output a single all.rttm with segments for all the recordings, it is then copied in the ourput_path given. 
```bash
#!/bin/bash
#SBATCH --job-name=vtc-mydata         # Job name
#SBATCH --partition=gpu               # Take a node from the 'gpu' partition
#SBATCH --cpus-per-task=2             # 2 CPU cores is fine as we use a GPU 
#SBATCH --gres=gpu:1                  # Ask for 1 gpu, usually a good idea for VTC
#SBATCH --time=48:00:00               # Time limit hrs:min:sec, default is 2h, which can be short for long form recordings 
#SBATCH --output=%x-%j.log            # Standard output and error log

echo "Running job on $(hostname)"

# load conda environment
source /shared/apps/anaconda3/etc/profile.d/conda.sh
conda activate /scratch2/username/modules/voice-type-classifier/conda-vtc-env #!!!! EDIT THIS !!!!

# set the paths
dataset_path="/scratch2/username/datasets/mydata" #!!!! EDIT THIS !!!!
profile="raw" #!!!! EDIT THIS IF YOUR AUDIOS WERE CONVERTED !!!!

dataset_path=${dataset_path%/}
audio_path=${dataset_path}/recordings/${profile%/}
output_path=${dataset_path}/annotations/vtc/raw
mkdir -p ${output_path} #create output dir if does not exist

# launch your computation
dirname=$(basename ${audio_path})
./apply.sh ${audio_path}/ --device=gpu
mv output_voice_type_classifier/${dirname}/all.rttm ${output_path}/all.rttm #copy all.rttm into the output_path
```
You can then submit your job to slurm.
```bash
sbatch job-vtc.sh
```
remarks:
- these templates use the dataset_path to find and place elements, if you have specific needs regardings paths, modify the script accordingly.
- We assume here that you only want to keep the all.rttm file (which contains the results for all speaker types) and not the speaker specific files. The script just deletes these other files, change the script if you want to keep them.

And that is it, check the log file of the job to check its progression. When it is over, find in your output_path your alice annotations. You are now ready to procede to [importation](#importing-the-new-annotations-to-the-dataset).

### Automatic LInguistic Unit Count Estimator (ALICE)

#### Installation

You should only install the repo and conda environment the first time. If you ran the model in the past, just reuse the same folder and conda environment.

The code for ALICE can be found in [this github repo](https://github.com/LoannPeurey/ALICE){:target="_blank"}. So the first step is to clone the repository in oberon, in a `scratch2/username` subdirectory.
```bash
cd /scratch2/username/modules
git clone --recurse-submodules https://github.com/LoannPeurey/ALICE.git #should take a dozens of seconds
cd ALICE
```
You now need to create the conda environment that will allow you to run the model and activate it. One easy way to keep everything together is to create that environment in the same directory and name it accordingly, so this is what we will do.
```bash
conda env create -p ./conda-alice-env -f ALICE_Linux.yml
```
The creation should last a few minutes. It happens more often than not that oberon is slowed down by other users, in that case this could take up to an hour.

You don't even need to activate the environment, the job used will take care of that itself.

#### Running it

We can't run the model directly on oberon as we need more ressources, so we will launch a [slurm job on oberon](https://wiki.cognitive-ml.fr/cluster/launching_jobs.html){:target="_blank"}.
You can use on of these script templates as a good starting point that you can then customize to your needs. Save the file in your ALICE folder as `job-alice.sh` for example and modify it for how you want to run alice.
Alice needs VTC annotations to run, the first script allows you to run ALICE and VTC at the same time, the second one skips VTC by using previously generated VTC annotations.

**To edit in the script:**
{: .label .label-green }
- conda environment path : change the `conda activate` line with the path of your brand new environment
- dataset_path : give the path to the root of your dataset
- profile : if had to convert your audios, put `converted/standard` or the name of the profile to use, otherwise keep the default `raw`

run VTC with alice
{: .label .label-blue }
This script will list all .wav files in the audio_path given, runs ALICE in its entirety by running VTC first. Each wav file will have their own vtc and alice outputs files, they will be named like the audio file they came from but as a rttm (for VTC) and txt (for ALICE) files instead of a wav one.
```bash
#!/bin/bash
#SBATCH --job-name=alice-mydata       # Job name
#SBATCH --partition=gpu               # Take a node from the 'gpu' partition
#SBATCH --cpus-per-task=2             # 2 CPU cores is fine as we use a GPU 
#SBATCH --gres=gpu:1                  # Ask for 1 gpu, usually a good idea for ALICE
#SBATCH --time=48:00:00               # Time limit hrs:min:sec, default is 2h, which can be short for long form recordings 
#SBATCH --output=%x-%j.log            # Standard output and error log

echo "Running job on $(hostname)"

# load conda environment
source /shared/apps/anaconda3/etc/profile.d/conda.sh
conda activate /scratch2/username/modules/ALICE/conda-alice-env #!!!! EDIT THIS !!!!

# set the paths
dataset_path="/scratch2/username/datasets/mydata" #!!!! EDIT THIS !!!!
profile="raw" #!!!! EDIT THIS IF YOUR AUDIOS WERE CONVERTED !!!!

dataset_path=${dataset_path%/}
audio_path=${dataset_path}/recordings/${profile%/}
alice_out_path=${dataset_path}/annotations/alice/output/raw
vtc_out_path=${dataset_path}/annotations/vtc/raw
aliceSum_out_path=${dataset_path}/annotations/alice/output/extra

mkdir -p ${alice_out_path} #create alice output path if does not exist
mkdir -p ${vtc_out_path} #create vtc output path if does not exist
mkdir -p ${aliceSum_out_path} #create alice sum output path if does not exist

# launch your computation
files=($(ls ${audio_path}/*.wav)) #list wav files in the audio_path
for c in "${!files[@]}"
do
  basename=$(basename ${files[$c]%.*})
  ./run_ALICE.sh ${files[$c]} --gpu
  mv ALICE_output.txt ${aliceSum_out_path}/${basename}_sum.txt
  mv ALICE_output_utterances.txt ${alice_out_path}/${basename}.txt
  mv diarization_output.rttm ${vtc_out_path}/${basename}.rttm
  echo "${basename} finished, $((c + 1))/${#files[@]} files"
done
```

Running when vtc annotations already exist
{: .label .label-blue }
This script will run ALICE separetly on all the wav files in the directory given in audio_path, it will try to find a rttm file with the same name in vtc_path to use as its VTC reference (and not having to waste time running VTC when it has already been done). It will then output a txt file with all the alice utterances and a summary of the results.

```bash
#!/bin/bash
#SBATCH --job-name=alice-mydata       # Job name
#SBATCH --partition=gpu               # Take a node from the 'gpu' partition
#SBATCH --cpus-per-task=2             # 2 CPU cores is fine as we use a GPU 
#SBATCH --gres=gpu:1                  # Ask for 1 gpu, usually a good idea for ALICE
#SBATCH --time=48:00:00               # Time limit hrs:min:sec, default is 2h, which can be short for long form recordings 
#SBATCH --output=%x-%j.log            # Standard output and error log

echo "Running job on $(hostname)"

# load conda environment
source /shared/apps/anaconda3/etc/profile.d/conda.sh
conda activate /scratch2/username/modules/ALICE/conda-alice-env #!!!! EDIT THIS !!!!

# set the paths
dataset_path="/scratch2/username/datasets/mydata" #!!!! EDIT THIS !!!!
profile="raw" #!!!! EDIT THIS IF YOUR AUDIOS WERE CONVERTED !!!!

dataset_path=${dataset_path%/}
audio_path=${dataset_path}/recordings/${profile%/}
alice_out_path=${dataset_path}/annotations/alice/output/raw
vtc_path=${dataset_path}/annotations/vtc/raw
aliceSum_out_path=${dataset_path}/annotations/alice/output/extra

mkdir -p ${alice_out_path} #create alice output path if does not exist
mkdir -p ${aliceSum_out_path} #create alice sum output path if does not exist

# launch computation
files=($(ls ${audio_path}/*.wav)) #list wav files in the audio_path
for c in "${!files[@]}"
do
  basename=$(basename ${files[$c]%.*})
  ./run_ALICE.sh ${files[$c]} --gpu --no-vtc ${vtc_path}/${basename}.rttm
  mv ALICE_output.txt ${aliceSum_out_path}/${basename}_sum.txt
  mv ALICE_output_utterances.txt ${alice_out_path}/${basename}.txt
  rm diarization_output.rttm
  echo "${basename} finished, $((c + 1))/${#files[@]} files"
done
```

On a VTC rttm file linked to multiple audios
{: .label .label-blue }
If you outputed a single rttm file with multiple audios with VTC, you must run ALICE on the same group of files together. Otherwise, ALICE will not understand why some audio files that are present in the rttm file are not available to him and it will cause it to fail. See the following example.

```bash
#!/bin/bash
#SBATCH --job-name=alice-mydata       # Job name
#SBATCH --partition=gpu               # Take a node from the 'gpu' partition
#SBATCH --cpus-per-task=2             # 2 CPU cores is fine as we use a GPU 
#SBATCH --gres=gpu:1                  # Ask for 1 gpu, usually a good idea for ALICE
#SBATCH --time=48:00:00               # Time limit hrs:min:sec, default is 2h, which can be short for long form recordings 
#SBATCH --output=%x-%j.log            # Standard output and error log

echo "Running job on $(hostname)"

# load conda environment
source /shared/apps/anaconda3/etc/profile.d/conda.sh
conda activate /scratch2/username/modules/ALICE/conda-alice-env #!!!! EDIT THIS !!!!

# set the paths
dataset_path="/scratch2/username/datasets/mydata" #!!!! EDIT THIS !!!!
profile="raw" #!!!! EDIT THIS IF YOUR AUDIOS WERE CONVERTED !!!!

dataset_path=${dataset_path%/}
audio_path=${dataset_path}/recordings/${profile%/}
alice_out_path=${dataset_path}/annotations/alice/output/raw
vtc_path=${dataset_path}/annotations/vtc/raw
aliceSum_out_path=${dataset_path}/annotations/alice/output/extra

mkdir -p ${alice_out_path} #create alice output path if does not exist
mkdir -p ${aliceSum_out_path} #create alice sum output path if does not exist

# launch computation
./run_ALICE.sh ${audio_path}/ --gpu --no-vtc ${vtc_path}/
mv ALICE_output.txt ${aliceSum_out_path}/sum_ALICE.txt
mv ALICE_output_utterances.txt ${alice_out_path}/all.txt
rm diarization_output.rttm
```
remarks:
- these templates use the dataset_path to find and place elements, if you have specific needs regardings paths, for example you want to place those annotations in a different set, modify the script accordingly.

You can then submit your job to slurm.
```bash
sbatch job-alice.sh
```

And that is it, check the log file of the job to check its progression and possible errors (see the troubleshooting section right below). The log file is named `alice-XX.log` where XX is the id of the job and it should be created in the folder where you launched it.
Check the status of the job with `squeue`. When it finishes, find in your output_path your alice annotations. You are now ready to procede to [importation](#importing-the-new-annotations-to-the-dataset).


#### Troubleshooting

- `ImportError: /lib64/libstdc++.so.6: version 'GLIBCXX_3.4.21' not found`. If you run into this error, you will need to update your libgcc version and explicitly add it to the library path of the conda environment.
To do so, first activate your conda environment and install the libgcc fron conda mirror:
```bash
conda activate ./conda-alice-env
conda install libgcc
```
Once the installation is complete, we will edit our job script to explicitly use the new libgcc path as a library path. Change the environment activation section by adding in the script the line `export LD_LIBRARY_PATH=/scratch2/username/modules/ALICE/conda-alice-env/lib:$LD_LIBRARY_PATH` right after the activation of the environment.
The activation section should look something like this:
```bash
# load conda environment
source /shared/apps/anaconda3/etc/profile.d/conda.sh
conda activate /scratch2/username/modules/ALICE/conda-alice-env #put your conda env path
export LD_LIBRARY_PATH=/scratch2/username/modules/ALICE/conda-alice-env/lib:$LD_LIBRARY_PATH # replace the path with your true conda environment path
``` 

-----

### VoCalisation Maturity (VCM)

#### Installation

You should only install the repo and conda environment the first time. If you ran the model in the past, just reuse the same folder and conda environment.

The code for VCM is stored in [this github repo](https://github.com/LAAC-LSCP/vcm/){:target="_blank"}. So the first step is to clone the repository in oberon, in a `scratch2/username` subdirectory.
```bash
cd /scratch2/username/modules
git clone https://github.com/LAAC-LSCP/vcm.git
cd vcm
```

On oberon, you need to create the conda environment that will allow you to run the model. One easy way to keep everything together is to create that environment in the same directory and name it accordingly, so this is what we will do here.
We first create an empty environment with only `pip` available, then we install the dependencies needed with `pip`.
```bash
conda create -p ./conda-vcm-env pip python=3.9
conda activate ./conda-vcm-env
pip install -r requirements.txt # installing the dependencies can take a few minutes
```

You will need the SMILExtract binary file to run vcm, download it for example in you current vcm directory and make it executable:
```bash
wget https://github.com/georgepar/opensmile/blob/master/bin/linux_x64_standalone_static/SMILExtract?raw=true -O SMILExtract
chmod u+x SMILExtract
```

#### Running it

Like the other models, we can't run it directly on oberon as we need more ressources, so we will launch a [slurm job on oberon](https://wiki.cognitive-ml.fr/cluster/launching_jobs.html){:target="_blank"}.
You can use on of these script templates as a good starting point that you can then customize to your needs. Save the file in your VCM folder as `job-vcm.sh` for example and modify it for how you want to run vcm.
VCM needs VTC annotations to run, make sure that you have those annotations ready and that the name of the audio file each line points to is the correct one (if you renamed your audios, it will not be able to find back which audio was used).

**To edit in the script:**
{: .label .label-green }
- conda environment path : change the `conda activate` line with the path of your brand new environment
- dataset_path : give the path to the root of your dataset
- profile : if had to convert your audios, put `converted/standard` or the name of the profile to use, otherwise keep the default `raw`

```bash
#!/bin/bash
#SBATCH --job-name=VCM         		  # Job name
#SBATCH --partition=all               # Take a node from the 'all' partition
#SBATCH --cpus-per-task=12            # here we pick only cpus, choose between taking 1 GPU and few CPUs or a bunch of CPUs with no GPU
#SBATCH --mem=2048                    # Memory request; MB assumed if unit not specified
#SBATCH --time=48:00:00               # Time limit hrs:min:sec default of 2h can be short on some occasions
#SBATCH --output=%x-%j.log            # Standard output and error log

echo "Running job on $(hostname)"

# load conda environment
source /shared/apps/anaconda3/etc/profile.d/conda.sh
conda activate /scratch2/username/modules/vcm/conda-vcm-env # !!!! EDIT THIS !!!!

# set the paths
dataset_path="/scratch2/username/datasets/mydata" #!!!! EDIT THIS !!!!
profile="raw" #!!!! EDIT THIS IF YOUR AUDIOS WERE CONVERTED !!!!

dataset_path=${dataset_path%/}
audio_path=${dataset_path}/recordings/${profile%/}
rttm_path=${dataset_path}/annotations/vtc/raw
out_path=${dataset_path}/annotations/vcm/raw
smilextract="."

mkdir -p ${alice_out_path} #create alice output path if does not exist
mkdir -p ${aliceSum_out_path} #create alice sum output path if does not exist

# launch your computation
./vcm.sh -a ${audio_path} -r ${rttm_path} -s ${smilextract} -o ${out_path} -j 12 #12 jobs, put your number of cpu cores
```
You can then submit your job to slurm.
```bash
sbatch job-vcm.sh
```

remarks:
	- We assume the SMILExtract binary file is in the vcm directory, you can modify that path in the script if necessary.


#### Troubleshooting

We have encountered problems where VCM jobs would hang and not make progress. We believe running VCM only CPUs in a node that has GPUs triggers that problem, probably because the models sees that the node has gpus available but can't access them because we did not ask for any. If you encounter that problem, either:
- require a GPU with : `#SBATCH --gres=gpu:1`
- require a specific node that does not have GPUs : `#SBATCH --nodelist=puck1`

-----

## Importing the new annotations to the dataset

Importing annotations to a dataset does the following:
- convert the given annotation files into the childproject standard format (csv) and nomenclature (ie using unified labels such as CHI / FEM / MAL / OCH etc).
- store information about each annotation file such as the recording it is linked to, the onset offset in the audio and so on ([see the documentation](https://childproject.readthedocs.io/en/latest/format.html#annotations-index){:target="_blank"}) in the annotation index.

This can be done with the command line or with the python API. Here we will use the API as it will be easier to just call one python script doing all the work.

Here are a couple of templates of python scripts building a dataframe for annotation importation and then running the importation.

**To edit in the script:**
{: .label .label-green }
- annot_type : depending on the type of annotation that you import, uncomment the correct line. We use the default sets and file extension for those types.

1 file per audio
{: .label .label-blue }
Importing when each annotation file is linked to a single audio and is named after it.
```python
#!/usr/bin/env python3
import pandas as pd
import os
from ChildProject.projects import ChildProject
from ChildProject.annotations import AnnotationManager

dataset_path = "."
### !!!! EDIT THIS SECTION !!!! ###
#annot_type = {"set":"vtc","file_extension":".rttm","format":"vtc_rttm"} # UNCOMMENT FOR VTC ANNOTATIONS
#annot_type = {"set":"alice/output","file_extension":".txt","format":"alice"} # UNCOMMENT FOR ALICE ANNOTATIONS
#annot_type = {"set":"vcm","file_extension":".vcm","format":"vcm_rttm"} # UNCOMMENT FOR VCM ANNOTATIONS
###################################

#load the project
project = ChildProject(dataset_path)
# load the annotation manager for our project
am = AnnotationManager(project)

# we take a copy of the recordings.csv file of the dataset, that suits us because we have one importation per recording, as is usually the case with automated annotations
input_frame = pd.DataFrame.copy(project.recordings)

# let's drop every column that we don't need
input_frame.drop(['experiment', 'child_id', 'date_iso', 'start_time', 'recording_device_type'], axis = 1, inplace = True)

#make sure that the duration for the recordings is set in recordings.csv, otherwise run child-project compute-durations /path

input_frame["raw_filename"]= input_frame.apply(lambda row: os.path.splitext(row["recording_filename"])[0] + annot_type["file_extension"], axis=1) #take the name of the audio and add extension of the annotation (so this assumes the annotation file has the same name as the audio appart from extension)
input_frame["set"] = annot_type["set"] #set to import to
input_frame["format"] = annot_type["format"] #format of the annotation
input_frame["time_seek"] = "0" # timestamps in the file don't need to be shifted
input_frame["range_onset"] = "0" #from the start of the audio              ...
input_frame["range_offset"]= input_frame["duration"] # ...to the end

am.import_annotations(input_frame)
```

1 file for all audio
{: .label .label-blue }
Importing when there is a single annotations file containing annotations for all the audio files. Note that you can not do this with VCM as it will always output one file per audio
```python
#!/usr/bin/env python3
import pandas as pd
import os
from ChildProject.projects import ChildProject
from ChildProject.annotations import AnnotationManager

dataset_path = "."
### !!!! EDIT THIS SECTION !!!! ###
#annot_type = {"set":"vtc","file":"all.rttm","format":"vtc_rttm"} # UNCOMMENT FOR VTC ANNOTATIONS
#annot_type = {"set":"alice/output","file":"all.txt","format":"alice"} # UNCOMMENT FOR ALICE ANNOTATIONS
###################################

#load the project
project = ChildProject(dataset_path)
# load the annotation manager for our project
am = AnnotationManager(project)

# we take a copy of the recordings.csv file of the dataset, that suits us because we have one importation per recording, as is usually the case with automated annotations
input_frame = pd.DataFrame.copy(project.recordings)

# let's drop every column that we don't need
input_frame.drop(['experiment', 'child_id', 'date_iso', 'start_time', 'recording_device_type'], axis = 1, inplace = True)

#make sure that the duration for the recordings is set in recordings.csv, otherwise run child-project compute-durations /path

input_frame["raw_filename"]= annot_type["file"] #name of the annotation file
input_frame["set"] = annot_type["set"] #set to import to
input_frame["format"] = annot_type["format"] #format of the annotation
input_frame["time_seek"] = "0" # timestamps in the file don't need to be shifted
input_frame["range_onset"] = "0" #from the start of the audio              ...
input_frame["range_offset"]= input_frame["duration"] # ...to the end
input_frame["filter"]= input_frame.apply(lambda row: os.path.splitext(row["recording_filename"])[0], axis=1) # take only the lines referring to the file we are importing for

am.import_annotations(input_frame)
```

Here are some elements to keep in mind:
- In this example, we are using automated annotations that cover the entire audio files, allowing us not to worry too much about the onset and offset parameters as they are just respectively 0 and the duration of the audio in millisecond.

Store your script in your dataset in a script folder (`mkdir scripts` from the root af dataset), give it an informative name (eg import_vtc.py) and edit it for your usage.
Make sure your childproject environment is activated and run it:
```bash
python scripts/import_vtc.py
```
This should not take more than a minute to complete.

If everything went smoothly, you can procede to publishing your changes

## Publishing changes to the GIN repository

Our annotations are now correctly structured and imported into the dataset, our next step is to push them upstream to the repository. We assume here the data was cloned from the same repository we want to push to and the remote url can handle both annexed and unannexed files (ie most likely GIN).
Go to the root of your dataset and check that your childproject environment is activated.
Check your remote url with `git config --get remote.origin.url`, this is the url where your data will be pushed (If the url is not the one you expected, you can see siblings with `datalad siblings`).

You should have a look at all the changes you made with `datalad status`. This will list the new files and the modified one, check that everything makes sense and you did not modify what you were not supposed to.

If everything looks good, you can save the state of your dataset:
```bash
datalad save -m "create VTC annotations, imported them with scripts/import_vtc.py"
```
Be informative with the message you write. This command will encrypt the annotation files so it can take several minutes

You can now push your changes to the online repo:
```bash
datalad push
#or
datalad push --to GIN #if you push to a specific sibling (replace GIN with the name of the silbing)
```

Hourra !! You successfully went through the all process of creating and adding automated annotations to your dataset. You can have a coffee break.