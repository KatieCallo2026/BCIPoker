import socket

def stream_from_windows_tcp():
    HOST = "172.28.112.1" # ip route | grep default
    PORT = 5001  # Make sure this matches your Windows script

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print(f"Connected to GSR stream at {HOST}:{PORT}")

            while True:
                data = s.recv(1024).decode().strip()
                if data:
                    print(f"GSR Value: {data}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    stream_from_windows_tcp()
