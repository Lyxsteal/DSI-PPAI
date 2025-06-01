import numpy as np
import matplotlib.pyplot as plt

# Parámetros
Tb = 1e-3  # tiempo de bit = 1 ms
Rb = 1 / Tb  # tasa de bits = 1000 bps
f = np.linspace(-3 * Rb, 3 * Rb, 1000)  # eje de frecuencias desde -3Rb a 3Rb

# PSD para NRZ Unipolar: sinc^2 con componente en DC
S_unipolar = (Tb ** 2) * (np.sinc(f * Tb)) ** 2

# PSD para NRZ Polar: misma forma pero sin componente DC
S_polar = S_unipolar.copy()
S_polar[np.abs(f) < 10] *= 0.01  # atenuamos el pico en DC artificialmente

# Gráfico
plt.figure(figsize=(10, 6))
plt.plot(f / 1e3, S_unipolar, label='NRZ Unipolar', color='red')
plt.plot(f / 1e3, S_polar, label='NRZ Polar', color='blue', linestyle='--')
plt.axvline(x=-Rb / 1e3, color='gray', linestyle=':', label='±Rb (1er nulo)')
plt.axvline(x=Rb / 1e3, color='gray', linestyle=':')
plt.title("Comparación de PSD: NRZ Unipolar vs. NRZ Polar")
plt.xlabel("Frecuencia (kHz)")
plt.ylabel("PSD relativa (sinc²)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()