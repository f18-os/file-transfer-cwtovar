#! /usr/bin/env python3
import sys
sys.path.append("../lib")       # for params

import os, socket, params


switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "fileServer"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

while True:
    sock, addr = lsock.accept()

    from framedSock import framedSend, framedReceive

    if not os.fork():
        print("new child process handling connection from", addr)
        while True:
            payload = framedReceive(sock, debug)
            if "put" in payload.decode() && len(payload.decode().split()):   
                cmd=payload.split()
            # get the current script path.
                subdir = "serverDir"
                newFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), subdir, cmd[1])
            # create an empty file.
            try:
                with open(newFile, "a") as copyFile:
                    while True:
                        payload = framedReceive(sock, debug)
                        if not payload:
                            if debug: print("child exiting")
                            sys.exit(0)
                        copyFile.write(payload.decode())
                
            except IOError:
                print( "Wrong path provided")
            #if debug: print("rec'd: ", payload)
            #framedSend(sock, payload, debug)
