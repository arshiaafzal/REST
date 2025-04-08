import numpy as np
import scipy
import mne
from scipy.signal import welch , resample
import mne
import numpy as np
import matplotlib.pyplot as plt
import data_utils as ps
import pyedflib
import glob
import os
from tqdm import tqdm
import csv
from torch.utils.data import Dataset, DataLoader
from random import randint
import random
import h5py
import torch



def build_data_directory_patient (train_set_directory , patient):
    
    patient_i_session_dir = train_set_directory + patient

    session_list =  [ f.name for f in os.scandir(patient_i_session_dir) if f.is_dir() ]

    D = []
    Directory = []

    for ses_id , ses in enumerate(session_list):


        montage =   [f.name for f in os.scandir(patient_i_session_dir+'/'+ses)  if f.is_dir()]


        data_dir = patient_i_session_dir+'/'+ses+'/'+montage[0]

        extension = 'edf'
        os.chdir(data_dir)
        result = glob.glob('*.{}'.format(extension))


        D.append([(data_dir+ '/' + r).replace('.edf', '') for r in result])
        
        for d in D:
            for dd in d:
                Directory.append(dd)

    return  np.unique(Directory)  


def build_data_dic (train_set_directory):
    
    Dir = []
    patients_list =  [ f.name for f in os.scandir(train_set_directory) if f.is_dir() ]
#     patients_list.remove('.ipynb_checkpoints')

    for p in tqdm(patients_list):

        dic = build_data_directory_patient('/home/afzal/datasets/tuh_eeg_datases/edf/eval/' , p)
        
        [Dir.append(d)  for d in dic]
    
    
    return np.array(Dir)


def raw_eeg_loader(dir_):

    extension = '.edf'
    data = mne.io.read_raw_edf(dir_+extension , verbose=False)
    
    return data

def resample_data(signals, to_freq, fs):

    N = signals.shape[1]
    window_size = N/fs
    num = int(to_freq * window_size)
    resampled = resample(signals, num=num, axis=1)

    return resampled

def get_seiz_times(path):
    
    seizure_times = []
    with open(path + '.csv_bi') as f:
        for line in f.readlines():
            
            if "seiz" in line:  # if seizure
                # seizure start and end time
                seizure_times.append(
                    [
                        float(line.split(",")[1]),
                        float(line.split(",")[2]),
                    ]
                )
                
    return seizure_times

def parsetxtfile(seizure_file , bckg_file , seed ):
    
    random.seed(seed)
    
    seizure_contents = open(seizure_file, "r") 
    non_seizure_contents = open(bckg_file, "r") 

    seiz_list = []
    non_seiz_list = []
    bckg_list = []
    dir_ = []

    dir_.extend(seizure_contents.readlines())

    for idx in range(len(dir_)):

        tuple_seiz = [eval(dir_[idx].split(',')[0].split('[')[1]) , 
        int( dir_[idx].split(',')[1] )  , int( dir_[idx].split(',')[-1] .split(']\n')[0] )]
        seiz_list.append(tuple_seiz)

    dir_ = []
    dir_.extend(non_seizure_contents.readlines())

    for idx in range(len(dir_)):

        tuple_bckg = [eval(dir_[idx].split(',')[0].split('[')[1]) , 
        int( dir_[idx].split(',')[1] )  , int( dir_[idx].split(',')[-1] .split(']\n')[0] )]
        bckg_list.append(tuple_bckg)



    combined_list = bckg_list + seiz_list

    random.shuffle(combined_list)
    
    return combined_list 


def Seiz_tuple_gen(set_directory , T):
    
    Dic = build_data_dic(set_directory)

    seiz_tuple = []

    for item in tqdm(Dic):

        seiz_time = get_seiz_times(item)

        if len(seiz_time) != 0:

            for times in seiz_time:

                start_time = times[0]
                end_time = times[1]

                clip_idx =  np.arange(np.floor(start_time/T),np.ceil(end_time/T) , dtype=int )  
                if len(clip_idx) > 0 :
                    [seiz_tuple.append([item,c,1]) for c in clip_idx]  
                    
    return seiz_tuple


