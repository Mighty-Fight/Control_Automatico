import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from control.matlab import TransferFunction, bode

# Planta del sistema
num_planta = [41.3]
den_planta = [75, 1]
G = TransferFunction(num_planta, den_planta)

# Crear una figura global para el diagrama de Bode
fig, ax_mag = plt.subplots(figsize=(8, 6))
ax_phase = ax_mag.twinx()  # Crear un segundo eje para la fase
plt.ion()  # Modo interactivo

def actualizar_bode(Kp, Ki, Kd):
    """
    Actualiza el diagrama de Bode dinámicamente.
    """
    # Limpiar las gráficas existentes
    ax_mag.cla()
    ax_phase.cla()

    # Controlador PID
    num_controlador = [float(Kd), float(Kp), float(Ki)]
    den_controlador = [1, 0]
    C = TransferFunction(num_controlador, den_controlador)

    # Sistema en lazo abierto
    G_abierto = C * G

    # Diagrama de Bode
    omega = np.logspace(-2, 2, 500)
    mag, phase, _ = bode(G_abierto, omega)

    # Magnitud
    ax_mag.semilogx(omega, 20 * np.log10(mag), color='blue', label='Magnitud')
    ax_mag.set_title('Diagrama de Bode - Controlador PID')
    ax_mag.set_xlabel('Frecuencia (rad/s)')
    ax_mag.set_ylabel('Magnitud (dB)', color='blue')
    ax_mag.grid(True)
    ax_mag.tick_params(axis='y', labelcolor='blue')

    # Fase
    ax_phase.semilogx(omega, np.degrees(phase), color='red', linestyle='--', label='Fase')
    ax_phase.set_ylabel('Fase (°)', color='red')
    ax_phase.tick_params(axis='y', labelcolor='red')

    # Redibujar
    fig.tight_layout()
    fig.canvas.draw()

# Crear la ventana principal
root = tk.Tk()
root.title("Diagrama de Bode - PID")

# Variables para las ganancias
Kp_var = tk.DoubleVar(value=1.0)
Ki_var = tk.DoubleVar(value=0.1)
Kd_var = tk.DoubleVar(value=0.05)

# Entradas para las ganancias
ttk.Label(root, text="Kp:").grid(row=0, column=0, padx=5, pady=5)
ttk.Entry(root, textvariable=Kp_var).grid(row=0, column=1, padx=5, pady=5)

ttk.Label(root, text="Ki:").grid(row=1, column=0, padx=5, pady=5)
ttk.Entry(root, textvariable=Ki_var).grid(row=1, column=1, padx=5, pady=5)

ttk.Label(root, text="Kd:").grid(row=2, column=0, padx=5, pady=5)
ttk.Entry(root, textvariable=Kd_var).grid(row=2, column=1, padx=5, pady=5)

# Botón para actualizar el diagrama de Bode
def generar_bode():
    actualizar_bode(Kp_var.get(), Ki_var.get(), Kd_var.get())

ttk.Button(root, text="Actualizar Bode", command=generar_bode).grid(row=3, column=0, columnspan=2, pady=10)

# Ejecutar la aplicación
root.mainloop()
