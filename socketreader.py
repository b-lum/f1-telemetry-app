import socket
from f1_2020_telemetry.packets import unpack_udp_packet
from PyQt5.QtCore import QThread, pyqtSignal
from telemetry_objects.session import Session


class SocketReader(QThread):
    new_data = pyqtSignal(float, float, float)

    def __init__(self):
        super().__init__()
        self.stop_flag = False

    def run(self):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind(("", 20777))
        udp_socket.settimeout(1.0)

        try:
            packetdata,  = udp_socket.recvfrom(2048)
            packet = unpack_udp_packet(packet_data)

            if hasattr(packet, "header") and hasattr(packet.header, "sessionUID"):
                session_uid = packet.header.sessionUID
                print(f"Session UID: {session_uid}")
                self.session = Session(session_uid)  # pass UID if needed
        except socket.timeout :
            pass


        while not self.stop_flag:
            try:
                packet_data, _ = udp_socket.recvfrom(2048)
                packet = unpack_udp_packet(packet_data)

                if hasattr(packet, "header") and hasattr(packet.header, "playerCarIndex"):
                    player_index = packet.header.playerCarIndex

                    if hasattr(packet, "carTelemetryData"):
                        telemetry = packet.carTelemetryData[player_index]

                        speed = telemetry.speed  # speed in km/hsocketreader.py
                        throttle = telemetry.throttle # throttle ratio (0.0 - 1.0)
                        brake = telemetry.brake # brake ratio (0.0 - 1.0)
                        self.new_data.emit(speed, throttle, brake)

                        print(f"Speed: {speed} km/h")
                        print(f"Throttle: {telemetry.throttle}")
                        print(f"Brake: {telemetry.brake}")
                        print(f"Gear: {telemetry.gear}")
                        print(f"RPM: {telemetry.engineRPM}")
                        print("------")

            except socket.timeout:
                continue

    def stop(self):
        self.stop_flag = True
        self.quit()
        self.wait()

