import queue
import socket
import threading

hostname = input('Input hostname: ')
start, end = int(input('Input start port: ')), int(input('Input end port: '))

def port_checker(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(3)
        try:
            sock.connect((hostname, port))
        except ConnectionRefusedError:
            result_queue.put((port, 'TCP', False))
            return
        except socket.timeout:
            result_queue.put((port, 'TCP', True))
            return
        except Exception as e:
            result_queue.put((port, 'TCP', False))
            return
    # result_queue.put((port, 'TCP', True))

def udp_ports(port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
        udp_sock.settimeout(3)
        try:
            udp_sock.connect((hostname, port))
            udp_sock.send(b'Hi')
            udp_sock.send(b'Hi')
            udp_sock.send(b'Hi')
            udp_sock.send(b'Hi')
            udp_sock.send(b'Hi')
            print(udp_sock.recv(1024))
        except ConnectionResetError:
            result_queue.put((port, 'UDP', False))
            return
        except socket.timeout:
            result_queue.put((port, 'UDP', True))
            return
        except Exception as e:
            result_queue.put((port, 'UDP', False))
            return
    result_queue.put((port, 'UDP', True))

# mc.hypixel.net
ports_queue = queue.Queue()
result_queue = queue.Queue()

for i in range(start, end + 1):
    ports_queue.put(i)

for _ in range(start, int((end + 1 + start) / 2)):
    i = ports_queue.get()
    j = ports_queue.get()

    threadU1 = threading.Thread(target=udp_ports, args=(i,))
    threadU2 = threading.Thread(target=udp_ports, args=(j,))
    thread1 = threading.Thread(target=port_checker, args=(i,))
    thread2 = threading.Thread(target=port_checker, args=(j,))

    threadU1.start()
    threadU2.start()
    thread1.start()
    thread2.start()

    threadU1.join()
    threadU2.join()
    thread1.join()
    thread2.join()

    for _ in range(4):
        res = result_queue.get()
        print(res[1], ' ', res[0], ' : ', res[2])

if (end - start + 1) % 2 != 0:
    i = ports_queue.get()

    thread1 = threading.Thread(target=port_checker, args=(i,))
    threadU1 = threading.Thread(target=udp_ports, args=(i,))

    thread1.start()
    threadU1.start()
    thread1.join()
    threadU1.join()  # cs.usu.edu.ru 10 122
    for _ in range(2):
        res = result_queue.get()
        print(res[1], ' ', res[0], ' : ', res[2])
