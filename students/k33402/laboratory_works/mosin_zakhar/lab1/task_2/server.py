import socket
import signal

enc = "utf-8"
port = 2448



def solve_quadratic_equation(a, b, c):
    if a == 0 or a is None:
        return None, None

    if b == 0 or b is None:
        return None, None

    if c == 0 or c is None:
        return 0, 0

    d = b ** 2 - 4 * a * c

    if d < 0:
        return None, None

    x1 = (-b + d ** 0.5) / (2 * a)
    x2 = (-b - d ** 0.5) / (2 * a)

    return x1, x2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("localhost", port))
s.listen(1)
signal.signal(signal.SIGINT, signal.SIG_DFL)

print("Waiting for a connection...")
while True:
    try:
        client_socket, client_address = s.accept()
        print("Accepted connection from: ", client_address)

        data = client_socket.recv(1024)
        print("Received data from client: ", data.decode(enc))

        a, b, c = map(int, data.decode(enc).split())

        x1, x2 = solve_quadratic_equation(a, b, c)

        if x1 is None:
            response = "No roots"

        else:
            response = "x1 = {}, x2 = {}".format(x1, x2)

        client_socket.send(response.encode(enc))
        print("Sent data to client: ", response)

        client_socket.close()

    except KeyboardInterrupt:
        print("Server terminated by user.")
        break

s.close()