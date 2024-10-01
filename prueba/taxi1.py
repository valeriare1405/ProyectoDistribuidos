import zmq
import time
import random
import json  

ip_central='10.43.100.106'

def mover_taxi(id_taxi, grid_size, velocidad, max_servicios):
    context = zmq.Context()

    # Publisher para enviar posiciones
    pub_socket = context.socket(zmq.PUB)
    pub_socket.connect(f"tcp://{ip_central}:5555")  # El servidor va a bindear a este puerto

    # REP para recibir servicios
    rep_socket = context.socket(zmq.REP)
    rep_socket.bind(f"tcp://*:556{id_taxi}")  # Cada taxi tiene su propio puerto
    time.sleep(1)  # Asegurar que el socket esté listo con un pequeño sleep

    x, y = random.randint(0, grid_size[0] - 1), random.randint(0, grid_size[1] - 1)
    servicios_realizados = 0

    while servicios_realizados < max_servicios:
        # Enviar la posición actual en formato JSON
        taxi_posicion = {"x": x, "y": y}
        mensaje = json.dumps(taxi_posicion)
        pub_socket.send_string(f"Taxi {id_taxi} {mensaje}")
        print(f"Enviado: Taxi {id_taxi} {mensaje}")

        poller = zmq.Poller()
        poller.register(rep_socket, zmq.POLLIN)
        socks = dict(poller.poll(1000))  # Esperar hasta 1 segundo

        if socks.get(rep_socket) == zmq.POLLIN:
            print("Datos disponibles para recibir en el taxi.")
            servicio = rep_socket.recv_string()
            print(f"Recibido servicio: {servicio}")
            rep_socket.send_string(f"Taxi {id_taxi} aceptando servicio")
            servicios_realizados += 1
        else:
            print("No se ha recibido ningún servicio en este ciclo.")

        x, y = mover_taxi_en_grilla(x, y, grid_size, velocidad)
        time.sleep(2)  # Cambiar a 15 segundos para 30 minutos simulados

    pub_socket.close()
    rep_socket.close()
    context.term()

def mover_taxi_en_grilla(x, y, grid_size, velocidad):
    movimiento = random.choice(['vertical', 'horizontal'])
    if movimiento == 'vertical':
        x = max(0, min(x + velocidad, grid_size[0] - 1))
    else:
        y = max(0, min(y + velocidad, grid_size[1] - 1))
    return x, y

if __name__ == "__main__":
    id_taxi = 1  # Identificador del taxi
    grid_size = (10, 10)  # Tamaño de la cuadrícula NxM
    velocidad = 2  # Velocidad del taxi (en km/h)
    max_servicios = 3  # Número máximo de servicios
    mover_taxi(id_taxi, grid_size, velocidad, max_servicios)
