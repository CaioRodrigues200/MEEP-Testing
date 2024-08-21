# MEEP-Testing

# Relatório

## Erros descobertos
- Inserir ``` sim.plot2D ``` dentro de um ```if mp.am_master():``` faz com que um erro nos processos do MPI seja gerado, a forma correta é: 

``` python
sim.plot2D(fields=mp.Ez,
            plot_sources_flag=True,
            plot_monitors_flag=True,
            plot_boundaries_flag=True,
            output_plane=mp.Volume(center=mp.Vector3(0,0,0), size=mp.Vector3(30.4,30.4,0)))
plt.axis('off')

if mp.am_master():

    plt.axis('off')
    plt.savefig("Plot2D_Ez.png", transparent=False, facecolor="white",  bbox_inches="tight")

```