root_path = 'miniconda3'
import sys
sys.path.append(f'{root_path}envs/mp/lib/python3.12.4/site-packages/')

import meep as mp
import numpy as np
from mpi4py.MPI import COMM_WORLD
import matplotlib.pyplot as plt
from IPython.display import clear_output, Math, HTML

comm = COMM_WORLD
rank = comm.Get_rank()

tot_flux = 10+rank
rec_flux = 0
if rank == 0:
    comm.send(tot_flux, dest=1, tag=11)
    rec_flux = comm.recv(source=1, tag=11)
elif rank == 1:
    comm.send(tot_flux, dest=0, tag=11)
    rec_flux = comm.recv(source=0, tag=11)

print(f'i am rank {rank}. Sent {tot_flux} and received {rec_flux}')