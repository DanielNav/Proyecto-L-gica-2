print("Importando paquetes...")
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
print("Listo!")

fig, ax = plt.subplots()
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_xlim(0,1)
ax.set_ylim(0,1)

circle_A = plt.Circle((0.2, 0.8), 0.08, color='#636363')
circle_B = plt.Circle((0.8, 0.8), 0.08, color='#9c9c9c')
circle_C = plt.Circle((0.5, 0.2), 0.08, color='#333333', clip_on=False)

letrasProp = ['b', 'c', 'd', 'f', 'g', 'h']
puntos = ['A', 'B', 'C']
f = ['-b', 'c', 'd', '-f', 'g', 'h']

for i in f:
	if i in letrasProp:
		if i == 'b':
			line_b = plt.plot( [0.2,0.8],[0.8,0.8], linewidth = 2.0, color='#48A9B0')
			#azul plateado

		elif i == 'c':
			line_c = plt.plot( [0.17,0.47],[0.8,0.2], linewidth = 2.0, color='#FA0501')
			#rojo

		elif i == 'd':
			line_d = plt.plot( [0.17,0.83],[0.83,0.83], linewidth = 2.0, color='#14FA03')
			#verde

		elif i == 'f':
			line_f = plt.plot( [0.53,0.83],[0.2,0.8], linewidth = 2.0, color = '#0501FA')
			#azul

		elif i == 'g':
			line_g = plt.plot( [0.2,0.5],[0.8,0.2], linewidth = 2.0, color='purple')
			#morado

		else:
			line_h = plt.plot( [0.5,0.8],[0.2,0.8], linewidth = 2.0, color = '#F38347')
			#naranja


ax.add_artist(circle_A)
ax.add_artist(circle_B)
ax.add_artist(circle_C)


fig.savefig("plotcircles1.png")


def dibujar_tablero(f):

    fig, axes = plt.subplots()
    axes.get_xaxis().set_visible(False)
    axes.get_yaxis().set_visible(False)

    # Dibujo el tablero
    step = 1./4
    tangulos = []

    # Creo los cuadrados de los puntos columnas

    tangulos.append(patches.Rectangle((1*step, 3*step), step, step,\
                                      facecolor='#636363'))

    tangulos.append(patches.Rectangle((2*step, 3*step), step, step,\
                                    facecolor='#9c9c9c'))

    tangulos.append(patches.Rectangle((3*step, 3*step), step, step,\
                                    facecolor='#333333'))

    # Creo los cuadrados de los puntos filas

    tangulos.append(patches.Rectangle((0*step, 2*step), step, step,\
                                    facecolor='#636363'))

    tangulos.append(patches.Rectangle((0*step, 1*step), step, step,\
                                    facecolor='#9c9c9c'))

    tangulos.append(patches.Rectangle((0*step, 0*step), step, step,\
                                    facecolor='#333333'))


    # Creando las direcciones en la imagen de acuerdo a literal
    direcciones = {}
    direcciones[1] = [0.375, 0.850]
    direcciones[2] = [0.625, 0.850]
    direcciones[3] = [0.87, 0.850]
    direcciones[4] = [0.125, 0.6]
    direcciones[5] = [0.125, 0.35]
    direcciones[6] = [0.125, 0.09]
    direcciones[7] = [0.625, 0.6]
    direcciones[8] = [0.87, 0.6]
    direcciones[9] = [0.375, 0.35]
    direcciones[10] = [0.87, 0.35]
    direcciones[11] = [0.375, 0.09]
    direcciones[12] = [0.625, 0.09]




    #LABELING
    i = 1
    while i<4:
        plt.text(direcciones[i][0], direcciones[i][1], str(puntos[i-1]), fontsize=20, horizontalalignment='center')
        i = i+1

    while i<7:
        plt.text(direcciones[i][0], direcciones[i][1], str(puntos[i-4]), fontsize=20, horizontalalignment='center')
        i = i+1

    while i<13:
        plt.text(direcciones[i][0], direcciones[i][1], str(letrasProp[i-7]), fontsize=20, horizontalalignment='center')
        i = i+1


    #COLORING LABELS

    for i in f:
        if i in letrasProp:
            if i == 'b':
                tangulos.append(patches.Rectangle((2 * step, 2 * step), step, step,\
                                                  facecolor='#48A9B0'))


            elif i == 'c':
                tangulos.append(patches.Rectangle((3 * step, 2 * step), step, step,\
                                                  facecolor='#FA0501'))


            elif i == 'd':
                tangulos.append(patches.Rectangle((1 * step, 1 * step), step, step,\
                                                facecolor='#14FA03'))

            elif i == 'f':
                tangulos.append(patches.Rectangle((3 * step, 1 * step), step, step,\
                                                facecolor='#0501FA'))

            elif i == 'g':
                tangulos.append(patches.Rectangle((1 * step, 0 * step), step, step,\
                                                facecolor='purple'))

            else:
              tangulos.append(patches.Rectangle((2 * step, 0 * step), step, step,\
                                                facecolor='#F38347'))



    # Creo las líneas del tablero
    for j in range(3):
        locacion = j * step
        # Crea linea horizontal en el rectangulo
        tangulos.append(patches.Rectangle(*[(0, step + locacion), 1, 0.005],\
                                          facecolor='black'))
        # Crea linea vertical en el rectangulo
        tangulos.append(patches.Rectangle(*[(step + locacion, 0), 0.005, 1],\
                                        facecolor='black'))

    for t in tangulos:
        axes.add_patch(t)

        fig.savefig("tablero_" + str(1) + ".png")


dibujar_tablero(f)
