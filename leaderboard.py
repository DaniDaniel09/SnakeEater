"""
:author: Daniel Zanón Lopez/DaniDaniel09
"""

# `import pandas as pd` is importing the pandas library and giving it an alias of `pd` to make it
# easier to reference in the code.
import pandas as pd

# This code is attempting to read a CSV file named 'scores.csv' using the pandas library. If the file
# is successfully read, the resulting data is stored in the `score` variable. If an error occurs while
# attempting to read the file (e.g. the file does not exist), an empty pandas DataFrame with columns
# 'id', 'score', and 'death' is created and stored in the `score` variable.
try:
    score = pd.read_csv('scores.csv')
except:
    score = pd.DataFrame(columns=['id', 'score', 'death'])
    
# This code sets up a server socket using the Python `socket` module, binds it to a specific IP
# address and port number, and listens for incoming connections. Once a connection is established, it
# enters a loop to receive data from the client socket and process it. The received data is decoded
# from ASCII format, split into a list of integers, and stored in the `res` variable.
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