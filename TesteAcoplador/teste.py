import meep as mp
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio   
import scipy.signal
from scipy.special import erfc
import scipy as sp
from meep.materials import Si,SiO2 ## Problem!
plt.rcParams["figure.figsize"] = (12,6)



SiO2 = mp.Medium(epsilon=2.25)
Si = mp.Medium(epsilon=12)

resolution = 6
three_d = True

gdsII_file = 'demo.gds'
CELL_LAYER = 1
ESTRUTURA_LAYER = 2
SOURCE_LAYER = 4
PORT1_LAYER = 3
PORT2_LAYER = 5
PORT3_LAYER = 6
PORT4_LAYER = 7

default_d = 0.3

t_oxide = 2.0
t_Si = 0.22


dpml = 1
cell_thickness = dpml+t_oxide+dpml

SiO2 = mp.Medium(epsilon=2.25)
Si = mp.Medium(epsilon=12)

λinicial = 1520e-9 *1e6
λfinal = 1575e-9 *1e6
Npontos = 20

finicial = 1/λfinal
ffinal = 1/λinicial


fcen = (ffinal + finicial)/2  # pulse center frequency
df = ffinal - finicial   # pulse width (in frequency)

####
cell_zmax = 0.5*cell_thickness if three_d else 0
cell_zmin = -0.5*cell_thickness if three_d else 0
si_zmax = 0.5*t_Si if three_d else 10
si_zmin = -0.5*t_Si if three_d else -10

estrutura = mp.get_GDSII_prisms(Si, gdsII_file, ESTRUTURA_LAYER, si_zmin, si_zmax)

# cell = mp.GDSII_vol(gdsII_file, CELL_LAYER, cell_zmin, cell_zmax)
# p1 = mp.GDSII_vol(gdsII_file, PORT1_LAYER, si_zmin, si_zmax)
# p2 = mp.GDSII_vol(gdsII_file, PORT2_LAYER, si_zmin, si_zmax)
# p3 = mp.GDSII_vol(gdsII_file, PORT3_LAYER, si_zmin, si_zmax)
# p4 = mp.GDSII_vol(gdsII_file, PORT4_LAYER, si_zmin, si_zmax)
# src_vol = mp.GDSII_vol(gdsII_file, SOURCE_LAYER, si_zmin, si_zmax)

cell = mp.GDSII_vol(gdsII_file, CELL_LAYER, cell_zmin, cell_zmax)
p1 = mp.GDSII_vol(gdsII_file, PORT1_LAYER, cell_zmin, cell_zmax)
p2 = mp.GDSII_vol(gdsII_file, PORT2_LAYER, cell_zmin, cell_zmax)
p3 = mp.GDSII_vol(gdsII_file, PORT3_LAYER, cell_zmin, cell_zmax)
p4 = mp.GDSII_vol(gdsII_file, PORT4_LAYER, cell_zmin, cell_zmax)
src_vol = mp.GDSII_vol(gdsII_file, SOURCE_LAYER, cell_zmin, cell_zmax)
sources = [mp.EigenModeSource(src=mp.GaussianSource(fcen,fwidth=df),
                                  volume=src_vol,
                                  eig_parity=mp.NO_PARITY if three_d else mp.EVEN_Y+mp.ODD_Z)]

# sources = [mp.EigenModeSource(src=mp.ContinuousSource(fcen,fwidth=df),
#                               volume=src_vol,
#                               eig_parity=mp.EVEN_Y+mp.ODD_Z)]

sim = mp.Simulation(resolution=resolution,
                    cell_size=cell.size,
                    boundary_layers=[mp.PML(dpml)],
                    sources=sources,
                    geometry=estrutura,
                    default_material=SiO2)


mode1 = sim.add_mode_monitor(fcen, df, Npontos, mp.ModeRegion(volume=p1))
mode2 = sim.add_mode_monitor(fcen, df, Npontos, mp.ModeRegion(volume=p2))
mode3 = sim.add_mode_monitor(fcen, df, Npontos, mp.ModeRegion(volume=p3))
mode4 = sim.add_mode_monitor(fcen, df, Npontos, mp.ModeRegion(volume=p4))


#sim.plot2D(output_plane=mp.Volume(center=mp.Vector3(0,0,0), size=mp.Vector3(30.4,30.4,0)))

mp.verbosity(3)
sim.use_output_directory()
sim.run(mp.in_volume(mp.Volume(center=mp.Vector3(0,0,0), size=mp.Vector3(30.4,30.4,0)),mp.at_every(50 , mp.output_png(mp.Ey, "-Zc dkbluered"))),until_after_sources=400)

# 

#plt.figure()
# mp.plot2D(sim,fields=mp.Ez,
#         plot_sources_flag=True,
#         plot_monitors_flag=True,
#         plot_boundaries_flag=True)
sim.plot2D(output_plane=mp.Volume(center=mp.Vector3(0,0,0), size=mp.Vector3(30.4,30.4,0)),fields=mp.Ez)
if mp.am_master():
    
    plt.axis('off')
    plt.savefig('campo.png')
#S parameters
p1_trans = np.zeros(Npontos)
p2_trans = np.zeros(Npontos)
p3_trans = np.zeros(Npontos)
p4_trans = np.zeros(Npontos)

from IPython.utils import io

# with io.capture_output() as captured:
for i in range(Npontos):
    p1_coeff = sim.get_eigenmode_coefficients(mode1, [1], eig_parity=mp.NO_PARITY if three_d else mp.EVEN_Y+mp.ODD_Z).alpha[0,i,0]
    p1r_coeff = sim.get_eigenmode_coefficients(mode1, [1], eig_parity=mp.NO_PARITY if three_d else mp.EVEN_Y+mp.ODD_Z).alpha[0,i,1]
    p2_coeff = sim.get_eigenmode_coefficients(mode2, [1], eig_parity=mp.NO_PARITY if three_d else mp.EVEN_Y+mp.ODD_Z).alpha[0,i,1]
    p3_coeff = sim.get_eigenmode_coefficients(mode3, [1], eig_parity=mp.NO_PARITY if three_d else mp.EVEN_Y+mp.ODD_Z).alpha[0,i,0]
    p4_coeff = sim.get_eigenmode_coefficients(mode4, [1], eig_parity=mp.NO_PARITY if three_d else mp.EVEN_Y+mp.ODD_Z).alpha[0,i,0]

    # transmittance
    p1_trans[i] = abs(p1r_coeff)**2/abs(p1_coeff)**2
    p2_trans[i] = abs(p2_coeff)**2/abs(p1_coeff)**2
    p3_trans[i]= abs(p3_coeff)**2/abs(p1_coeff)**2
    p4_trans[i] = abs(p4_coeff)**2/abs(p1_coeff)**2

if mp.am_master():
    plt.figure(2)
    w = np.linspace(1520,1575,Npontos)
    plt.plot(p3_trans)
    plt.plot(p4_trans)

    plt.savefig('transmissao.png')

# print('Fim')
#     #plt.figure()
# #    


# #     w = np.linspace(1520,1575,Npontos)
# #     plt.plot(p3_trans)
# #     plt.plot(p4_trans)
# #     plt.savefig('Teste.png')
# #     plt.figure(2)
# #     plt.plot(p1_trans)
# #     plt.plot(p2_trans)
