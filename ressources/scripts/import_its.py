"""
This script uses metadata/recordings.csv to import its annotations. It assumes recordings.csv contains columns 'its_filename' and 'duration' to run the importation
"""
import pandas as pd
from ChildProject.projects import ChildProject
from ChildProject.annotations import AnnotationManager

dataset_path = "."

#load the project and annotation manager
project = ChildProject(dataset_path)
am = AnnotationManager(project)

# we take a copy of the recordings.csv file of the dataset, that suits us because we have one importation per recording, as is usually the case with automated annotations
input_frame = pd.DataFrame.copy(project.recordings)
input_frame = input_frame.sort_values(['its_filename', 'recording_filename'])

#make sure that the duration for the recordings is set in recordings.csv, it should be imported with the metadata of the its
input_frame["raw_filename"]= input_frame['its_filename']
input_frame["set"] = 'its'
input_frame["range_onset"] = "0" #from the start of the audio...
input_frame["range_offset"]= input_frame["duration"] # ...to the end

for its, df in input_frame.groupby('its_filename'):
    input_frame.loc[df.index,'time_seek'] = - df['duration'].cumsum().shift(1, fill_value = 0)

am.import_annotations(input_frame)


