import torch
import torch.nn as nn

# 4 Hidden layers

class Model(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(Model,self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, hidden_size)
        self.l4 = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU() #Rectified Linear Unit. If output < 0, call it 0 and move on. Else, use output.
    def forward(self, x):
        x = self.relu(self.l1(x)) 
        x = self.relu(self.l2(x))
        x = self.relu(self.l3(x))
        x = self.l4(x) #Final output layer
        
        return x