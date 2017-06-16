#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from bs4 import BeautifulSoup
from requests import get
import Pyro4
from Tkinter import *
import ttk
import Tkinter as tk
import tkMessageBox
from PIL import ImageTk
from functools import partial
import sys, string, urllib
from urllib2 import urlopen
import re
import MySQLdb
import json
import ast
from functools import partial

@Pyro4.expose
class Cliente(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.initUI()

    def initUI(self):

         b = tk.Button()
         image = ImageTk.PhotoImage(file="login.png")
         b.config(image=image, bd=0)
         b.image = image
         b.pack()

         login = Frame(bd=4, relief='ridge')
         login.pack()

         Label(login, text="E-mail:", width=10, height=2, font=('MS', 10, 'bold')).pack()
         email = Entry(login)
         email.pack()

         Label(login, text="Password:", width=10, height=2, font=('MS', 10, 'bold')).pack()
         clave = Entry(login, show="*")
         clave.pack()


         f0 = tk.LabelFrame(login, width=100, height=100, relief='flat', borderwidth=4)
         f0.pack(padx=5, pady=5, side='left')
         Button(f0, text="Login", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'), activebackground="turquoise3", width=10, height=2, command=lambda: self.ingresar(email, clave)).pack()

         f1 = tk.LabelFrame(login, width=100, height=100, relief='flat', borderwidth=4)
         f1.pack(padx=5, pady=5, side='left')
         Button(f1, text="Registrarse", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'), activebackground="turquoise3", width=10, height=2, command=lambda: self.registrar_usuario).pack()


    def registrar_usuario(self):

        register = Toplevel()

        Label(register, text="Nombre Completo:").pack()
        nombre = Entry(register)
        nombre.pack()

        Label(register, text="Apellidos:").pack()
        apellido = Entry(register)
        apellido.pack()

        Label(register, text="Password:").pack()
        clave = Entry(register, show="*")
        clave.pack()

        Label(register, text="E-mail:").pack()
        email = Entry(register)
        email.pack()

        Button(register, text="Crear", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=10, height=2, command=lambda: self.usuario_tipo(nombre, apellido, clave, email)).pack()


    def ingresar(self, email, clave):

        mail = email.get()
        pasw = clave.get()

        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")# conexion servidor

        tipo = ingreso.login_usuario(mail, pasw)

        if (tipo==0):
            tkMessageBox.showerror(title="Ingresar", message="Usuario o contraseña incorrecta")
        if (tipo==1):
            self.master.destroy()
            self.usuario_cliente()


    def usuario_tipo(self, nombre, apellido, clave, email):

        id = 1
        nom = nombre.get()
        ape = apellido.get()
        cl = clave.get()
        em = email.get()
        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor

        resul = ingreso.login_register(id, nom, ape, cl, em)


    def usuario_cliente(self):

        ventana_cliente = Tk()

        a = tk.Button(ventana_cliente)
        image = ImageTk.PhotoImage(file="listar.png")
        a.config(image=image, command=self.listar, bd=0)
        a.image = image
        a.pack()

        b = tk.Button(ventana_cliente)
        image = ImageTk.PhotoImage(file="eliminar.png")
        b.config(image=image, command=self.veliminar, bd=0)
        b.image = image
        b.pack()

        c = tk.Button(ventana_cliente)
        image = ImageTk.PhotoImage(file="agregar.png")
        c.config(image=image, command=self.vinsertar, bd=0)
        c.image = image
        c.pack()

        d = tk.Button(ventana_cliente)
        image = ImageTk.PhotoImage(file="seo.png")
        d.config(image=image, command=self.vseo, bd=0)
        d.image = image
        d.pack()



    def listar(self):

        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor

        result = ingreso.pagina_listar()

        ventanalistar = Tk()
        ventanalistar.geometry("650x450+400+400")

        Title = Label(ventanalistar, text='Id', bg='DodgerBlue4', fg='white', width=5, font=('MS', 10, 'bold'))
        Title.grid(row=0, column=0, columnspan=1, rowspan=1)
        Title1 = Label(ventanalistar, text='Nombre', bg='DodgerBlue4', fg='white', width=30,
                       font=('MS', 10, 'bold'))
        Title1.grid(row=0, column=1, columnspan=1, rowspan=1)
        Title2 = Label(ventanalistar, text='Dominio', bg='DodgerBlue4', fg='white', width=30,
                       font=('MS', 10, 'bold'))
        Title2.grid(row=0, column=2, columnspan=1, rowspan=1)
        try:
            i = 1
            for registro in result:
                id_pagina = registro[0]
                nombre = registro[1]
                url = registro[2]
                # Imprimimos los resultados obtenidos

                Contenido = Label(ventanalistar, text="%d" % (id_pagina), bg='turquoise3', fg='white', width=5,
                                  font=('MS', 10, 'bold'))
                Contenido.grid(row="%d" % (i), column=0, columnspan=1, rowspan=1)

                Contenido1 = Label(ventanalistar, text="%s" % (registro[1]), bg='turquoise3', fg='white', width=30,
                                   font=('MS', 10, 'bold'))
                Contenido1.grid(row="%d" % (i), column=1, columnspan=1, rowspan=1)

                Contenido2 = Label(ventanalistar, text="%s" % (registro[2]), bg='turquoise3', fg='white', width=30,
                                   font=('MS', 10, 'bold'))
                Contenido2.grid(row="%d" % (i), column=2, columnspan=1, rowspan=1)
                i = i + 1

        except:
            print ("Error")


    def veliminar(self):

        ventana_eliminar = Tk()

        Label(ventana_eliminar, text="Ingrese el nombre de la pagina a eliminar :").pack()
        eliminar = Entry(ventana_eliminar)
        eliminar.pack()

        Button(ventana_eliminar, text="Borrar", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'), activebackground="turquoise3", width=10, height=2, command=lambda: self.eliminar_pag(eliminar)).pack()



    def eliminar_pag(self, eliminar):

        elim = eliminar.get()
        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor

        id = ingreso.pagina_eliminar(elim)

        if (id==0):
            tkMessageBox.showinfo(title="Info", message="la pagina se elimino con exito")

        else:
            tkMessageBox.showerror(title="Error", message="El registro no existe")


    def vinsertar(self):
        ventanaagregar = Tk()
        ventanaagregar.title("Agregar pagina web")

        ventanaagregar.geometry("340x140+500+550")

        Label(ventanaagregar, text="Nombre:", width=10, height=2, font=('MS', 10, 'bold')).grid(row=1, sticky=W)
        nombre = Entry(ventanaagregar)
        Label(ventanaagregar, text="Dominio:", width=10, height=2, font=('MS', 10, 'bold')).grid(row=2, sticky=W)
        dominio = Entry(ventanaagregar)
        nombre.grid(row=1, column=1)
        dominio.grid(row=2, column=1)

        Button(ventanaagregar, text="Crear", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=10, height=2, command=lambda: self.insertar_pag(nombre, dominio)).grid(row=3, column=1)

    def insertar_pag(self, nombre, dominio):

        grabar = 1

        nom = nombre.get()
        url = dominio.get()

        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor
        if nom == '' or url == '':

           grabar = 0

        if grabar == 1:
            result = ingreso.pagina_insertar(nom, url)

            if (result==0):
               tkMessageBox.showinfo(title="Info", message="Pagina creada con exito")

            else:
               tkMessageBox.showerror(title="Error", message="Error al crear la pagina")
        else:
            tkMessageBox.showinfo(title="Info", message="Todos los campos son obigatorios")


    def vseo(self):

        seo = Tk()

        Button(seo, text="Contar Palabras", bg="aquamarine", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2, command=self.contar_palabras).grid(row=1, column=1)
        Button(seo, text="Diccionario", bg="aquamarine1", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=1, column=2)
        Button(seo, text="Contar Imagenes", bg="aquamarine2", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2, command=self.contar_img).grid(row=1, column=3)

        Button(seo, text="Contar enlaces", bg="aquamarine3", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=1, column=4)
        Button(seo, text="Analizar Url", bg="aquamarine4", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=1, column=5)
        Button(seo, text="Analizar Palabras claves", bg="azure", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=2, column=1)
        Button(seo, text="Redes sociales", bg="azure1", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=2, column=2)
        Button(seo, text="Estructura del sitio", bg="azure2", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=2, column=3)
        Button(seo, text="Contenido No Apto", bg="azure3", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=2, column=4)
        Button(seo, text="Contenido Dudoso", bg="azure4", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=2, column=5)
        Button(seo, text="Malas practicas", bg="CadetBlue", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=3, column=1)
        Button(seo, text="Librerias Usadas", bg="CadetBlue1", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=3, column=2)
        Button(seo, text="Comprobar enlaces externos", bg="CadetBlue2", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=3, column=3)
        Button(seo, text="Más Puntuación", bg="CadetBlue3", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=3, column=4)

    def contar_palabras(self):

        ventana_contar = Tk()

        Label(ventana_contar, text="Ingrese el ID  de la pagina:").pack()
        contar = Entry(ventana_contar)
        contar.pack()

        print (contar)
        Button(ventana_contar, text="Enviar", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=10, height=2, command=lambda: self.contarp(contar)).pack()

    def contarp(self, contar):
        con = contar.get()

        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor

        result = ingreso.palabras_cont(con)

        print (result)

    def contar_img(self):

        ventana_img = Tk()

        Label(ventana_img, text="Ingrese el ID  de la pagina:").pack()
        contar = Entry(ventana_img)
        contar.pack()

        Button(ventana_img, text="Enviar", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=10, height=2, command=lambda: self.contarimg(contar)).pack()

    def contarimg(self, contar):

        con = contar.get()

        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor

        result = ingreso.contar_imagenes(con)

        print (result)


def main():
    ventana = Tk()
    app = Cliente(ventana)
    ventana.geometry("400x480+300+300")
    ventana.mainloop()

if __name__ == '__main__':
    main()
