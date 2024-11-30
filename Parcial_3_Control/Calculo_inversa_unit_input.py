from sympy import symbols, inverse_laplace_transform, Heaviside, Function
from sympy.abc import s, t

# Definimos la función de transferencia G(s)
numerator = s + 1  # Numerador de G(s)
denominator = s**2 + 2*s + 2  # Denominador de G(s)
G_s = numerator / denominator

# Entrada: u(t) = 5 * impulso(t) => en Laplace: U(s) = 5
U_s = 5

# Salida en el dominio de Laplace: Y(s) = G(s) * U(s)
Y_s = G_s * U_s

# Transformada inversa de Laplace para obtener la salida en el tiempo
y_t = inverse_laplace_transform(Y_s, s, t)

print("La salida en el dominio del tiempo es:")
print(y_t)
    