from configuration.train_configuration import TrainConfiguration
from data_loading.sampler_factory import SamplerFactory
import torch.optim as optim
import torch.nn as nn
from networks.autoencoder import AutoEncoder

# define these things here
loader = SamplerFactory.GetAESampler(max_frames=200)
model = AutoEncoder()
optimizer = optim.SGD(model.parameters(), lr=0.005, momentum=0.9)
loss = nn.BCELoss()

train_config = TrainConfiguration(loader,optimizer,model,loss)