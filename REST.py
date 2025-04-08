import torch
import torch.nn.functional as F
from torch.nn import Linear
import torch.optim as optim

from torch_geometric.nn import GraphConv
from torch_geometric.nn import global_mean_pool
from torch_geometric.loader import DataLoader

import wandb

class LitREST(L.LightningModule):
    
    def __init__(self  , fire_rate  , multi  , T):
        
        super(LitREST, self).__init__()

        self.fire_rate = fire_rate
        self.multi = multi
        self.T = T

        
        self.l1 = Linear(100 , 32 , bias = False)
        self.l2 = Linear(32 , 32 )
    
        self.gc1 = GraphConv(32 , 32 )
        self.gc2 = GraphConv(32 , 32 )

            
        self.fc = torch.nn.Linear(32, 1)
        torch.set_float32_matmul_precision('high')
        

    def update(self, x_t , edge_index , edge_weight  , s_t , fire_rate ):

        if s_t is  None:
            s_t =   self.l1(x_t)      
        else:
            s_t =   self.l1(x_t) +  self.l2(s_t)


        
        ds = self.gc1(s_t , edge_index ,  edge_weight.float() )
        ds = ds.relu()
        ds = self.gc2(ds , edge_index ,  edge_weight.float() )

        update_mask = torch.rand(ds.size()).float().cuda() <= fire_rate
        ds *= update_mask
        s_t = s_t + ds
        
        return s_t 

    def forward(self , data ):

        clip = (data.x.float()  - 
            data.x.float().mean(2, keepdim=True))/(data.x.float().std(2, keepdim=True) +1e-10)
        
        s_t = None
    
        for t in range (self.T):
            
            if self.multi == True:
                N = int(torch.randint(1,10 , (1,)))
            if self.multi == False:
                N = 1
            
            for i in range(N):
            
                x_t = clip[:,t,:].float()
                s_t  = self.update(x_t ,data.edge_index , data.edge_weight , s_t , fire_rate = self.fire_rate)
            
        return self.fc(s_t)


    def training_step(self, data , batch_idx ):
 
        s =  self(data) 
        out = global_mean_pool (s , data.batch)

        loss = F.mse_loss (torch.sigmoid(out.reshape(-1,1)) , data.y.type(torch.float32).reshape(-1,1)   )
        # loss = F.binary_cross_entropy_with_logits( out.reshape(-1,1) , data.y.type(torch.float32).reshape(-1,1)   )
        
        if batch_idx%5 == 0:
            wandb.log({ "loss-CA-gconv-bce": loss})
        
        return loss

    def configure_optimizers(self):
        
        optimizer = optim.Adam(params=model.parameters(),
                           lr = 5e-4)
        scheduler = torch.optim.lr_scheduler.MultiStepLR(optimizer, [1000 , 2000], 0.3)
        
        return [optimizer], [{"scheduler": scheduler, "interval": "epoch"}]