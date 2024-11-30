import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def routh_hurwitz(coefficients):
    n = len(coefficients)
    rows = (n + 1) // 2  # número de filas
    routh_table = np.zeros((n, rows))
    
    # Llenamos la primera y segunda fila de la tabla
    routh_table[0, :len(coefficients[::2])] = coefficients[::2]  # coeficientes de s^n, s^(n-2), ...
    routh_table[1, :len(coefficients[1::2])] = coefficients[1::2]  # coeficientes de s^(n-1), s^(n-3), ...
    
    def is_row_zero(row):
        return np.all(routh_table[row] == 0)
    
    def replace_zero_with_constant(row):
        routh_table[row, 0] = 1  # constante x para reemplazar el cero en la primera columna
    
    changes_in_sign = 0
    case1 = False
    case2 = False
    case2_info = []
    
    # Generamos el resto de la tabla de Routh
    for i in range(2, n):
        for j in range(rows - 1):
            a = routh_table[i-2, 0]
            b = routh_table[i-2, j+1] if j+1 < len(routh_table[i-2]) else 0
            c = routh_table[i-1, 0]
            d = routh_table[i-1, j+1] if j+1 < len(routh_table[i-1]) else 0
            
            # Aplicamos la fórmula corregida
            numerator = -(a * d - c * b)
            denominator = c
            if denominator == 0:
                case1 = True
                replace_zero_with_constant(i-1)
                denominator = routh_table[i-1, 0]
            routh_table[i, j] = numerator / denominator if denominator != 0 else 0
        
        # Caso 2: si una fila entera es 0
        if is_row_zero(i):
            case2 = True
            # Construcción del polinomio auxiliar
            order = n - i  # Orden correspondiente a la fila
            aux_poly_coeffs = routh_table[i-1, :np.count_nonzero(routh_table[i-1])]  # Coeficientes de la fila anterior (s^n-1)
            powers = np.arange(order, -1, -2)  # Potencias para el polinomio auxiliar (s^n, s^(n-2), s^0)
            
            # Construimos la cadena que representa el polinomio auxiliar
            aux_poly_str = " + ".join([f"{coeff:.2f}s^{p}" if p != 0 else f"{coeff:.2f}" for coeff, p in zip(aux_poly_coeffs, powers)])
            
            # Cálculo de la derivada manualmente respetando las potencias
            derivative_terms = [f"{coeff * p:.2f}s^{p-1}" if p != 1 else f"{coeff * p:.2f}s" for coeff, p in zip(aux_poly_coeffs, powers) if p > 0]
            aux_poly_derivative_str = " + ".join(derivative_terms)
            
            # Almacenar la derivada en la tabla de Routh
            routh_table[i, :len(derivative_terms)] = [coeff * p for coeff, p in zip(aux_poly_coeffs, powers) if p > 0]
            case2_info = [i, routh_table[i-1], aux_poly_str, aux_poly_derivative_str]
    
    # Evaluación de cambios de signo en la primera columna
    first_column = routh_table[:, 0]  # Obtenemos los primeros términos de cada fila
    for i in range(1, len(first_column)):
        if first_column[i-1] * first_column[i] < 0:  # Si hay un cambio de signo
            changes_in_sign += 1
    
    return routh_table, changes_in_sign, case1, case2, case2_info

def plot_routh_table(routh_table, coefficients):
    rows = ['s^' + str(i) for i in range(len(coefficients)-1, -1, -1)]
    df = pd.DataFrame(routh_table, index=rows, columns=['']*routh_table.shape[1])  # Quitar encabezados de columnas
    df = df.replace(0, '-')  # Para mayor claridad en los ceros
    print("Tabla de Routh-Hurwitz:")
    print(df)

def stability_analysis(changes_in_sign, case1, case2, case2_info):
    if changes_in_sign == 0:
        if case1 or case2:
            print("El sistema es marginalmente estable, ya que no hubo cambios de signo y se presentó un caso 1 o 2.")
        else:
            print("El sistema es estable, ya que no hubo cambios de signo.")
    else:
        print(f"El sistema es inestable. Hay {changes_in_sign} cambio(s) de signo, lo que indica {changes_in_sign} polo(s) en el semiplano derecho.")
    
    if case1:
        print("El sistema tiene un caso 1: Primer término igual a cero.")
    if case2:
        row, prev_row, aux_poly_str, aux_poly_derivative_str = case2_info
        order = len(routh_table) - row - 1
        print(f"El sistema tiene un caso 2 en la fila s^{order}:")
        print(f"Fila anterior: {prev_row}")
        print(f"Polinomio auxiliar construido: {aux_poly_str}")
        print(f"Derivada del polinomio auxiliar: {aux_poly_derivative_str}")
    
# Ejemplo de coeficientes
coefficients = [2,3,2,3,1,2,3,2]

# Generar tabla de Routh-Hurwitz
routh_table, changes_in_sign, case1, case2, case2_info = routh_hurwitz(coefficients)

# Mostrar tabla y análisis
plot_routh_table(routh_table, coefficients)
stability_analysis(changes_in_sign, case1, case2, case2_info)
