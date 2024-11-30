from sympy import symbols, expand, apart, inverse_laplace_transform
from sympy.abc import s, t

# Definimos la función de transferencia H(s)
numerator = s**3 + 5*s**2 + 9*s + 7
denominator = (s + 1) * (s + 2)
H_s = numerator / denominator

# Expandimos H(s) en fracciones parciales para facilitar la transformada inversa
H_s_expanded = apart(H_s)

# Calculamos la transformada inversa de Laplace para obtener la respuesta en el tiempo
f_t = inverse_laplace_transform(H_s_expanded, s, t)

print("La respuesta en el tiempo es:")
print(f_t)
