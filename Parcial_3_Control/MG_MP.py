import numpy as np
import control as ctrl
import matplotlib.pyplot as plt

# Definir la representación en espacio de estados del sensor H(s)
A = np.array([[-1.2, -1], [1, 0]])
B = np.array([[1], [0]])
C = np.array([[0, 20]])
D = np.array([[0]])

# Crear el sistema en espacio de estados y convertirlo a función de transferencia
H = ctrl.ss2tf(A, B, C, D)

# Controlador Gc(s) y planta Gp(s)
Gc = ctrl.TransferFunction([3], [1])  # Controlador: Gc(s) = 3
Gp = ctrl.TransferFunction([1], [1, 10])  # Planta: Gp(s) = 1 / (s + 10)

# Sistema en lazo abierto
L = Gc * Gp * H

# Obtener los márgenes de ganancia (GM) y fase (PM)
gm, pm, wg, wp = ctrl.margin(L)

# Determinar si el sistema es estable
stability = "stable" if pm > 0 and gm > 1 else "unstable"

# Mostrar resultados
print(f"Phase Margin (PM): {pm:.2f} degrees")
print(f"Gain Margin (GM): {20 * np.log10(gm):.2f} dB")
print(f"System is {stability}.")

# Graficar diagramas de Bode
plt.figure(figsize=(10, 6))
ctrl.bode_plot(L, dB=True, margins=True)
plt.show()