def Bckg_tuple_gen(set_directory , T):
    
    Dic = build_data_dic(set_directory)

    bckg_tuple = []
    for item in tqdm(Dic):

        seiz_time = get_seiz_times(item)

        if len(seiz_time) == 0:

            data_len = np.floor( raw_eeg_loader(item).times[-1]/T-2) 

            if data_len > 0:

                clip_idx =  np.arange(0,data_len, dtype=int)
                [bckg_tuple.append([item,c,0]) for c in clip_idx]
                
    return bckg_tuple

def make_tuple_files(dir_ , set_directory , T , train_bool):
    
    seiz_tuple = Seiz_tuple_gen(set_directory , T )
    bckg_tuple = Bckg_tuple_gen(set_directory , T )
    
    if train_bool:
        random.seed(123)
        bckg_tuple = random.sample(bckg_tuple,  len(seiz_tuple) )
    
    with open(dir_ + "/seiz_tuple.txt", "w") as f:
        for s in seiz_tuple:
            f.write(str(s) +"\n")
        
    with open(dir_ + "/bckg_tuple.txt", "w") as f:
        for s in bckg_tuple:
            f.write(str(s) +"\n")
    


def save_eeg_clip(seizure_file , bckg_file , time_step ,T , to_freq ,h5_file , h5_file_label ,  seed):
    

    INCLUDED_CHANNELS = [
    'EEG FP1',
    'EEG FP2',
    'EEG F3',
    'EEG F4',
    'EEG C3',
    'EEG C4',
    'EEG P3',
    'EEG P4',
    'EEG O1',
    'EEG O2',
    'EEG F7',
    'EEG F8',
    'EEG T3',
    'EEG T4',
    'EEG T5',
    'EEG T6',
    'EEG FZ',
    'EEG CZ',
    'EEG PZ']


    combined_list = parsetxtfile(seizure_file , bckg_file , seed)
    dirs = [elemnt[0].split('/')[-1] for elemnt in combined_list]


    for elemnt in tqdm( np.unique (dirs)):

        matches =  [ i for i,x in enumerate(dirs) if x == elemnt ]

        C = [combined_list[clpind] for clpind in matches]

        eeg_dir = C[0][0]

        Raw_file = raw_eeg_loader(eeg_dir)

        mon_id = Raw_file.ch_names[0].split('-')[1]

        fs = 1/(Raw_file.times[1] - Raw_file.times[0])  
        eeg_ch = [ch +'-'+ mon_id  for ch in INCLUDED_CHANNELS ]     
        eeg_signal = Raw_file.pick_channels(eeg_ch).get_data()

        resampled_eeg = resample_data(eeg_signal , fs = fs , to_freq = to_freq)

        for label , clip_idx in  zip((np.array(C)[:,2]).astype(int) , (np.array(C)[:,1]).astype(int)):

   

            start_window = int(clip_idx * to_freq* T)

            eeg_slc = [resampled_eeg[:,start_window + t*to_freq:start_window + (t+1)*to_freq]  for t in range(T)]

            a = [e.shape[1] for e in eeg_slc]

            if np.sum(a)/to_freq != T:
                continue

            eeg_clip = np.stack( eeg_slc ,0)

            if eeg_clip.shape != (T,19,to_freq):
                continue


            with h5py.File(h5_file + eeg_dir.split('/')[-1] + '_' + str(clip_idx) +'.h5' , "w") as hf: 
                hf.create_dataset(eeg_dir.split('/')[-1] + '_' + str(clip_idx) +'.h5' , data = eeg_clip  )


            with h5py.File(h5_file_label +eeg_dir.split('/')[-1] + '_' + str(clip_idx) +'.h5', "w") as hf_label: 
                hf_label.create_dataset(eeg_dir.split('/')[-1]+ '_' + str(clip_idx) +'.h5' , data = label  )


def create_dataset_list(h5_file_dir , label_dir):               
    EEG = []
    Label = []

    for idx in tqdm(range(len(os.listdir(h5_file_dir)))):

        clip_list = os.listdir(h5_file_dir)

        with h5py.File( h5_file_dir + clip_list[idx], "r") as f:

            eeg_clip = np.array(f[list(f.keys())[0]])

            label_list = os.listdir(label_dir)
            index = np.argwhere( np.array(label_list) == clip_list[idx])   

            EEG.append(eeg_clip)

        with h5py.File(label_dir +label_list[int(index)], "r") as f:

            label = np.array(f[list(f.keys())[0]])

            Label.append(label)
            
    return EEG, Label






