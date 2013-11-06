# -*- coding: utf-8 -*-
import qrcode

members = []

#load data from csv
f = open("lista-socios.csv")
rawList = f.readlines()[1:]

for n in rawList:
    s = list(n.split("\t"))
    #print s
    if len(s) > 3:
        members.append((s[0],s[3],s[2]))

#create QR codes
i = 0
while i < len(members):
    numero, apellido, nombre = members[i]
    numero = '%(numero)04d'%{"numero":int(numero)}
    apellido = apellido.strip(" ")
    nombre = nombre.strip(" ")

    print "[" + str(len(members) - i - 1) + " restantes] (" + numero + "," + apellido + "," + nombre + ")"

    qr = qrcode.QRCode(
        #version=7,
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    #qr.add_data('BEGIN:VCARD\nVERSION:3.0\nN:' + apellido + ';'+ nombre +';\nFN:' + nombre + ' ' + apellido + '\nNOTE:' + numero + '\nEND:VCARD')
    qr.add_data(numero + ';' + apellido + ';'+ nombre)
    qr.make(fit=False)

    img = qr.make_image()
    img.save("qr," + numero + "," + apellido + "," + nombre + ".png")

    i += 1
