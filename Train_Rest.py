import torch
import numpy as np
from tqdm import tqdm
from scipy.fft import fft
from sklearn import metrics

from torch_geometric.data import Dataset
from torch_geometric.loader import DataLoader


import torch.nn.functional as F
import scipy.io as sio

from torch_geometric.nn import global_mean_pool
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader



import lightning as L


from REST import LitREST


def make_adj_matrix(adj_path):
    # the adjacancy matrix is also located in the repository and it is brough from: https://github.com/tsy935/eeg-gnn-ssl/tree/main
    adj = sio.loadmat(adj_path+'/adj_mat')['adj_mat']
    ind = (adj != 0) & (adj != 1)
    edge_index = np.argwhere(ind == True).T 

    edge_weight = np.zeros((1,edge_index.shape[1]))

    for i , e in enumerate(edge_index.T):  
        
        edge_weight[0,i] = adj [e[0] , e[1]]
            

    edge_index =torch.tensor(edge_index )
    edge_weight = torch.tensor(edge_weight)
    
    return edge_weight , edge_index


def train_rest(edge_weight , edge_index , ratio_train = 0.75 , is_fft = True , epoch=100, devices = [1,2,3] , batch_size=1024):
    
    # This needs the clip_data and labels to be in correct path
    
    with h5py.File( 'clip_data' +'.h5' , "r") as f:
        EEG = np.array(f[list(f.keys())[0]])

    with h5py.File(  'label' +'.h5', "r") as f: 
        Label = np.array(f[list(f.keys())[0]])
        
    dataset = []
    batch = np.ones((1,19))
    
    
    for idx in tqdm(range(EEG.shape[0])):
        
        eeg_clip = EEG[idx,:,:,:]
        
        if is_fft:
            eeg_clip = np.log(np.abs( fft(eeg_clip,axis=2)[:,:,0:100]) +1e-30) # Just real part might also be useful
            
        label = Label[idx]
        
        dataset.append(Data(x = torch.tensor(eeg_clip).transpose(1,0) , 
                        y = torch.tensor((label)  , dtype=torch.long) , batch = batch  , 
                        edge_weight = edge_weight , edge_index = edge_index , elec_pos = torch.tensor(pos) )  
    )
    
    
    print('Shape of the training Label is: ' , Label.shape)
    
    train_idx = [0 , int(ratio_train*len(dataset))]
    test_idx = [int(ratio_train*len(dataset)) , len(dataset)]

    train_dataloader = DataLoader(dataset[train_idx[0]:train_idx[1]] , batch_size = batch_size  )
    
    model = LitREST(fire_rate = 0.5 , conv_type = 'gconv' )
    
    torch.manual_seed(123)  # Seed which can be removed or added in another part

    torch.set_float32_matmul_precision('high')
    trainer = L.Trainer(max_epochs=epoch  ,devices = devices ,  accelerator="gpu" , precision="bf16-mixed" , 
                        strategy = "ddp_notebook_find_unused_parameters_false"   )

    trainer.fit(model, train_dataloader  )
    
    return model


def eval_REST(model , batch_size ,edge_weight , edge_index , is_fft=True):
    
    
    with h5py.File( 'clip_data_eval' +'.h5' , "r") as f:
    
        EEG = np.array(f[list(f.keys())[0]])

        
    with h5py.File(  'label_eval' +'.h5', "r") as f: 

        Label = np.array(f[list(f.keys())[0]])
    
    dataset = []
    batch = np.ones((1,19))

    for idx in tqdm(range(EEG.shape[0])):
        
        eeg_clip = EEG[idx,:,:,:]
        
        if is_fft:
            eeg_clip = np.log(np.abs( fft(eeg_clip,axis=2)[:,:,0:100]) +1e-30) # Just real part might also be useful
            
        label = Label[idx]
        
        dataset.append(Data(x = torch.tensor(eeg_clip).transpose(1,0) , 
                        y = torch.tensor((label)  , dtype=torch.long) , batch = batch  , 
                        edge_weight = edge_weight , edge_index = edge_index  )  
    )
        
        
    del Label , EEG  # Added new
    
    test_dataloader = DataLoader(dataset , batch_size  )
    
    l = []
    gt = []

    for batch_num, data in enumerate(tqdm(test_dataloader)):
        
        out = model.to('cuda')(data.to('cuda'))
        out = global_mean_pool (out , data.batch)
        
        l.extend ( (  (torch.sigmoid(out.reshape(-1,1)) )).to('cpu').detach().numpy()  )  

        gt.extend( ( data.y.type(torch.float32).reshape(-1,1).to('cpu') ).detach().numpy() )
        
        

        fpr, tpr, thresholds = metrics.roc_curve(np.ravel( np.array(gt).reshape(-1,1)) , 
                                                np.ravel( np.array(l).reshape(-1,1)   ) )
        metrics.auc(fpr,tpr)
                
        

