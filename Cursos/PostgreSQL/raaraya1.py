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

    def mostrar_tabla(self, comando, nombre_tabla=False):
        if nombre_tabla == False:
            conn = psycopg2.connect(self.conexion)
            cur = conn.cursor()
            cur.execute(comando)
            rows = cur.fetchall()
            df = pd.DataFrame(rows)
            conn.commit()
            cur.close()
            conn.close()
            return df
        else:
            # nombre de las columnas
            conn = psycopg2.connect(self.conexion)
            cur = conn.cursor()
            comando1 = "SELECT (column_name, data_type) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}'".format(nombre_tabla)
            cur.execute(comando1)            
            columnas = cur.fetchall()            
            conn.commit()
            cur.close()
            conn.close()
            
            # para el resto de los datos
            conn = psycopg2.connect(self.conexion)
            cur = conn.cursor()
            cur.execute(comando)
            rows = cur.fetchall()
            df = pd.DataFrame(rows)
            conn.commit()
            cur.close()
            conn.close()
            return columnas, df       
            
            
            

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
        
        
    def agregar_columna(self, nombre_tabla, nombre_columna, lista_datos, tipo_columna='varchar(50)'):
        comando = 'alter table {} add column indice serial'.format(nombre_tabla)
        self.ejecutar(comando)
        
        if tipo_columna == 'varchar(50)':
            comando_base = 'alter table {} add column {} {}'.format(nombre_tabla, nombre_columna, tipo_columna)
            self.ejecutar(comando_base) 
            
            for ind, valor in enumerate(lista_datos):
                comando_base = "update {} set {} = '{}' where indice = {}".format(nombre_tabla, nombre_columna, valor, ind+1)
                self.ejecutar(comando_base)
            
        else:
            comando_base = 'alter table {} add column {} {}'.format(nombre_tabla, nombre_columna, 'int')
            self.ejecutar(comando_base)            

            for ind, valor in enumerate(lista_datos):
                comando_base = 'update {} set {} = {} where indice = {}'.format(nombre_tabla, nombre_columna, valor, ind+1)
                self.ejecutar(comando_base)

        comando = 'alter table {} drop column indice'.format(nombre_tabla)
        self.ejecutar(comando)
    
    # esta parte del codigo es para establecer la primary key de una tabla (con posibilidad de generar la columna)
    def valores_duplicados(self, columna_nueva):
        num_col_nueva = len(columna_nueva)
        conjunto = set(columna_nueva) 
        num_conj_nueva = len(conjunto)
        duplicados = num_col_nueva - num_conj_nueva
        return duplicados

    def dic_duplicados(self, df, columna_nueva):
        indices =  range(len(df))
        diccionario = {}
        for ind in indices:
            diccionario[columna_nueva[ind]] = indices[ind]
        indices_dic = list(diccionario.values())
        ind_duplicados = [valor for valor in indices]
        for ind in indices_dic:
            ind_duplicados.remove(ind)
        # corregir la posicion
        ind_duplicados = [i+1 for i in ind_duplicados]
        return ind_duplicados

    def generar_columna(self, df, columnas_generadoras):
        columna_nueva = []
        for i in range(len(df)):
            columna_nueva.append('')
            for j in columnas_generadoras:            
                columna_nueva[i] += df[j][i] + '_'
            columna_nueva[i] = columna_nueva[i][:-1]
        return columna_nueva    

    def primary_key(self, nombre_tabla, nombre_columna, num_columna, columna_adicional=False, columnas_generadoras=[]):
        # generar dataframe
        comando = 'select * from {}'.format(nombre_tabla)
        df = self.mostrar_tabla(comando)

        # generar columna para verificar
        if columna_adicional == True:
            columna_nueva = self.generar_columna(df, columnas_generadoras)
        # en caso contrario se asigna a columna_nueva la columna que se quiere verificar
        else:
            columna_nueva = list(df[num_columna][:])

        # calcular cantidad de duplicados de la nueva columna
        duplicados = self.valores_duplicados(columna_nueva)

        # caso 1 -> no existen valores duplicados y columna adicional
        if columna_adicional == True and duplicados == 0:
            self.agregar_columna(nombre_tabla, 'columna_nueva', columna_nueva)
            comando = 'alter table {} add primary key (columna_nueva)'.format(nombre_tabla)
            self.ejecutar(comando)

        # caso 2 -> no existen valores duplicados y sin columna adicional
        elif columna_adicional == False and duplicados == 0:
            comando = 'alter table {} add primary key ({})'.format(nombre_tabla, nombre_columna)
            self.ejecutar(comando)

        # caso 3 -> existen valores duplicados y columna adicional
        if columna_adicional == True and duplicados > 0:
            # generar la columna indice 
            comando = 'alter table {} add column indice serial'.format(nombre_tabla)
            self.ejecutar(comando)

            # indice de las filas que hay que eliminar
            ind_duplicados = self.dic_duplicados(df, columna_nueva)

            # para eliminarlas ejecutamos el siguiente comando
            for ind in ind_duplicados:
                comando_base = 'delete from {} where indice = {}'.format(nombre_tabla, ind)
                self.ejecutar(comando_base)

            # recordamos eliminar la columna indice
            comando = 'alter table {} drop column indice'.format(nombre_tabla)
            self.ejecutar(comando)

            # volvemos a generar la nueva columna (pero ahora corregida)
            comando = 'select * from {}'.format(nombre_tabla)
            df = self.mostrar_tabla(comando)

            # restablecemos la columna nueva
            columna_nueva = self.generar_columna(df, columnas_generadoras)

            # verificar condicion de valores duplicados
            duplicados = self.valores_duplicados(columna_nueva)
            if duplicados == 0:
                self.agregar_columna(nombre_tabla, nombre_columna, columna_nueva)
                comando = 'alter table {} add primary key ({})'.format(nombre_tabla, nombre_columna)
                self.ejecutar(comando)

        # caso 4 -> existen valores duplicados y sin columna adicional
        elif columna_adicional == False and duplicados > 0:
            # indice de las filas que hay que eliminar
            ind_duplicados = self.dic_duplicados(df, columna_nueva)

            # añadir la columna indice
            comando = 'alter table {} add column indice serial'.format(nombre_tabla)
            self.ejecutar(comando)

            # retirar las filas que calzan con la de los valores repetidos
            for ind in ind_duplicados:
                comando_base = 'delete from {} where indice = {}'.format(nombre_tabla, ind)
                self.ejecutar(comando_base)    

            # volvemos a generar la nueva columna (pero ahora corregida)
            comando = 'select * from {}'.format(nombre_tabla)
            df = self.mostrar_tabla(comando)

            # restablecemos la columna nueva
            columna_nueva = self.generar_columna(df, columnas_generadoras)

            # verificar condicion de valores duplicados
            duplicados = self.valores_duplicados(columna_nueva)
            if duplicados == 0:
                comando = 'alter table {} add primary key ({})'.format(nombre_tabla, nombre_columna)
                self.ejecutar(comando)

            ## eliminar la columna indice
            comando = 'alter table {} drop column indice'.format(nombre_tabla)
            self.ejecutar(comando)
    
    def foreign_key(self, tabla1, columna1, tabla2, columna2):
        comando = '''alter table {} 
                     add constraint FK{} 
                     foreign key({}) 
                     references {} ({})'''.format(tabla1, columna1 + '_' + columna2 ,columna1, tabla2, columna2)

        self.ejecutar(comando)

