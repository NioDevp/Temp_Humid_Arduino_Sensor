import serial
import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def read_data_from_arduino(ser):
    data = ser.readline().decode('utf-8').rstrip()
    print("Datos recibidos desde Arduino:", data)

    if data:
        return data.split()
    else:
        return None

def animate(i, temperature_data, humidity_data, heat_index_data, ser):
    data = read_data_from_arduino(ser)
    if data is not None and len(data) == 3:
        try:
            humidity_data.append(float(data[0]))
            temperature_data.append(float(data[1]))
            heat_index_data.append(float(data[2]))
        except ValueError:
            print("Error al convertir los datos a números flotantes:", data)
    else:
        print("Datos no válidos recibidos desde el Arduino:", data)

    # Limpiar la gráfica y volver a dibujar los datos
    plt.cla()

    plt.plot(temperature_data, label='Temperatura (°C)', marker='o')
    plt.plot(humidity_data, label='Humedad (%)', marker='o')
    plt.plot(heat_index_data, label='Índice de Calor', marker='o')

    plt.xlabel('Tiempo (muestras)')
    plt.ylabel('Valores')
    plt.title('Datos de Temperatura, Humedad e Índice de Calor')
    plt.legend()
    plt.grid(True)

def save_data_to_excel(temperature_data, humidity_data, heat_index_data):
    data = {
        'Tiempo (muestras)': list(range(len(temperature_data))),
        'Temperatura (°C)': temperature_data,
        'Humedad (%)': humidity_data,
        'Índice de Calor': heat_index_data
    }

    df = pd.DataFrame(data)

    # Guardar los datos en un archivo Excel
    df.to_excel('datos_registrados.xlsx', index=False)

if __name__ == '__main__':
    try:
        ser = serial.Serial('COM3', 9600, timeout=1)
        print("Conectado al puerto COM3")
        time.sleep(2)  # Esperar a que se estabilice la conexión

        temperature_data = []
        humidity_data = []
        heat_index_data = []

        num_samples = 100  # Puedes ajustar este número según la cantidad de muestras que desees graficar

        fig = plt.figure()
        ani = FuncAnimation(fig, animate, fargs=(temperature_data, humidity_data, heat_index_data, ser), interval=1000)
        plt.show()

        save_data_to_excel(temperature_data, humidity_data, heat_index_data)
    
    except serial.SerialException:
        print("Error: No se pudo establecer conexión con el puerto COM3.")
