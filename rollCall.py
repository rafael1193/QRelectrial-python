# -*- coding: utf-8 -*-

import zbar
import gtk
from sys import argv
import time
from datetime import date
import io
import codecs

asistanceList = []


def rollCall():
    try:
        f = io.open('lista-' + str(date.today()) + '.csv', 'rt')
        linea = f.readline()
        while linea != "":
            num, lastname, firstname = linea.split(',')
            asistanceList.append((num, lastname, firstname))
            linea = f.readline()
    except IOError:
        pass

    proc = zbar.Processor()
    proc.parse_config('enable')

    # initialize the Processor
    device = '/dev/video0'
    if len(argv) > 1:
        device = argv[1]
    proc.init(device)

    # setup a callback
    def my_handler(proc, image, closure):
        for symbol in image:
            if not symbol.count:
                # do something useful with results
                #print ('decoded', symbol.type, 'symbol', '"%s"' % symbol.data)
                #try:
                 logReadedCode(symbol.data)
                #except ValueError:
                    #print ("QR incorrecto")

    proc.set_data_handler(my_handler)

    # enable the preview window
    proc.visible = True

    # initiate scanning
    proc.active = True
    try:
        proc.user_wait()
    except zbar.WindowClosed:
        pass


def sanitice_input(string):
    '''
    Converts shift-jis bytes into unicode
    (because zbar sucks!)
    '''
    string = string.replace("ﾃｳ", "ó")
    return string

def logReadedCode(s):
    #load file
    try:
        f = io.open('lista-' + str(date.today()) + '.csv', 'ab')
    except Error:
        print Error
    print(s)
    s = sanitice_input(s)

    content = s.strip().split('\r\n')

    print content
    if len(content) is not 3:
        print content
        print ("error on " + str*content)
        raise ValueError

    number = content[0]
    lastname = content[1]
    firstname = content[2]

    # Check if person is in list, to not store duplicates
    inList = False
    for p in asistanceList:
        if p[0] == number and p[1] == lastname and p[2] == firstname:
            print ("Ya esta en la lista")
            inList = True
            break;
    if not inList:
        print('\a')
        f.write((number + ','))
        f.write((lastname + ','))
        f.write((firstname + '\n'))
        asistanceList.append((number, unicode(lastname), unicode(firstname)))
        print (asistanceList)

    f.close()
