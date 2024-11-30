import sys
import cv2
import pytesseract
import numpy as np
import pyautogui
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import Qt, QRect, QTimer
from PyQt5.QtGui import QPainter, QColor

# Configura la ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Define las frases clave y respuestas
keywords = {    
    "The figure depicts a control system. The system is desired to be stable, and the steady-state error for a unit step input should be less than or equal to 0.05 (5%)": "alpha = 0.98",
    "We have a system described by its root locus plot, as shown in the following figure. Use the Routh stability criterion to determine the range of positive values for the constant K for which the system in the figure is stable.": "M=0 < K < 4.50 ///Arco=0 < K < 727.34",
    "Consider a control system with unity feedback with the following transfer functions for the plant P(s) and its controller K(s), respectively. Using the Routh criterion, find the values of" : "0.0333 < alpha < 0.2077",
    "Find the stability region (K1 vs K2) for the control system depicted in the figure. (K2 must be positive).": "Stability Region 5",
    "Which of the following statements about the Routh-Hurwitz criterion is true": "It can be used to determine the stability of any linear time-invariant system",
    "Which of the following statements about the root locus method is true?":"It can be used to determine the stability of any linear time-invariant system",
    "Which of the following conditions is necessary for a system to be stable using the root locus method?" : "All the poles of the system must be in the left half of the complex plane",
    "How does a zero affect the root locus plot?": "It pulls the root locus towards it",
    "What is the significance of the Routh-Hurwitz": "It provides a necessary and sufficient condition for stability.",
    "In which case does the root locus method indicate that the system is critically damped?" : "When the root locus branches intersect the imaginary axis at complex conjugate poles",
    "How does the root locus method determine stability when the gain varies?": "By observing the movement of poles as gain changes.",
    "If the root locus plot of a system has a branch that approaches the imaginary axis asymptotically, it indicates:": "Sustained oscillations.",
    "True or False: A pole-zero cancellation in a control system always leads to instability, regardless of the location of the remaining poles.": "False.",
    "True or False: A system with a characteristic equation that has repeated roots is always stable according to the Routh-Hurwitz criterion.": "False.",
    "True or False: The number of roots in the right-half of the s-plane is equal to the number of sign changes in the first column of the Routh array.": "True.",
    "True or False: If all the roots of the characteristic equation of a system have negative real parts, then the system is stable.": "True.",
    "True or False: The root locus of a system with complex poles and zeros will always be symmetrical about the real axis.": "True.",
    "True or False: The root locus of a system with a single pole in the right half of the s-plane will always be in the right half of the s-plane.": "True.",
    "True or False: According to the Routh-Hurwitz criterion, if any row of the Routh array contains all zero elements, the system is unstable.": "False.",
    "True or False: The Routh-Hurwitz criterion can be used to determine both the stability and performance of a control system.": "False.",
    "True or False: A system is considered unstable if any coefficient of the characteristic polynomial is negative according to the Routh-Hurwitz criterion.": "True.",
    "True or False: A system with multiple poles lying on the imaginary axis in the root locus plot can exhibit sustained oscillations without instability.": "True.",
    "True or False: The root locus method can be applied to systems with time- varying parameters to analyze their stability over time.": "False.",
    "True or False: A system with a dominant pole closer to the imaginary axis in the root locus plot is more stable than a system with a dominant pole left-half farther away.": "False.",
    "Consider the unity feedback system with an open-loop transfer function G(s) = 10/(s+1). Determine the steady-state output of the system when subjected to the following input:": "C_ss(t) = 0.905sin(t + 24.8°) - 1.788cos(2t - 55.3°).",
    "A system with unity feedback has the following open-loop transfer function G(s). What is the gain K required to achieve a phase margin PM = 30°? With the calculated gain K, what is the steady-state error for a unit ramp input?": "K = 10.82, e_ss = 0.6932.",
    "The Figure shows a Bode magnitude plot of a control system for which only its frequency response is known. The system consists solely of simple zeros and poles, all of which are located in the left half-plane of the complex plane.": "3.521 (PM=75.43, GM=32.16) // 20 (PM=20.12, GM=9.6827)",
    "There is a control system consisting of the controller and the plant in the forward path, and the sensor in the negative feedback path. The transfer functions of the controller and the sensor are shown below. However, the plant has a standard second-order transfer function, and its unit step response is shown in the figure. Obtain the phase margin PM and gain margin": "PM = -61.85° and GM = -11.05dB -> unstable.",
    "However, for the sensor, the circuit diagram used for its implementation is known, and it is understood that H(s) is its voltage transfer function. The circuit diagram is also shown in the figure.": "PM = -36.41° and GM = -9.394dB -> unstable.",
    "In control systems, what is the primary purpose of a Bode plot?": "To represent frequency-domain behavior.",
    "If a control system exhibits a small phase margin, what is the likely impact on system behavior?": "Reduced stability and generate potential oscillations.",
    "For a stable system, which of the following statements about the phase margin is correct?": "Phase margin is always positive.",
    "In control systems, what is the primary goal of analyzing the phase margin?": "To assess the system's stability.",
    "When should you use lead (forward) compensation in control system design?": "When you need to increase the system's phase margin and speed up the transient response.",
    "What is the primary purpose of lag (backward) compensation in control system design?": "To improve the system's steady-state accuracy.",
    "What is the primary advantage of using a lead-lag compensator in control system design?": "To reduce steady-state error and improve transient response.",
    "What is the steady-state error for a type 1 system when the reference input is a unit step function, based on the Bode plot analysis?": "0.",
    "In control system analysis, what is the primary role of the gain margin?": "To measure the safety margin before the system becomes unstable.",
    "If the constant of position error (Kp) is zero for a system, what can be inferred about the system's steady-state error?": "The system has infinite steady-state error for all inputs.",
    "A compensator with the transfer function Gc(s)=(s+1)/(s+0.1) primarily does which of the following?": "Improves phase margin and increases bandwidth.",
    "What does a system's gain margin represent in the frequency domain?": "The maximum gain increase before instability occurs.",
    "Which of the following is true for a system with zero steady-state error for a step input?": "The system must have at least one integrator in its forward path.",
    "What effect does increasing the static velocity error constant Kv have on a system?": "Reduces the steady-state error for ramp inputs.",
    "A lead compensator has a transfer function Gc(s)=K(s+α)/(s+β) with α>β. What is the primary effect on the Bode plot?": "Adds positive phase and increases bandwidth.",
    "In the frequency domain, a system is characterized by the following: gain crossover frequency = 10 rad/s, phase margin = 15°, gain margin = 2 dB. What is the most likely conclusion?": "The system is stable but sensitive to gain variations.",
    "Accelerometers are used to measure velocity in conveyor belt systems.": "False.",
    "pH electrodes are used to measure the intensity of light in photography studios.": "False.",
    "Which of the following actuators would be most suitable for controlling the water level in the reservoir?": "Solenoid valve.",
    "On/Off control is a type of feedback control system.": "True.",
    "would be most suitable for measuring the position of the satellite antenna?": "Encoder.",
    "controlling the humidity levels in the mushroom farm?":"Ultrasonic humidifier",
    "In a chemical processing plant, a reactor is used to carry out various chemical":"Heater",
    "In a chemical processing plant, controlling the level of liquid in a reactor is crucial for":"Float Swicth",
    "In a hydroelectric dam, controlling the water level is critical for maintaining a steady":"Ultrasonic Sensor",
    "In an electric vehicle, the speed of the vehicle needs to be controlled to ensure safe":"PID control",
    "PID control is a type of open-loop control system.":"False",
    "In an oil storage facility, controlling the level of oil in the storage tanks is crucial for":"Ultrasonic Sensor",
    "In a greenhouse, the temperature needs to be regulated to ensure optimal growth":"Thermocouple",
    "In a high-rise building, an elevator system is used to transport people between":"DC Motor",
    "In addition to temperature control, the intensity of light inside the greenhouse also":"LDR",
    "In a photography studio, controlling the intensity of light is crucial for capturing":"Proportional control",
    "A thermistor is commonly used as a sensor in HVAC (heating, ventilation and air conditioning) systems.":"True",
    "In a water treatment plant, the pH level of the water needs to be regulated to ensure":"pH electrode",
    "LDRs (Light Dependent Resistors) are suitable for measuring light intensity in greenhouses":"True",
    "A solenoid valve is commonly used as an actuator in temperature control systems.": "True",
    "In a hydroelectric power plant, the governor system controls the flow of water":"Tachometer Generator",
    "An autonomous vehicle adjusts its speed to maintain a safe following distance from":"Kalman filtering",
    "In a smart building, the air conditioning system needs to maintain the temperature":"PID control",
    "A conveyor belt system in a packaging facility needs to maintain a constant speed of 2 meters":"Increase the motor speed to accelerate the conveyor belt.",
    "In a greenhouse, the temperature needs to be maintained at 25°C for optimal plant":"ON OFF Control",
    "In a water treatment plant, a tank is used to store treated water before distribution.":"Closed-loop control",
    "A cruise control system in an automobile needs to maintain a constant speed of 100":"Increase the throttle position to accelerate the vehicle",
    "In an Autonomous Underwater Vehicle (AUV), maintaining depth is crucial for":"Pressure sensor",
    "In a traffic light control system, traffic flow at an intersection is managed by":"Actuated control",
    "In a smart greenhouse, temperature and humidity are critical variables to control for":"Thermistor",
    "In a Heating, Ventilation, and Air Conditioning (HVAC) system, maintaining indoor":"PI Control",
    "You’re maintaining water levels in a storage tank. Which type of control action would you use to prevent overflow or depletion?":"On Off control",
    "In a power system, the voltage needs to be maintained at 220V. The voltage sensor":"Proportional-Integral-Derivative (PID) Control",
    "In a water treatment plant, the level of a storage tank needs to be maintained within":"Close the valve to decrease the outflow rate",
    "In a smart home, a thermostat controls heating and cooling systems to maintain":"Thermistor",
    "In an aircraft altitude control system, altitude is regulated to maintain a steady flight":"Radar Altimeter",
    "sensor would provide accurate solar azimuth and elevation angles?":"Inclinometer",
    "A robotic arm is required to move to a specific position within a tolerance of 1 mm":"Proportional-Integral (PI) Control",
    "A manufacturing plant needs to control the temperature of a chemical reactor. The":"Increase the heating power to raise the temperature.",
    "In a manufacturing facility, robotic arms are used to assemble electronic components":"PID control",
    "In a hydroelectric power plant situated in the mountainous regions of Antioquia, the":"Actuator: Machinery that controls the opening and closing of water gates",
    "In a solar power plant situated in a desert region, maximizing energy capture from":"Actuator: Motors or hydraulic cylinders adjusting the orientation of solar panels",
    "In a wind farm situated in a coastal region prone to gusty winds, wind turbine blades":"Integral time (Ti)",
    "In a warehouse environment where robotic vacuum cleaners navigate to maintain":"Controller: Systems analyzing sensor data and generating navigation commands.",
    "In the bustling streets of Barranquilla, autonomous vehicles navigate through heavy":"Camera: Optical sensors capturing visual information from the environment",
    "In a nuclear power plant operating near its thermal limits, maintaining safe reactor":"Controller: Systems analyzing reactor conditions and adjusting coolant flow",
    "In an oil refinery operating in a desert climate, precise temperature control is":"Actuator: Control valves regulating the flow of steam to heat exchangers.",
    "In a wastewater treatment plant situated in an industrial area, the pH control system":"Controller: Systems analyzing pH data and issuing commands to the dosing pumps.",
    "In a densely populated urban area experiencing rapid temperature changes":"Actuator: Equipment controlling the air conditioning unit.",
    "In an automated warehouse facility handling a high volume of packages, conveyor":"Actuator: Variable frequency drives controlling the speed of conveyor motors.",
    "In a geothermal power plant situated in a volcanic region, steam pressure control is":"Actuator: Steam control valves regulating the flow of steam through turbines.",
    "In a greenhouse located in a region with fluctuating weather patterns, an automated":"Proportional Gain",
    "In the mission control center of a space agency, engineers monitor and control the":"Actuator: Mechanisms controlling valves and fuel injectors.",
    "In a high-speed train braking system employed on a busy commuter line, precise":"Actuator: Brake pressure modulators adjusting braking force.",
    "In a wastewater treatment plant located in a densely populated urban area, the":"Controller: Systems analyzing contamination data and regulating chemical dosages.",
    "In a modern manufacturing facility producing consumer electronics, conveyor belts":"Proximity sensor: Devices detecting nearby objects without physical contact.",
    "In a hydroponic greenhouse facility, nutrient solution levels must be carefully":"Controller: Systems analyzing nutrient concentration data and issuing commands to ad‐just pump flow rates",
    "In a pharmaceutical manufacturing facility producing specialty drugs, precise control":"Actuator: Control valves adjusting the flow of heating or cooling fluids to the reactor.",
    "In an electric vehicle charging station located in a metropolitan area, the charging":"Actuator: Charging station equipment adjusting the charging rate of electric vehicles.",
    "In a steel manufacturing plant operating blast furnaces, precise control of furnace":"Actuator: Fuel and air control valves adjusting the flow of fuel and air to burners",
    "In a Bode plot, the effect of adding a complex conjugate pole pair at":"A resonant peak in the magnitude curve",
    "In the Bode plot, the asymptotic slope of the magnitude curve for a first-order system is:": "-20 dB/decade.",
    "The gain crossover frequency of a system can be determined from the Bode plot by:": "Finding the frequency where the magnitude curve crosses 0 dB.",
    "Which statement about a Bode plot is true?": "It displays both the magnitude and phase responses of a system.",
    "What is the slope of the phase response of a first-order system in a Bode plot?": "-45 degrees/decade.",
    "Which of the following statements is NOT true about Bode magnitude plots?": "The magnitude plot always has a slope of -20 dB/decade for frequencies below the break frequency.",
    "True or False: A Bode plot is a graphical representation of the impulse response of a system.": "False.",
    "The bandwidth of a system can be determined from the Bode plot by:": "Finding the frequency where the magnitude curve crosses 0 dB.",
    "In a Bode plot, the phase angle of a system with a single real pole at s = -a is:": "0° at low frequencies and -90° at high frequencies.",
    "True or False: Bode plots cannot be used to determine the bandwidth of a system.": "False.",
    "True or False: The cutoff frequency of a system can be determined from the Bode plot by finding the frequency where the magnitude curve decreases -3 dB.": "True.",
    "The phase margin of a system can be determined from the Bode plot by:": "Reading the phase angle at the gain crossover frequency.",
    "In a Bode plot, the effect of adding a real pole at s = -p to a system is:": "The magnitude curve has a slope of -20 dB/decade at high frequencies.",
    "Which of the following statements is true about the Bode plot of a system with a zero at the origin?": "The magnitude curve has a slope of +20 dB/decade at low frequencies.",
    "The Bode plot of a system with a double real pole at s = -a is characterized by:": "A magnitude curve slope of -40 dB/decade at high frequencies.",
    "In a Bode plot, the effect of adding a real zero at s = -z to a system is:": "The magnitude curve has a slope of +20 dB/decade at low frequencies.",
    "True or False: A system with multiple poles has a Bode plot with multiple corner frequencies.": "True.",
    "True or False: In a Bode plot, the asymptotic slope of the magnitude curve for an integrator is +20 dB/decade at low frequencies.": "False.",
    "True or False: Bode plots are a graphical representation of the frequency response of a system.": "True.",
    "Consider the transfer function G(s)=10/(s+10) as an approximation for an":"K >-1",
    "Given the Routh-Hurwitz criteria, can it be determined if the system with characteristic polynomial Q(s) is stable or unstable, and why?":"Stable. There are no sign changes in the first column of the Routh array, therefore, the system has all its roots in the left-hand side of the complex s-plane",
    "True or False: Bode plots are useful for analyzing both the frequency and time domain behavior of a system.": "True.",
    "Consider the system described in state-space form. What values of K keep the system stable?": "K > 1.",
    "How does the Routh-Hurwitz criterion handle systems with time-varying parameters?": "It becomes inapplicable.",
    "What does a zero entry in the first column of the Routh array indicate?": "A pole on the imaginary axis.",
    "What additional mathematical tools are often used in conjunction with the Routh-Hurwitz criterion for analyzing control system stability?": "Laplace transforms.",
    "The Routh-Hurwitz criterion is applicable to which type of systems?": "Linear time-invariant (LTI) systems.",
    "In the Routh-Hurwitz criterion, what is the implication if there are zero elements in the first column of the Routh array?": "Presence of complex poles.",
    "Consider the following characteristic equation. What is the range of values of K for the stability of the system?": "There is no value of K that allows the stability of the system.",
    "What is the minimum number of poles in the right-half plane for a stable system according to the Routh-Hurwitz criterion?": "0.",
    "True or False: Bode plots cannot be used to determine the bandwidth of a system.": "False.",
    "True or False: The cutoff frequency of a system can be determined from the Bode plot by finding the frequency where the magnitude curve decreases -3 dB.": "True.",
    "The phase margin of a system can be determined from the Bode plot by:": "Reading the phase angle at the gain crossover frequency.",
    "In a Bode plot, the effect of adding a real pole at s = -p to a system is:": "The magnitude curve has a slope of -20 dB/decade at high frequencies.",
    "Which of the following statements is true about the Bode plot of a system with a zero at the origin?": "The magnitude curve has a slope of +20 dB/decade at low frequencies.",
    "The Bode plot of a system with a double real pole at s = -a is characterized by:": "A magnitude curve slope of -40 dB/decade at high frequencies.",
    "In a Bode plot, the effect of adding a real zero at s = -z to a system is:": "The magnitude curve has a slope of +20 dB/decade at low frequencies.",
    "True or False: A system with multiple poles has a Bode plot with multiple corner frequencies.": "True.",
    "True or False: In a Bode plot, the asymptotic slope of the magnitude curve for an integrator is +20 dB/decade at low frequencies.": "False.",
    "True or False: Bode plots are a graphical representation of the frequency response of a system.": "True.",
    "Which statement regarding the Routh array is correct?": "The first element of each row is the coefficient of the highest power of the characteristic equation.",
    "What does it mean if there are any negative elements in the first column of the Routh array?": "System is unstable.",
    "What limitation of the Routh-Hurwitz criterion becomes more pronounced as the system order increases?": "Computational complexity.",
    "What happens if the system has a pole on the imaginary axis according to the Routh-Hurwitz criterion?": "The system is marginally stable.",
    "In the root locus method, what does the number of branches of the root locus correspond to?": "Both (a) and (c).",
    "What does the angle of departure represent in root locus analysis?": "The angle between the root locus branches and the real axis as they depart from complex poles.",
    "Breakaway points in the root locus plot indicate the locations where the system becomes unstable.": "False.",
    "If the root locus plot shows that a pole lies on the imaginary axis, what can be said about the system's stability?": "The system is marginally stable.",
    "Which of the following statements is true regarding root locus analysis?": "It can only be applied to linear time-invariant systems.",
    "The root locus plot shows the path of the system's poles as a system parameter changes.": "True.",
    "The Routh-Hurwitz criterion is used to calculate the steady-state error of a system.": "False.",
    "In a root locus plot, what does a breakaway or break-in point represent?": "The point where two branches of the root locus meet.",
    "What does the term 'root locus' refer to in control systems?": "The set of all possible values of the roots of the characteristic equation as a parameter varies.",
    "How does the location of the dominant poles of a system affect the root locus?": "It influences the shape and orientation of the root locus.",
    "The angle of departure in root locus analysis is measured counterclockwise from the positive real axis.": "True.",
    "What is the significance of asymptotes in a root locus plot?": "They indicate the direction in which the root locus approaches infinity.",
    "The root locus plot shows the path of the system's poles as a system parameter changes.": "True.",
    "The Routh-Hurwitz criterion is used to calculate the steady-state error of a system.": "False.",
    "In a root locus plot, what does a breakaway or break-in point represent?": "The point where two branches of the root locus meet.",
    "What does the term 'root locus' refer to in control systems?": "The set of all possible values of the roots of the characteristic equation as a parameter varies.",
    "How does the location of the dominant poles of a system affect the root locus?": "It influences the shape and orientation of the root locus.",
    "The angle of departure in root locus analysis is measured counterclockwise from the positive real axis.": "True.",
    "What is the significance of asymptotes in a root locus plot?": "They indicate the direction in which the root locus approaches infinity.",
    "All points on the root locus correspond to stable closed-loop poles.": "False.",
    "In the Routh-Hurwitz stability criterion, what does a sign change in the first row indicate?": "Presence of roots in the right half-plane.",
    "Which of the following is a limitation of the Routh-Hurwitz criterion?": "All other options.",
    "If a root locus plot shows that all poles lie in the left-half of the s-plane, what can be said about the system's stability?": "The system is stable.",
    "The Routh-Hurwitz criterion can be used to determine the stability of a system by:": "Checking the sign of the coefficients of the system's characteristic polynomial.",
    "A system is considered stable if its root locus crosses the imaginary axis in the right half-plane.": "False.",
    "What is the primary purpose of root locus analysis in control system design?": "To analyze the stability of the system.",
    "Which statement best describes the behavior of a root locus as the gain of a stable system increases?": "The roots move towards the left half-plane.",
    "What does overshoot in a step response indicate about a system?": "The system is underdamped.",
    "The values of K1 and K2 for the system in the figure that result in a damping factor of 0.7 and an undamped natural frequency of 4 rad/sec are:": "K1 = 16 and K2 = 0.225",
    "For the altitude control system of a spacecraft shown in the figure, calculate the damping coefficient for the case where T = 3, and K/J = 2/9.": "√2/2",
    "The characteristic equation of a system contains its closed-loop poles.": "Yes",
    "Which type of response does an overdamped system exhibit?": "Exponential",
    "The peak time of a system's step response is the time at which the output first exceeds its final value.": "False",
    "For an overdamped system, the poles are complex conjugates.": "False",
    "The settling time of a system is the time it takes for the response to decay to half of its maximum value.": "No",
    "The settling time of a second-order system is independent of its natural frequency ωn.": "False",
    "A closed-loop system with unity feedback has the following open-loop transfer function G(s). What are the values of K for which the steady-state error of the closed-loop system is less than 0.1 for a unit step input?":"K>18",
    "A control system with unity negative feedback has an open-loop transfer function G(s). Determine the percentage overshoot and the range of K values for which the settling time (2% criterion) is less than 1 second.":"𝑀𝑝 (%) = 4.3% 𝑎𝑛𝑑 𝐾 > 32",
    "Consider the altitude control system of satellites shown in figure (a). The output of this system exhibits undesirable constant oscillations. The system can be stabilized by using tachometric feedback as shown in figure (b). If K/J = 4, what value of Kh will result in a damping ratio of 0.6?": "0.6.",
    "For a first-order system, what is the time constant τ defined as?": "The time it takes for the output to reach 63.2% of its final value for a unit step input.",
    "What is the settling time of a system's step response?": "The time it takes for the output to reach 95% of its final value for a unit step input.",
    "What is the relationship between the natural frequency (ωn) and the settling time of a second-order system?": "As ωn increases, settling time decreases.",
    "The peak time (tp) of a second-order system is independent of the damping ratio (ζ).": "False.",
    "A higher damping ratio (ζ) results in a faster rise time for a second-order system.": "False.",
    "What is the relationship between the damping ratio (ζ) and the overshoot in a second-order system?": "As ζ increases, overshoot decreases.",
    "For the system in the figure, select K such that the steady-state error is equal to 1. Assume Km=10, Kb=0.05 for a unit ramp input.": "K = 0.051.",
    "Is it possible to meet both specifications simultaneously: tp=1.1 seconds and Mp=5%, for the system's response to a unit-step input, given the open-loop transfer function G(s) of a unity negative feedback system?":"NO",
    "We have the closed-loop transfer function C(s)/R(s). Determine the steadystate error for a unit step input.":"0",
    "Settling time is inversely proportional to the damping ratio (ζ) in a second-order system.": "True.",
    "The overshoot of a second-order system decreases as the damping ratio (ζ) increases.": "True.",
    "The settling time of a second-order system is the time taken for the response to reach 99% of the final value.": "No.",
    "What is the primary purpose of a control system?": "To maintain a desired output.",
    "Which of the following is an example of a closed-loop control system?": "Automatic temperature control in an air conditioner.",
    "In a feedback control system, the feedback signal is derived from the:": "Output.",
    "Which component of a control system directly influences the system output?" :"Actuator",
    "Which of the following is NOT a characteristic of an open-loop control system?":"Self-correcting",
    "In a control system, the purpose of the controller is to:":"Convert the error signal into a control signal",
    "A system is considered stable if:":"The output follows set-point over time",
    "What type of system is likely to be affected by external disturbances more significantly?":"Open-loop system",
    "The main disadvantage of a feedback control system is:":"Increased complexity",
    "The term 'servo mechanism' is commonly associated with:":"Closed-loop systems",
    "What is a key feature of a closed-loop control system?":"It improves accuracy by adjusting based on feedback.",
    "Which component in a feedback control system is responsible for reducing error to zero?":"Controller",
    "The transfer function of a system is defined as the ratio of the:":"Laplace transform of output to the Laplace transform of input with all initial conditions",
    "In a block diagram, the transfer function of the system is represented as:":"A block",
    "What does a summing point in a block diagram indicate?":"The addition or subtraction of signals",
    "In a block diagram, if the blocks are connected in series, the overall transfer function is:":"The product of individual transfer functions",
    "In block diagram reduction, which rule applies when two blocks are connected in parallel?":"Add their transfer functions",
    "Which block diagram representation is equivalent to G(s)/(1+G(s)H(s))?":"Forward path with negative feedback",
    "In a control system block diagram, what does a branch point indicate?":"The point where the signal splits into multiple paths",
    "State variables in a control system model are used to represent:":"The internal conditions of the system",
    "Which matrix in the state-space model represents the effect of the input on the state?":"B",
    "The state-space representation of a system includes:":"The state-space representation of a system includes:",
    "Obtain the state-space representation for the control system in the figure:":"The state-space representation 2:",
    "From the following sets of matrices, a valid state-space representation of a system is:":"Option 4",
    "Consider a linear time-invariant system described by a differential equation with the state variables defined. The corresponding state-space representation of this system is:":"Option 3",
    "The time constant τ of a first-order system is a measure of:":"The time required for the response to reach 63.2% of its final value",
    "For a second-order system, the damping ratio ζ determines:":"The type of response (overdamped, underdamped, critically damped)",
    "A second-order system is considered underdamped if:":"0<ζ<1",
    "For a critically damped system, the response:":"Reaches the steady state with no oscillation in the shortest possible time",
    "In a second-order system, if the damping ratio ζ=0, the system is:":"Critically damped",
    "The settling time ts for a second-order system is typically defined as the time required for the response to remain within:":"2% of its final value",
    "The natural frequency ωn of a second-order system is:":"The frequency of oscillation in the absence of damping",
    "In a second-order system, the peak time tp is the time required for:":"The first peak of the response to occur",
    "For an underdamped second-order system, the overshoot is dependent on:":"The damping ratio ",
    "The following figure shows the transient response of a system to a step input. Based on the information provided in the figure, the transfer function C(s)/R(s) of the second-order system that describes this dynamic is?":"First Option",
    "The steady-state error in a control system is:":"The difference between the desired and actual output as time approaches infinity",
    "For a type 0 system with a unit step input, the steady-state error is:":"Non-zero finite value",
    "A type 1 system has a transfer function with:":"One pole at the origin",
    "The steady-state error for a unit ramp input in a type 1 system is:":"Non-zero finite value",
    "For a type 2 system, the steady-state error for a unit step input is:":"ZERO",
    "In a control system, increasing the system gain will generally:":"Reduce the steady-state error",
    "The static error constant Kp is associated with the steady-state error for a:":"Step Input",
    "The steady-state error for a unit ramp input is inversely proportional to:":"Velocity error constant 𝐾v",
    "The final value theorem is used in control systems to determine:":"The steady-state value of the output",
    "The steady-state error for a unit parabolic input in a type 0 system is:":"Infinity",
    "For the control system shown, the steady-state error for a unit step input is equal to:":"Seguna opcion",
    "In state-space modeling, which matrix represents the direct influence of the input on the output?":"Matrix D",
    "The time constant of a system represents the time it takes for the system's response to reach 63.2% of its final value for a unit step input.":"True",
    "The state-space representation is not suitable for describing systems with multiple inputs and outputs.":"False",
    "What is the transfer function of the system represented by the state-space equations":"Third option",
    "The transfer function of a system can be directly obtained from its state- space representation.":"True",
    "Obtain the state-space representation for the control system in the figure":"The state representation 2",
    "What is the characteristic polynomial of a system with state matrix":"s²+3s +2",
    "All state variables must be directly observable from the output for a system to be observable.":"False",
    "The output matrix C in state-space modeling represents the mapping from the state variables to the outputs.":"True",
    "In a data center, maintaining optimal temperature is critical to prevent overheating of servers and equipment. The facility manager decides to implement a closed-loop":"Thermistor",
    "In a high-rise building, an elevator system is installed to transport people between":"Motor",
    "In a smart home automation system, light intensity control enhances energy":"Photocell",
    "An industrial assembly line relies on a robotic arm to perform precise tasks. To":"ServoMotor",
    "A CNC (Computer Numerical Control) machine is used for precision machining operations. To ensure accurate positioning of the cutting tool, the machine is":"Servomotor",
    "A manufacturing plant utilizes a conveyor belt system to transport products between workstations. To maintain consistent production speed, they employ a speed control":"Encoder",
    "An electric vehicle manufacturer wants to implement a speed control system to ensure safe and efficient operation. They decide to use a closed-loop control strategy":"Electric Motor",
    "A pilot wants to maintain a constant altitude during flight to ensure a smooth journey. What variable is typically controlled to achieve this in an aircraft autopilot system?":"Altitude",
    "In a wind turbine generator, the rotational speed of the turbine blades needs to be":"Anemometer",
    "In a power distribution network, voltage control is necessary to ensure stable and":"Capacitor Bank",
    "In an automotive assembly line, a robotic arm is employed to perform precise tasks":"Encoder",
    "In a chemical reactor used for polymerization, temperature control is crucial to":"PI Proportinal Integral",
    "A driver wants to maintain a constant speed while driving on the highway to improve":"Throttle position",
    "A homeowner wants to upgrade their heating, ventilation, and air conditioning":"Infrared motion sensor",
    "In a water treatment plant, a tank is used to store water. To prevent overflow or":"Solenoid valve",
    "An HVAC system is installed in a commercial building to regulate indoor temperature":"Thermostat setting",
    "A drone enthusiast wants to build a quadcopter capable of autonomous flight. One":"Barometric pressure sensor",
    "A homeowner installs a smart lighting system to adjust indoor lighting levels based":"Photodetector",
    "In a semiconductor manufacturing facility, a cleanroom environment is essential for":"Humidifier",
    "A commercial greenhouse owner needs to maintain optimal humidity levels to promote healthy plant growth. They plan to install a control system using humidity":"Solenoid Valve",
    "Which of the following is an example of a closed-loop control system?":"A thermostat regulating",
    "System dynamics refer to the system's ability to resist disturbances.":"False",
    "What information does the transfer function of an LTI system provide?":"Both",
    "What is the primary purpose of control in the context of control systems?":"To maintain",
    "What defines a closed-loop control system?":"It includes",
    "In the context of control systems, what are disturbances?":"Unwated",
    "What type of controller is designed to reduce the system's steady-state error?":"Proportional controller",
    "How is the system response defined in a control system?":"The regulated",
    "What is an Automatic Control System?":"Without human intervention",
    "What is the purpose of feedback in a control system?":"To provide",
    "Design specifications in control systems are typically expressed in terms of system performance requirements.":"Yes",
    "What does the term system dynamics refer to in a control system?":"The behavior",
    "In a linear time-invariant system, what property ensures that the system":"Homogenity",
    "What type of controller is designed to reduce the system's steady-state error?":"PI controller",
    "The system response is influenced only by the reference input.":"NO",
    "Find Ff(s)/R(s) for the system in the figure":"(G1*G2)/1+G1G2H2+G1G3H2",
    "What is the final value of a system described by the transfer function G(s) when the input is a unit impulse function?":"0",
    "For a system with transfer function H(s) and input u(t)=2-ramp(t), what is the inverse Laplace transform of the output?":"f(t)=2-2e-3t",



}   
    
