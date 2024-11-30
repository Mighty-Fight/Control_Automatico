import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from control.matlab import TransferFunction, feedback, step, bode, pole, zero

# Planta del sistema
num_planta = [41.3]
den_planta = [75, 1]
G = TransferFunction(num_planta, den_planta)

# Función para actualizar las gráficas
def actualizar_graficas(Kp, Ki, Kd):
    """
    Actualiza las gráficas basadas en los valores de Kp, Ki y Kd.
    """
    # Controlador PID
    num_controlador = [float(Kd), float(Kp), float(Ki)]
    den_controlador = [1, 0]
    C = TransferFunction(num_controlador, den_controlador)

    # Sistema en lazo cerrado
    G_cerrado = feedback(C * G, 1)

    # Respuesta al escalón
    t, y = step(G_cerrado)

    # Polos y ceros
    polos = pole(G_cerrado)
    ceros = zero(G_cerrado)

    # Diagrama de Bode
    omega = np.logspace(-2, 2, 500)
    mag, phase, omega = bode(G_cerrado, omega)

    # Crear subplots
    fig, axs = plt.subplots(3, 1, figsize=(12, 18))

    # Respuesta al escalón
    axs[0].plot(t, y, label='Respuesta al escalón')
    axs[0].axhline(1, color='r', linestyle='--', label='Referencia')
    axs[0].set_title('Respuesta al Escalón - Controlador PID')
    axs[0].set_xlabel('Tiempo (s)')
    axs[0].set_ylabel('Amplitud')
    axs[0].grid(True)
    axs[0].legend()

    # Polos y ceros
    axs[1].scatter(np.real(polos), np.imag(polos), color='red', label='Polos', s=100)
    axs[1].scatter(np.real(ceros), np.imag(ceros), color='blue', label='Ceros', s=100)
    axs[1].axhline(0, color='black', linestyle='--')
    axs[1].axvline(0, color='black', linestyle='--')
    axs[1].set_title('Diagrama de Polos y Ceros')
    axs[1].set_xlabel('Re')
    axs[1].set_ylabel('Im')
    axs[1].grid(True)
    axs[1].legend()

    # Diagrama de Bode
    axs[2].semilogx(omega, 20 * np.log10(mag), label='Magnitud')
    axs[2].semilogx(omega, np.degrees(phase), label='Fase', linestyle='--')
    axs[2].set_title('Diagrama de Bode')
    axs[2].set_xlabel('Frecuencia (rad/s)')
    axs[2].set_ylabel('Magnitud (dB) / Fase (°)')
    axs[2].grid(True)
    axs[2].legend()

    plt.tight_layout()
    plt.show()

# Crear ventana principal
root = tk.Tk()
root.title("Controlador PID")

# Variables para los parámetros
Kp_var = tk.DoubleVar(value=1.0)
Ki_var = tk.DoubleVar(value=0.1)
Kd_var = tk.DoubleVar(value=0.05)

# Crear etiquetas y entradas para Kp, Ki, Kd
ttk.Label(root, text="Ganancia Proporcional (Kp):").grid(row=0, column=0, padx=10, pady=5)
ttk.Entry(root, textvariable=Kp_var).grid(row=0, column=1, padx=10, pady=5)

ttk.Label(root, text="Ganancia Integral (Ki):").grid(row=1, column=0, padx=10, pady=5)
ttk.Entry(root, textvariable=Ki_var).grid(row=1, column=1, padx=10, pady=5)

ttk.Label(root, text="Ganancia Derivativa (Kd):").grid(row=2, column=0, padx=10, pady=5)
ttk.Entry(root, textvariable=Kd_var).grid(row=2, column=1, padx=10, pady=5)

# Botón para actualizar las gráficas
def generar_graficas():
    """
    Llama a la función para actualizar gráficas con los valores actuales.
    """
    Kp = Kp_var.get()
    Ki = Ki_var.get()
    Kd = Kd_var.get()
    actualizar_graficas(Kp, Ki, Kd)

ttk.Button(root, text="Generar Gráficas", command=generar_graficas).grid(row=3, column=0, columnspan=2, pady=10)

# Ejecutar la aplicación
root.mainloop()
