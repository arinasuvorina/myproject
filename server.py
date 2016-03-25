import socket 

sock = socket.socket() 
sock.bind(('localhost',8000)) 
sock.listen(10) 
 
while True: 
    conn, addr = sock.accept() 
    data = conn.recv(1024) 
    dataAsStr = data.decode()
    dataFirstStr = dataAsStr.split('\n')[0]
    path = dataFirstStr.split(' ')[1]
    path = path[1:] 
    if path == "": 
        path = "index.html" 
    file = open(path, 'rb') 
    conn.send(file.read()) 
    file.close() 
    conn.close()
    
sock.close() 
