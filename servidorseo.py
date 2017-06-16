#!/usr/bin/python
# -*- coding: utf-8 -*-


from __future__ import print_function
import Pyro4
from bs4 import BeautifulSoup
import bs4 as bs
from requests import get
import json
import MySQLdb
etiquetas_imagenes= list()
import re, string
import mysql.connector


@Pyro4.expose
class Servidor(object):

    @Pyro4.expose


    def conexionbd(self):
        HOST = 'localhost'  # '192.168.1.24' #base de datos remota
        USER = 'root'
        PASSWORD = ''
        DATABASE = 'paginadistri'
        conexion = (HOST, USER, PASSWORD, DATABASE)
        conn = MySQLdb.connect(*conexion)  # Conectar a la base de datos
        return conn

    @property
    def run_query(self, query):
        cursor = self.conexionbd()
        cursor.execute(query)  # Ejecutar una consulta
        if query.upper().startswith('SELECT'):
            data = self.cursor.fetchall()  # Traer los resultados de un select
        else:
            conn.commit()  # Hacer efectiva la escritura de datos
            data = None

        cursor.close()  # Cerrar el cursor
        conn.close()  # Cerrar la conexión
        return data


    @Pyro4.expose
    def login_usuario(self, email, clave):

        conexion= self.conexionbd()
        cursor = conexion.cursor()


        sql = "SELECT id_tipo FROM usuario WHERE email = '%s' AND clave = '%s'" % (email, clave)
        cursor.execute(sql)  # Ejecutar una consulta

        result = cursor.fetchall()

        if result:
            for registro in result:
                datos = registro[0]

        else:
            datos = 0

        return datos

    def login_register(self, nombre, apellido, clave, id_tipo, email):

        conexion = self.conexionbd()
        cursor = conexion.cursor()

        sql = "INSERT INTO usuario (nombre, apellido, clave, id_tipo, email ) VALUES ('%s','%s','%s',%d,'%s')" % (
            nombre, apellido, clave, id_tipo, email)

        result = cursor.fetchall()

        if result:
            for registro in result:
                datos = registro[0]

        else:
            datos = 0

        return datos

    def pagina_listar(self):
        conexion=self.conexionbd()
        cursor=conexion.cursor()
        sql = "SELECT * FROM pagina"
        cursor.execute(sql)
        resultados = cursor.fetchall()
        return resultados

    @Pyro4.expose
    def pagina_eliminar(self, pagina):


        conexion = self.conexionbd()
        cursor = conexion.cursor()  # Crear un cursor
        sql = "DELETE FROM pagina WHERE id_pagina = %s" % (pagina)


        cursor.execute(sql)
        conexion.commit()
        result = cursor.fetchall()

        if result:
            for registro in result:
                datos = registro[0]

        else:
            datos = 0

        return datos


    def pagina_insertar(self, nombre, url):

        conexion = self.conexionbd()
        cursor = conexion.cursor()  # Crear un cursor
        sql = "INSERT INTO pagina (nombre, url) VALUES ('%s','%s')" % (nombre, url)

        cursor.execute(sql)
        conexion.commit()
        result = cursor.fetchall()

        if result:
            for registro in result:
                datos = registro[0]

        else:
            datos = 0

        return datos

    def palabras_cont(self, pagina):

        conexion = self.conexionbd()
        cursor = conexion.cursor()
        sql = "SELECT url FROM pagina WHERE id_pagina = %s" % (pagina)
        cursor.execute(sql)
        result = cursor.fetchone()

        if result:
            for registro in result:
                datos = registro[0]

        else:
            datos = 0
            return 0

        recurso = datos
        print(datos)
        texto = BeautifulSoup(recurso.text, 'html.parser').get_text()

        # Remplazo todos los caracteres ASCII de puntuacion por espacios e inicializa el Array
        palabrasArray = re.sub('[%s]' % re.escape(string.punctuation), ' ', texto).split()

        # Ordenacion sin repeticion de todos los elementos del Array
        numero = 0
        for i in sorted(set(palabrasArray)):
            # Imprime solo las palabras con caracteres alfabeticos.
            if (i.isalpha() == True):
                numero += 1
                # print("%.3d %s" % (numero, i))
        return "la cantidad de palabras de la pagina " + str(result) + " es :" + str(numero)

    def diccionario(self):
        conexion=self.conexionbd()
        cursor=conexion.cursor()
        sql = "SELECT * FROM diccionario"
        cursor.execute(sql)
        resultados = cursor.fetchall()
        return resultados

    def contar_imagenes(self, pagina):

        conexion = self.conexionbd()
        cursor = conexion.cursor()
        sql = "SELECT url FROM pagina WHERE id_pagina = %s" % (pagina)
        print (sql)
        cursor.execute(sql)
        result = cursor.fetchall()

        if result:
            for registro in result:
                datos = registro[0]

        else:
            datos = 0
            return 0

        recurso = get(datos)
        pagina = BeautifulSoup(recurso.text, 'html.parser')

        enlaces = pagina.find_all('img')  # Buscar Imagenes por medio de la etiqute img
        for enlace in enlaces:
            etiquetas = enlace.get('alt')  # Nombre de la Imagen, texto alternativo
            if (etiquetas != None and etiquetas != ""):  # Seleciona las imagenes
                etiquetas_imagenes.append(etiquetas.upper())  # Concatena las imagenes en una lista

        a = len(etiquetas_imagenes)

        return (a)


def main():
    demonio = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = demonio.register(Servidor)
    ns.register("Leidy.Cristian", uri)
    print ("estoy corriendo")
    demonio.requestLoop()

if __name__ == "__main__":
    main()
