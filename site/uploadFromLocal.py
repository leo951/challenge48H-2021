# import mysql.connector
# from mysql.connector.constants import ClientFlag
# import base64
# import io
# import os
# from io import StringIO
# import PIL.Image

# config = {
#     'user': 'root',
#     'password': 'challenge48h',
#     'host': '104.197.252.23',
#     'client_flags': [ClientFlag.SSL],
#     'ssl_ca': 'ssl/server-ca.pem',
#     'ssl_cert': 'ssl/client-cert.pem',
#     'ssl_key': 'ssl/client-key.pem',
#     'database': 'challenge'
# }

# db = mysql.connector.connect(**config)
# mycursor=db.cursor()

# mycursor.execute("drop table img")
# mycursor.execute("create table img(images longblob not null);")

# def pushB64(path):
#     with open(path, 'rb') as f:
#         photo = f.read()
#     encodestring = base64.b64encode(photo)

#     sql = "insert into picture (image) values (%s)"
#     mycursor.execute(sql,(encodestring,))
#     db.commit()

# def get():
#     mycursor.execute("select * from img")
#     data = mycursor.fetchall()
#     data1=base64.b64decode(data[0][0])
#     img=PIL.Image.open( io.BytesIO(data1) )
#     img.show()

# for dir in os.listdir('pic'):
#     for file in os.listdir('pic/'+dir):
#         print("upload :" + file)
#         pushB64('pic/'+dir+'/'+file)

# db.close()

import requests

def pushAPI(path):
    myobj = {'path': path}
    x = requests.post('https://localhost.com:5000/create', data = myobj)

for dir in os.listdir('pic'):
    for file in os.listdir('pic/'+dir):
        print("upload :" + file)
        pushAPI(file)
