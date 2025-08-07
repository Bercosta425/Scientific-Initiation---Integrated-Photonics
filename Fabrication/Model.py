import matplotlib.pyplot as plt
import numpy as np

#Parâmetro modificáveis: tau = tempo para corroer o taper, em segundos; R0 = raio da fibra, em micrometros; theta1 = angulo do taper, em graus
R0 = 62.5
theta1 = 8*np.pi/180
theta2 = 10*np.pi/180
tau = 3000


#Y é o valor do comprimento do taper. h é a velocidade em que o menisco desce. tau é o tempo que demora para corroer o taper completamente.
def Y(h, tau):
    return h * tau
#Função que retorna a velocidade de subida em função do angulo theta que queira, em 10^-6 m/s.
def v(theta, R0, tau):
    theta = theta * np.pi/180
    a = R0/(np.tan(theta/2)*tau)
    a = "%.2f" % a
    a = str(a)
    return a


# #Parâmetro modificáveis: h = velocidade para cima, em m/s; tau = tempo para corroer o taper, em segundos; 
# h1 = v(theta1, R0, tau)
# h2 = v(theta2, R0, tau)
# print(h1, h2)v
# t = 1#(tamanho da fibra sendo mostrada)

# #Define os pontos das linhas verticais do plot 1
# x = [R0 for i in range(t)]
# y = [i for i in np.arange(Y(h1, tau), t + Y(h1, tau))]
# x2 = [-R0 for i in range(t)]
# y2 = [i for i in np.arange(Y(h1, tau), t + Y(h1, tau))]

# #Define os pontos das linhas verticais do plot 2
# y = [i for i in np.arange(Y(h2, tau), t + Y(h2, tau))]
# y2 = [i for i in np.arange(Y(h2, tau), t + Y(h2, tau))]

# largura1 = np.linspace(0, R0, 20)
# altura1 = np.linspace(0, Y(h1, tau), 20)
# altura2 = np.linspace(0, Y(h2, tau), 20)
# largura2 = np.linspace(0, -R0, 20)


# # Create a Matplotlib figure and axis
# fig, ax = plt.subplots()


# # Add vertical lines at specific x-values
# ax.axvline(x=-R0, ymin = 0.95, color='blue')
# ax.axvline(x=R0, ymin = 0.95, color='blue')

# ax.axvline(x=0, ymin = 0.05, color='orange')



# #Plot as linhas verticais
# ax.plot(x, y, color = "blue")
# ax.plot(x2, y2, color = "blue")

# #Plot do taper
# ax.plot(largura1, altura1, color = "blue")
# ax.plot(largura2, altura1, color = "blue")
# ax.plot(largura1, altura2, color = "red")
# ax.plot(largura2, altura2, color = "red")


# # Add labels and a legend
# ax.set_xlabel('Largura(10^-6 m)')
# ax.set_ylabel('Comprimento(10^-6 m)')
# ax.set_title('Exemplificação do modelo de fibra')
# ax.legend()

# # Show the plot
# plt.show()



