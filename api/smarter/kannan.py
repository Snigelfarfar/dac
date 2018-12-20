#!/usr/bin/python3.5
import sys
import socket
import json
import time

#method names to validate
API_METHOD_BREW = "brew"
API_METHOD_RESET = "reset"

#IP address of the smarter coffee machine on your network
TCP_IP = '192.168.1.244'
TCP_PORT = 2081
BUFFER_SIZE = 10

#default method to call
api_method = sys.argv[1]

def connect_and_execute(method, address):

        if api_method == API_METHOD_BREW:
                message_to_send = "7"
        elif api_method == API_METHOD_RESET:
                message_to_send = "\x10"
        
        #make connection to machine and send message
        try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((address, TCP_PORT))
                s.send(message_to_send)
                data = s.recv(BUFFER_SIZE)
                s.close()
        except Exception as msg:
                print('Failed to create socket. Error code: {} , Message: {} '.format( str(msg[0]), msg[1]))
                #sys.exit();
        
        #convert response from machine to unicode
        return_code = unicode(data)
        
        #set default values to ouput
        success=0
        message=""
        
        #find out what the machine response means
        if return_code =="\x03\x00~":
                success=1
                message="brewing"
        elif return_code=="\x03\x01~":
                message="already brewing"
        elif return_code=="\x03\x05~":
                message="no carafe"
        elif return_code=="\x03\x06~":
                message="no water"
        elif return_code=="\x03i~":
                success=1
                message="reset"
        else:
                message="check machine"
        
        #ouput JSON to whatever called this script
        code = repr(data)
        print(json.dumps({'success': success,'message':message,'return_code':code}))
        
        #quit()
if __name__ == '__main__':
        
        for i in range(2,255):
            time.sleep(0.5)
            IP = "192.168.1.{}".format(i)
            print(IP)
            try:
                    connect_and_execute(API_METHOD_BREW, IP)
            except Exception as e:
                    print(e)
            finally:
                    pass
        quit()
        sys.exit()
