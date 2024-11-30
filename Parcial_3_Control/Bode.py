# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt

def bode_plot_time_delay(T, w_start=1e-4, w_end=1e4, num_points=1000):
    """
    Genera el diagrama de Bode para una función de transferencia con retraso en el tiempo G(s) = e^(-Ts).

    Parameters:
    - T: Tiempo de retraso.
    - w_start: Frecuencia inicial (rad/s).
    - w_end: Frecuencia final (rad/s).
    - num_points: Número de puntos en la escala logarítmica de frecuencias.
    """
    # Frecuencia angular
    w = np.logspace(np.log10(w_start), np.log10(w_end), num_points)
    
    # Magnitud y fase
    magnitude = np.zeros_like(w)  # Magnitud constante en 0 dB
    phase = -w * T * (180 / np.pi)  # Fase lineal decreciente: -ωT, convertido a grados
    
    # Gráficos
    plt.figure(figsize=(10, 6))

    # Magnitud
    plt.subplot(2, 1, 1)
    plt.semilogx(w, magnitude)
    plt.title('Diagrama de Bode para G(s) = e^(-Ts)')
    plt.ylabel('Magnitud (dB)')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Fase
    plt.subplot(2, 1, 2)
    plt.semilogx(w, phase)
    plt.xlabel('Frecuencia (rad/s)')
    plt.ylabel('Fase (grados)')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    plt.tight_layout()
    plt.show()


# Ejemplo con T = 7 segundos
bode_plot_time_delay(T=7, w_start=1e-4, w_end=1e4)
