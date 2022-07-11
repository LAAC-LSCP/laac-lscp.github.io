"""
This script splits the audio files outputted by lena that contains multiple days of recording.
Based on recordings.csv, splits audio that is linked to the same .its file into separate audio files by using the durations.
"""
from ChildProject.projects import ChildProject 
from pydub import AudioSegment
import os

audio_path = 'recordings/lena_output'

project = ChildProject('.')
project.read()

#regroup recordings by the original lena output(as the its file)
for its, recordings in project.recordings.groupby('its_filename'):
    #print(recordings)
    #print(session)
    
    recordings['position'] = recordings['duration'].cumsum().shift(1, fill_value = 0)
    
    input_audio = os.path.join(audio_path, its[:-4] +'.wav')
    if not os.path.exists(input_audio):
        #print(f"{input_audio} does not exist")
        pass

    audio = None

    for recording in recordings.to_dict(orient = 'records'):
        on = recording['position']
        off = recording['position']+recording['duration']

        print("audio : {} -> {} - {} -> {}".format(input_audio, on, off,recording['recording_filename']))
    
        if audio is None:
            audio = AudioSegment.from_file(input_audio)
        
        try:
            audio[on:off].set_sample_width(2).export(
                project.get_recording_path(recording['recording_filename']),
                format = 'wav',
                bitrate = '16k'
            )
        except Exception as e:
           print("failed to extract {}: {}", recording['recording_filename'], str(e))