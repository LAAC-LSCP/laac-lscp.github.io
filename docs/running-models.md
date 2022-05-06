---
layout: default
title: running models
nav_order: 9
description: "Running model analysis on your data"
---

# Run models to obtain automated annotations for your project
{: .no_toc }

This guides assume you are using the childproject data structure and that you store you project in the oberon server.
They are meant to guide you run the models in the cluster to obtain automated annotations, import those new annotations to the childproject dataset and then upload the changes made to the dataset to gin.

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Running the models

Everytime you add new annotations to a dataset, you need to arganize them correctly for childproject. First, they will need to be in the annotations folder from the root of the dataset, then you must choose a name for this set of annotations, the name of the set is there to specify that all the annotations inside are of the same format and were produced together or serve the same purpose.

### Voice type classifier (VTC)

If you want both VTC and ALICE annotations, go directly to the ALICE section as ALICE can run both models in one go.
{: .label .label-yellow }

VTC is currently being reworked by the CoML team so a new version (and easier way to run the model) should soon replace this tutorial.
{: .label .label-red }

#### Installation

The code for VTC is stored in [this github repo](https://github.com/MarvinLvn/voice-type-classifier/){:target="_blank"}. So the first step is to clone the repository in oberon, in a `scratch2/username` subdirectory.
```bash
cd /scratch2/username/modules
git clone --recurse-submodules https://github.com/MarvinLvn/voice-type-classifier.git
cd voice-type-classifier
```
You now need to create the conda environment that will allow you to run the model and activate it. One easy way to keep everything together is to create that environment in the same directory and name it accordingly, so this is what we will do.
```bash
conda create -p ./conda-vtc-env -f vtc.yml
```

#### Running it

We can't run the model directly on oberon as we need more ressources, so we will launch a [slurm job on oberon](https://wiki.cognitive-ml.fr/cluster/launching_jobs.html){:target="_blank"}.
You can use on of these script templates as a good starting point that you can then customize to your needs. Save the file in your vtc folder as `job-vtc.sh` for example and modify it for how you want to run vtc.

Some remarks:
- Using one GPU is a good idea for running VTC.
- When using a GPU, only ask for a few cpus (usually 2).
- don't forget to put a time limit as the default one is 2 hours and this can be too short for long recordings.
- these templates use an audio_path for where to find audio files, output_path for where to store the results and a path to the conda environment to activate, change them accordingly in the script.
- We assume here that you only want to keep the all.rttm file (which contains the results for all speaker types) and not the speaker specific files. The script just deletes these other files, change the script if you want to keep them.

One output file per audio
{: .label .label-blue }
This script will list all .wav files in the audio_path given, run VTC on each of them and move the results into the output_path given, renaming them with the name of the audio file they came from but as a rttm files instead of a wav one. 
```bash
#!/bin/bash
#SBATCH --job-name=vtc-mydata         # Job name
#SBATCH --partition=gpu               # Take a node from the 'gpu' partition
#SBATCH --cpus-per-task=2             # Ask for 2 CPU cores
#SBATCH --gres=gpu:1                  # Ask for 1 gpu
#SBATCH --time=48:00:00               # Time limit hrs:min:sec
#SBATCH --output=%x-%j.log            # Standard output and error log

echo "Running job on $(hostname)"

# load conda environment
source /shared/apps/anaconda3/etc/profile.d/conda.sh
conda activate /scratch2/username/modules/voice-type-classifier/conda-vtc-env #put your conda env path

# launch your computation
audio_path="/scratch2/username/datasets/mydata/recordings/raw/"
output_path="/scratch2/username/datasets/mydata/annotations/vtc/raw/"
audio_path=${audio_path%/}
output_path=${output_path%/}
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
This script will run VTC on the directory given in audio_path, this will output a single all.rttm with segments for all the recordings, it is then copied in the ourput_path_given. 
```bash
#!/bin/bash
#SBATCH --job-name=vtc-mydata         # Job name
#SBATCH --partition=gpu               # Take a node from the 'gpu' partition
#SBATCH --cpus-per-task=2             # Ask for 2 CPU cores
#SBATCH --gres=gpu:1                  # Ask for 1 gpu
#SBATCH --time=48:00:00               # Time limit hrs:min:sec
#SBATCH --output=%x-%j.log            # Standard output and error log

echo "Running job on $(hostname)"

# load conda environment
source /shared/apps/anaconda3/etc/profile.d/conda.sh
conda activate /scratch2/username/modules/voice-type-classifier/conda-vtc-env #put your conda env path

# launch your computation
audio_path="/scratch2/username/datasets/mydata/recordings/raw/"
output_path="/scratch2/username/datasets/mydata/annotations/vtc/raw/"
audio_path=${audio_path%/}
output_path=${output_path%/}
mkdir -p ${output_path} #create output dir if does not exist

dirname=$(basename ${audio_path})
./apply.sh ${audio_path}/ --device=gpu
mv output_voice_type_classifier/${dirname}/all.rttm ${output_path}/all.rttm #copy all.rttm into the output_path
```
You can then submit your job to slurm.
```bash
sbatch job-vtc.sh
```

And that is it, check the log file of the job to check its progression. When it is over, find in your output_path your alice annotations. You are now ready to procede to [importation](#importing-the-new-annotations-to-the-dataset).

### Automatic LInguistic Unit Count Estimator (ALICE)

Work in progress
{: .label .label-red }

#### Installation

The code for ALICE can be found in [this github repo](https://github.com/LoannPeurey/ALICE){:target="_blank"}. So the first step is to clone the repository in oberon, in a `scratch2/username` subdirectory.
```bash
cd /scratch2/username/modules
git clone --recurse-submodules https://github.com/LoannPeurey/ALICE.git
cd ALICE
```
You now need to create the conda environment that will allow you to run the model and activate it. One easy way to keep everything together is to create that environment in the same directory and name it accordingly, so this is what we will do.
```bash
conda create -p ./conda-alice-env -f ALICE_Linux.yml
```

#### Running it

We can't run the model directly on oberon as we need more ressources, so we will launch a [slurm job on oberon](https://wiki.cognitive-ml.fr/cluster/launching_jobs.html){:target="_blank"}.
You can use on of these script templates as a good starting point that you can then customize to your needs. Save the file in your ALICE folder as `job-alice.sh` for example and modify it for how you want to run alice.
Alice needs VTC annotations to run, the first script allows you to run ALICE and VTC at the same time, the second one skips VTC by using previously generated VTC annotations.

Some remarks:
- Like for VTC, using one GPU is a good idea for running ALICE.
- When using a GPU, only ask for a few cpus (usually 2).
- don't forget to put a time limit as the default one is 2 hours and this can be too short for long recordings.
- these templates use :
    - audio_path for where to find audio files
    - alice_out_path for where to store the ALICE base results
    - aliceSum_out_path for where to move the summary of alice
    - vtc_out_path for where to store the VTC results that ALICE runs first (if you choose not to skip VTC)
    - vtc_path for where to find the VTC annotations (if you choose to skip VTC)
    - a path to the conda environment to activate
Change those paths accordingly in the script.

run VTC with alice
{: .label .label-blue }
This script will list all .wav files in the audio_path given, runs ALICE in its entirety by running VTC first. Each wav file will have their own vtc and alice outputs files, they will be named like the audio file they came from but as a rttm (for VTC) and txt (for ALICE) files instead of a wav one.
```bash
#!/bin/bash
#SBATCH --job-name=alice-mydata       # Job name
#SBATCH --partition=gpu               # Take a node from the 'gpu' partition
#SBATCH --cpus-per-task=2             # Ask for 2 CPU cores
#SBATCH --gres=gpu:1                  # Ask for 1 gpu
#SBATCH --time=48:00:00               # Time limit hrs:min:sec
#SBATCH --output=%x-%j.log            # Standard output and error log

echo "Running job on $(hostname)"

# load conda environment
source /shared/apps/anaconda3/etc/profile.d/conda.sh
conda activate /scratch2/username/modules/ALICE/conda-alice-env #put your conda env path

# launch your computation
audio_path="/scratch2/username/datasets/mydata/recordings/raw/"
alice_out_path="/scratch2/username/datasets/mydata/annotations/alice/output/raw/"
vtc_out_path="/scratch2/username/datasets/mydata/annotations/vtc/raw/"
aliceSum_out_path="/scratch2/username/datasets/mydata/annotations/alice/output/extra/"
audio_path=${audio_path%/}
alice_out_path=${alice_out_path%/}
vtc_out_path=${vtc_out_path%/}
aliceSum_out_path=${aliceSum_out_path%/}
mkdir -p ${alice_out_path} #create alice output path if does not exist
mkdir -p ${vtc_out_path} #create vtc output path if does not exist
mkdir -p ${aliceSum_out_path} #create alice sum output path if does not exist

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
#SBATCH --cpus-per-task=2             # Ask for 2 CPU cores
#SBATCH --gres=gpu:1                  # Ask for 1 gpu
#SBATCH --time=48:00:00               # Time limit hrs:min:sec
#SBATCH --output=%x-%j.log            # Standard output and error log

echo "Running job on $(hostname)"

# load conda environment
source /shared/apps/anaconda3/etc/profile.d/conda.sh
conda activate /scratch2/username/modules/ALICE/conda-alice-env #put your conda env path

# launch your computation
audio_path="/scratch2/username/datasets/mydata/recordings/raw/"
vtc_path="/scratch2/username/datasets/mydata/annotations/vtc/raw"
alice_out_path="/scratch2/username/datasets/mydata/annotations/alice/output/raw/"
aliceSum_out_path="/scratch2/username/datasets/mydata/annotations/alice/output/extra/"
audio_path=${audio_path%/} #clean up path name (remove /)
vtc_path=${vtc_path%/}
alice_out_path=${alice_out_path%/}
aliceSum_out_path=${aliceSum_out_path%/}
mkdir -p ${alice_out_path} #create alice output path if does not exist
mkdir -p ${aliceSum_out_path} #create alice sum output path if does not exist

files=($(ls ${audio_path}/*.wav)) #list wav files in the audio_path
for c in "${!files[@]}"
do
  basename=$(basename ${files[$c]%.*})
  ./run_ALICE.sh ${files[$c]} --gpu --no-vtc ${vtc_path}/${basename}.rttm
  mv ALICE_output.txt ${aliceSum_out_path}/${basename}_sum.txt
  mv ALICE_output_utterances.txt ${alice_out_path}/${basename}.txt
  mv diarization_output.rttm ${vtc_out_path}/${basename}.rttm
  echo "${basename} finished, $((c + 1))/${#files[@]} files"
done
```
You can then submit your job to slurm.
```bash
sbatch job-alice.sh
```


And that is it, check the log file of the job to check its progression. When it is over, find in your output_path your alice annotations. You are now ready to procede to [importation](#importing-the-new-annotations-to-the-dataset).

### VoCalisation Maturity (VCM)

Work in progress
{: .label .label-red }

#### Installation

The code for VCM is stored in [this github repo](https://github.com/LAAC-LSCP/vcm/){:target="_blank"}. So the first step is to clone the repository in oberon, in a `scratch2/username` subdirectory.
```bash
cd /scratch2/username/modules
git clone https://github.com/LAAC-LSCP/vcm.git
cd vcm
```

On oberon, you need to create the conda environment that will allow you to run the model. One easy way to keep everything together is to create that environment in the same directory and name it accordingly, so this is what we will do here.
We first create an empty environment with only `pip` available, then we install the dependencies needed with `pip`.
```bash
conda create -p ./conda-vcm-env pip
conda activate ./conda-vcm-env
pip install -r requirements
```

You will need the SMILExtract binary file to run vcm, download it for example in you current vcm directory:
```bash
wget https://github.com/georgepar/opensmile/blob/master/bin/linux_x64_standalone_static/SMILExtract?raw=true -O SMILExtract
chmod u+x SMILExtract
```

#### Running it

Like the other modeils, we can't run it directly on oberon as we need more ressources, so we will launch a [slurm job on oberon](https://wiki.cognitive-ml.fr/cluster/launching_jobs.html){:target="_blank"}.
You can use on of these script templates as a good starting point that you can then customize to your needs. Save the file in your VCM folder as `job-vcm.sh` for example and modify it for how you want to run vcm.
VCM needs VTC annotations to run, make sure that you have those annotations ready and that the name of the audio file each line points to is the correct one (if you renamed your audios, it will not be able to find back which audio was used).

Some remarks:
- Depending on the size of the data, you should choose between taking 1 GPU and few CPUs or a bunch of CPUs.
- don't forget to put a time limit as the default one is 2 hours and this can be too short for long recordings.
- this template uses :
    - audio_path for where to find audio files
    - 
Change those paths accordingly in the script.

## Importing the new annotations to the dataset

## Publishing changes to the GIN repository