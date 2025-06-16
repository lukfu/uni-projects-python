import pickle
import torch
import io
import numpy


#class CPU_Unpickler(pickle.Unpickler):
#    def find_class(self, module, name):
#        if module == 'torch.storage' and name == '_load_from_bytes':
#            return lambda b: torch.load(io.BytesIO(b), map_location='cpu')
#        else: return super().find_class(module, name)


#with open('C:/Users/BeH4ppy/DeepH/graph/HGraph-npz-graphene-5l-6.0r0mn.pkl', 'rb') as file:
#    data = CPU_Unpickler(file).load()

with open('C:/Users/BeH4ppy/DeepH/graph/HGraph-npz-graphene-5l-6.0r0mn.pkl', 'rb') as file:
    pickle.load(file)  # , protocol=pickle.HIGHEST_PROTOCOL

#print(data)