# Clase para la superposición
class OverlayWindow(QMainWindow):
    def __init__(self, region, parent=None):
        super(OverlayWindow, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(10, 0, 1920, 1080)  # Ajusta a la resolución de tu pantalla
        self.region = region  # Región de monitoreo
        self.timer = QTimer()
        self.timer.timeout.connect(self.capture_and_process)
        self.timer.start(1000)  # Intervalo de 1 segundo

        self.text_label = QLabel(self)
        self.text_label.setStyleSheet("color: grey; font-size: 15px;")
        self.text_label.setGeometry(600, 700, 600, 100)  # Posición y tamaño del texto



    def paintEvent(self, event):
        # Dibuja el rectángulo verde sobre la pantalla
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(0,0,0,0))
        painter.setBrush(QColor(0, 0,0,0))
        x, y, w, h = self.region
        painter.drawRect(QRect(x, y, w, h))

    def capture_and_process(self):
        # Captura y procesa la región definida
        x, y, w, h = self.region
        screenshot = pyautogui.screenshot(region=(x, y, w, h))
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        text = pytesseract.image_to_string(screenshot, lang='eng+spa')

        # Procesa el texto extraído
        processed_text = " ".join(text.splitlines()).strip()  # Unifica líneas en un solo bloque
        processed_text = " ".join(processed_text.split())  # Elimina espacios extra

        
        # Busca frases clave
        for key, response in keywords.items():
            normalized_key = " ".join(key.splitlines()).strip()  # Normaliza clave
            normalized_key = " ".join(normalized_key.split())  # Elimina espacios extra

            if normalized_key.lower() in processed_text.lower():
                self.text_label.setText(f"Frase detectada:  {response}")
                return
        self.text_label.setText("  ")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    region = (270, 200, 850, 100)  # (x, y, ancho, alto), ajusta según tu pantalla
    overlay = OverlayWindow(region)
    overlay.show()
    sys.exit(app.exec_())
