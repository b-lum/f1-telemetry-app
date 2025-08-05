import socket
from f1_2020_telemetry.packets import unpack_udp_packet

# UDP socket bound to F1 2020 telemetry port
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(("", 20777))
udp_socket.settimeout(0.5)

def get_latest_telemetry():
    try:
        packet_data, _ = udp_socket.recvfrom(2048)
        packet = unpack_udp_packet(packet_data)

        if hasattr(packet, "header") and hasattr(packet.header, "playerCarIndex"):
            player_index = packet.header.playerCarIndex
            if hasattr(packet, "carTelemetryData"):
                telemetry = packet.carTelemetryData[player_index]
                return {
                    "speed": telemetry.speed,
                    "throttle": telemetry.throttle,
                    "brake": telemetry.brake
                }

    except socket.timeout:
        return None
