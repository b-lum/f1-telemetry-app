import socket
from f1_2020_telemetry.packets import unpack_udp_packet
import random

last_fake = {'speed': 150, 'throttle': 0.5, 'brake': 0.1}

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('0.0.0.0', 20777))
udp_socket.settimeout(0.05)  # Timeout after 50ms


def get_next_packet():
    try:
        data, _ = udp_socket.recvfrom(2048)
        packet = unpack_udp_packet(data)
        return packet
    except socket.timeout:
        return None



def get_latest_telemetry() :
    try:
        data, _ = udp_socket.recvfrom(2048)
        packet = unpack_udp_packet(data)
        
        if hasattr(packet, 'carTelemetryData'):
            player_index = packet.header.playerCarIndex
            car = packet.carTelemetryData[player_index]
            return {
                'speed': car.speed,
                'throttle': car.throttle,
                'brake': car.brake
            }

    except socket.timeout:
        # No packet arrived in time, send dummy data
        return get_fake_telemetry()
    except Exception as e:
        print(f"Error in telemetry: {e}")
        return get_fake_telemetry()
    

def get_fake_telemetry() :
    for k in last_fake:
        # For 'speed', add a random change between -5 and 5
        # For 'throttle' and 'brake', smaller changes between -0.05 and 0.05
        change = random.uniform(-5, 5) if k == 'speed' else random.uniform(-0.05, 0.05)
        
        # Update last_fake value and clamp to allowed range
        max_val = 400 if k == 'speed' else 1
        new_val = last_fake[k] + change
        last_fake[k] = max(0, min(max_val, new_val))
    
    # Return a copy so external code can’t mutate internal state accidentally
    return dict(last_fake)

#def get_session_id():
    try:
        data, _ = udp_socket.recvfrom(2048)
        packet = unpack_udp_packet(data)

        if hasattr(packet, 'header') and hasattr(packet.header, 'sessionUID'):
            return packet.header.sessionUID
    except socket.timeout:
        return get_fake_telemetry()
    except Exception as e:
        print(f"Error in telemetry: {e}")
        return get_fake_telemetry()
    


