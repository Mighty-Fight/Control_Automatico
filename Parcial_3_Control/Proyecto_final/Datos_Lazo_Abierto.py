import serial
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time

# Configuración de la conexión serial
puerto = 'COM7'  # Cambia esto al puerto de tu Arduino
baudrate = 9600
arduino = serial.Serial(puerto, baudrate, timeout=1)

# Variables globales
consigna = 35.0  # Consigna inicial
temperatura = 0.0
error = 0.0
potencia = "0%"
datos_temperatura = []
datos_consigna = []
tiempos = []
inicio_tiempo = time.time()  # Referencia de tiempo inicial

# Función para actualizar los datos desde Arduino
def leer_datos_arduino():
    global consigna, temperatura, error, potencia
    while True:
        try:
            linea = arduino.readline().decode('utf-8').strip()
            if linea:
                if "TEMP:" in linea and "CONS:" in linea and "ERR:" in linea and "POT:" in linea:
                    partes = linea.split(',')
                    temperatura = float(partes[0].split(':')[1])
                    consigna = float(partes[1].split(':')[1])
                    error = float(partes[2].split(':')[1])
                    potencia = partes[3].split(':')[1]
                    
                    # Actualizar listas de datos
                    tiempo_actual = time.time() - inicio_tiempo
                    tiempos.append(tiempo_actual)
                    datos_temperatura.append(temperatura)
                    datos_consigna.append(consigna)
        except Exception as e:
            print(f"Error al leer datos: {e}")

# Función para enviar nueva consigna al Arduino
def enviar_nueva_consigna():
    global consigna
    nueva_consigna = consigna_entry.get()
    try:
        consigna = float(nueva_consigna)
        arduino.write(f"{consigna}\n".encode())  # Enviar nueva consigna al Arduino
        print(f"Consigna enviada: {consigna}")
    except ValueError:
        print("Por favor, ingresa un número válido.")

# Función para actualizar la interfaz gráfica
def actualizar_grafica():
    ax.clear()

    # Restar 20 para ajustar la visualización
    datos_temperatura_ajustados = [temp - 20 for temp in datos_temperatura]
    datos_consigna_ajustados = [cons - 20 for cons in datos_consigna]

    # Graficar los datos ajustados
    ax.plot(tiempos, datos_temperatura_ajustados, label='Temperatura (ajustada)', color='blue')
    ax.plot(tiempos, datos_consigna_ajustados, label='Consigna (ajustada)', color='red', linestyle='--')

    # Configurar la gráfica
    ax.set_title('Datos experimentales lazo abierto')
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Temperatura(°C)')
    ax.set_ylim(0, 50)  # Fijar el rango del eje Y de 0 a 100

    # Ajustar el eje X para que abarque todo el tiempo acumulado
    if tiempos:
        ax.set_xlim(0, tiempos[-1])  # Desde 0 hasta el último tiempo registrado

    ax.legend()
    canvas.draw()

    # Actualizar los datos en la interfaz
    error_label['text'] = f"Error: {error:.1f} °C"
    potencia_label['text'] = f"Potencia: {potencia}"
    potencia_bar['value'] = float(potencia.strip('%'))  # Actualizar barra de potencia

    # Programar la próxima actualización
    root.after(100, actualizar_grafica)


# Crear la ventana principal
root = tk.Tk()
root.title("Control de Temperatura - Interfaz Gráfica")

# Crear la figura de Matplotlib
fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Crear un marco para los controles y la barra de potencia
control_frame = tk.Frame(root)
control_frame.pack(side=tk.RIGHT, fill=tk.Y)

# Etiqueta de error
error_label = tk.Label(control_frame, text="Error: 0.0 °C", font=("Arial", 14))
error_label.pack(pady=10)

# Etiqueta de potencia
potencia_label = tk.Label(control_frame, text="Potencia: 0%", font=("Arial", 14))
potencia_label.pack(pady=10)

# Barra de potencia
potencia_bar = ttk.Progressbar(control_frame, orient="horizontal", length=200, mode="determinate")
potencia_bar.pack(pady=10)

# Entrada para cambiar la consigna
consigna_label = tk.Label(control_frame, text="Nueva Consigna:", font=("Arial", 14))
consigna_label.pack(pady=10)
consigna_entry = tk.Entry(control_frame, font=("Arial", 14))
consigna_entry.pack(pady=10)

# Botón para enviar la nueva consigna
consigna_button = tk.Button(control_frame, text="Enviar Consigna", command=enviar_nueva_consigna, font=("Arial", 14))
consigna_button.pack(pady=10)

# Iniciar el hilo para leer datos del Arduino
thread = threading.Thread(target=leer_datos_arduino, daemon=True)
thread.start()

# Iniciar la actualización de la gráfica
actualizar_grafica()

# Ejecutar la aplicación
root.mainloop()
