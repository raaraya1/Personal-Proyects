import psycopg2
import pandas as pd


class SQL():
    def __init__(self, data_base, user, password):
        self.conexion = 'dbname={} user={} password={}'.format(data_base, user, password)

    def ejecutar(self, comando):
        conn = psycopg2.connect(self.conexion)
        cur = conn.cursor()
        cur.execute(comando)
        conn.commit()
        cur.close()
        conn.close()

    def mostrar_tabla(self, comando):
        conn = psycopg2.connect(self.conexion)
        cur = conn.cursor()
        cur.execute(comando)
        rows = cur.fetchall()
        df = pd.DataFrame(rows)
        conn.commit()
        cur.close()
        conn.close()
        return df
    
    def importar(self, nombre, df):
        columnas = list(df.columns)
        arg = ''
        for columna in columnas:
            arg += columna + ' varchar(50), ' 
        arg = arg[:-2]
        comando_base = 'create table {}({})'.format(nombre, arg)
        self.ejecutar(comando_base)

        num_filas = len(df)
        for fila in range(num_filas):    
            comando_base = ''
            arg = ''

            for columna in columnas:
                arg += "'" + str(df[columna][fila]) + "', " 
            arg = arg[:-2]
            comando_base = 'insert into {} values({})'.format(nombre, arg)

            self.ejecutar(comando_base)
            
    def column_type_int(self, nombre_tabla, nombre_columna):
        nombre_tabla = str(nombre_tabla)
        nombre_columna = str(nombre_columna)

        comando_base = 'select {} from {}'.format(nombre_columna, nombre_tabla)
        df = self.mostrar_tabla(comando_base)
        columna_guardada = list(df[0][:])
        columna_guardada = [int(valor) for valor in columna_guardada]

        comando = 'alter table {} drop column {}'.format(nombre_tabla, nombre_columna)
        self.ejecutar(comando)

        comando = 'alter table {} add column {} int'.format(nombre_tabla, nombre_columna)
        self.ejecutar(comando)

        comando = 'alter table {} add column indice serial'.format(nombre_tabla)
        self.ejecutar(comando)

        for ind, valor in enumerate(columna_guardada):
            comando = 'update {} set {} = {} where indice = {}'.format(nombre_tabla, nombre_columna, valor, (ind+1))
            self.ejecutar(comando)

        comando = 'alter table {} drop column indice'.format(nombre_tabla)
        self.ejecutar(comando)
