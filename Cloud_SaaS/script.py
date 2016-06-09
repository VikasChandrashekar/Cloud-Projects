'''
Created on Jun 9, 2016

@author: vicky
'''

from Crypto import Random
from Crypto.Cipher import AES
import hashlib
from keystoneclient import client
import os, random, struct
import re 
import swiftclient


auth_url="https://identity.open.softlayer.com/v3" 
project= "object_storage_7f1fb404_b6d8_4a53_951f_7fe58a3509d9"
projectId= "d16dcae48a674c2b8c90c9cb6073a716"
region= "dallas"


IBM_Objectstorage_Connection = swiftclient.Connection(key=password,user=username,authurl=auth_url,auth_version='3',
os_options={"project_id": projectId,"user_id": userId,"region_name": region})
x =  IBM_Objectstorage_Connection.get_account()[1]

#Encryption
def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_ECB, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))

#Decryption
def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_ECB, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)

def put(filename):
    for container in IBM_Objectstorage_Connection.get_account()[1]:
        for data in IBM_Objectstorage_Connection.get_container(container['name'])[1]:
            if(filename == data['name']):
                print "File already exists" 
            
    size = os.path.getsize(filename)
    if(size<=1048576):
        with open(filename,'r') as ex_file:
            IBM_Objectstorage_Connection.put_object('Cloud assignment 1',filename,ex_file.read(),content_type='text')
        print ("File list:")
        for container in IBM_Objectstorage_Connection.get_account()[1]:
            for data in IBM_Objectstorage_Connection.get_container(container['name'])[1]:
                    print '-> {0}t size: {1}t date: {2}'.format(data['name'], data['bytes'], data['last_modified'])
    else:
        print("File too large")

def delete(del_file_name):
    IBM_Objectstorage_Connection.delete_object('Cloud assignment 1', del_file_name)
    print "nObject %s deleted successfully." % del_file_name  

    print ("Filb.e list after deletion:")
    for container in IBM_Objectstorage_Connection.get_account()[1]:
        for data in IBM_Objectstorage_Connection.get_container(container['name'])[1]:
            print '-> {0}t size: {1}t date: {2}'.format(data['name'], data['bytes'], data['last_modified'])  

def download_file_to_local(save_file_name):
    obj = IBM_Objectstorage_Connection.get_object('Cloud assignment 1', save_file_name)
    with open(save_file_name, 'w') as my_example:
        my_example.write(obj[1])
    print "nObject %s downloaded successfully." % save_file_name
    print ("Done")

term=1
#keygen for encryption, decryption.
while(term):
    number=raw_input("1. Upload a file \n2.Delete a file \n3.Download a file\n4.Exit the program")
    print(number+" ssss")
    if(number=="1"):
        filename=raw_input("\nEnter a filename to upload")
        encrypt_file('aSSSSSaSSaaSSSaS', filename)
        put(filename+".enc")
        
    if(number=="2"):
        filename=raw_input("\nEnter a filename to delete")
        delete(filename)
    if(number=="3"):
        filename=raw_input("\nEnter a filename to download")
        download_file_to_local(filename)
        break
    if(number=="4"):
        break;