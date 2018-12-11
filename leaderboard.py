import pandas as pd

try:
    score = pd.read_csv('scores.csv')
except:
    score = pd.DataFrame(columns=['id', 'score', 'death'])
    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    host = '127.0.0.1'
    port = 9999
    
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    connection, address = server_socket.accept()
    
    while True:
        res = client_socket.recv(100).decode('ascii')
        
        if res == '':
            break
        else:
            res = [int(item) for item in res.strip().split(' ')]