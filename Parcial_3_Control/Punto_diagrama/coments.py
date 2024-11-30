
# Respuestas a las preguntas de control de sistemas

# Pregunta 1:
# Enunciado: What is the primary purpose of lag (backward) compensation in control system design?
# Respuesta correcta: To improve the system's steady-state accuracy.
# Comentario: La compensación "lag" se usa principalmente para mejorar la precisión en el estado estacionario.

# Pregunta 2:
# Enunciado: If the constant of position error (Kp) is zero for a system, what can be inferred about the system's steady-state error?
# Respuesta correcta: The system has infinite steady-state error for all inputs.
# Comentario: Si Kp = 0, el sistema no puede corregir el error en el estado estacionario para ninguna entrada, por lo que el error será infinito.

# Pregunta 3:
# Enunciado: In control system analysis, what is the primary role of the gain margin?
# Respuesta correcta: To measure the safety margin before the system becomes unstable.
# Comentario: El margen de ganancia mide cuánto se puede aumentar la ganancia antes de que el sistema se vuelva inestable.

# Pregunta 4:
# Enunciado: What is the steady-state error for a type 1 system when the reference input is a unit step function, based on the Bode plot analysis?
# Respuesta correcta: 0
# Comentario: Un sistema tipo 1 tiene un error de estado estacionario de 0 para entradas tipo escalón, debido a su integrador.

# Pregunta 5:
# Enunciado: What is the primary advantage of using a lead-lag compensator in control system design?
# Respuesta correcta: To reduce steady-state error and improve transient response.
# Comentario: El compensador **lead-lag** mejora tanto la respuesta transitoria como el error en el estado estacionario.

# Pregunta 6:
# Enunciado: When should you use lead (forward) compensation in control system design?
# Respuesta correcta: When you need to increase the system's phase margin and speed up the transient response.
# Comentario: La compensación **lead** se utiliza para aumentar el margen de fase y mejorar la respuesta transitoria.

# Pregunta 7:
# Enunciado: A system with unity feedback has the following open-loop transfer function G(s). What is the gain K required to achieve a phase margin PM = 30°? With the calculated gain K, what is the steady-state error for a unit ramp input?
# Respuesta correcta: K = 10.82, e_ss = 0.6932
# Comentario: El valor de \( K \) requerido para obtener un margen de fase de 30° es 10.82, y el error en estado estacionario para una entrada de tipo rampa es 0.6932.

# Pregunta 8:
# Enunciado: Consider a control system with unity feedback whose open-loop transfer function is G(s). The value of alpha (α) such that the phase margin PM = 45° is?
# Respuesta correcta: α = 0.84
# Comentario: El valor de \( \alpha \) que asegura un margen de fase de 45° es 0.84.

# Enunciado: Consider the unity feedback system with an open-loop transfer function G(s) = 10/(s+1).
#            Determine the steady-state output of the system when subjected to the following input:
#            r(t) = sin(t + 30°) - 2 * cos(2t - 45°)

# Respuesta correcta:
# Css(t) = 0.905 * sin(t + 24.8°) - 1.788 * cos(2t - 55.3°)
