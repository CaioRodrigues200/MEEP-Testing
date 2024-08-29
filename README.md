# MEEP-Testing

# Guia do repositório

Este repositório contém simulações e testes acerca do uso do software open-source MEEP para aplicações de sistemas de comunicações ópticos. O mesmo é seccionado em arquivos de guia de instalação, notebooks de simulação e documentação geral.

## Instalação de pre-requisitos

Para começar, leia o notebook **MEEP_Instalations.ipynb** para instalar os pacotes necessários.

## MEEP

Simulações de teste e tutoriais básicos podem ser encontrados no notebook **MEEPBasicView.ipynb**. 

Arquivos de imagem de GIFs podem ser encontrados na pasta **pngComponents**.

Simulações utilizando o MPI podem ser encontrados na pasta **ParallelResults**.

Por fim, a documentação geral encontra-se na pasta **Documentation**

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