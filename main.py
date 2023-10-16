'''

'''

import numpy as np
from datetime import timedelta, date, datetime
from dateutil import relativedelta
#from reportlab.pdfgen import canvas
import sqlite3


nombre_db = "db1.db"

def crear_base_de_datos():    
    conexion=sqlite3.connect(nombre_db)
    try:                       
        conexion.execute("""create table oldpersonal (
                                  cedula integer primary key unique,
                                  nombre text,
                                  apellido text,
                                  codplantel text,
                                  nombreplantel text,
                                  fechaingreso text,
                                  vacpendientes text,
                                  vacdiaspendientes text,
                                  vacultima text,
                                  codcargo text,
                                  tipocargo text,
                                  descipccioncargo text,
                                  ultimoincrementovac text

                            )""")  

        conexion.execute("""create table personal (
                                  cedula integer primary key unique,
                                  nombre text,
                                  apellido text,
                                  coddependencia text, 
                                  codcargo text,                                  
                                  fechaingreso text,
                                  vacpendientes text,
                                  vacdiaspendientes text,
                                  vacultima text,
                                  ultimoperiodovac text,                                                                  
                                  ultimoincrementovac text

                            )""")          

        conexion.execute("""create table vacaciones (
                                  cedula integer,  
                                  fechainicio text,
                                  fechafin text,                                  
                                  diasdisfrutados text,
                                  ultimoperiodovac text,   
                                  observacion text                                                            
                                  
                            )""")
      
        conexion.execute("""create table dependencia (                                  
                                  cod text,                                    
                                  descripcion text 
                            )""")
       
        conexion.execute("""create table cargo (                                  
                                  cod text,                                   
                                  descripcion text 
                            )""")

        
        print("se crearon las tablas")                        
    except sqlite3.OperationalError as e:
        print("La tabla ya existe", e)                    
    conexion.close()

##### CRUD Operation #########

def crear_informacion(inf):  
   

    try:
        ingreso = inf["fechaingreso"][4:]
        nuevoincremento = datetime.strptime(f'{int(datetime.now().year-1)}{ingreso}', '%Y-%m-%d').date()
        conexion=sqlite3.connect(nombre_db)   
        conexion.execute("insert into personal(cedula,nombre,apellido,codcargo,coddependencia,fechaingreso,vacpendientes,vacdiaspendientes,vacultima,ultimoperiodovac,ultimoincrementovac) values (?,?,?,?,?,?,?,?,?,?,?)"
            ,(  inf["cedula"], # cedula 
                inf["nombre"],# nombre
                inf["apellido"],# apellido
                inf["codcargo"],# codplantel
                inf["coddependencia"],# nombreplantel
                inf["fechaingreso"],# fechaingreso
                inf["vacpendientes"],# vacpendientes
                inf["vacdiaspendientes"],# vacdiaspendientes
                inf["vacultima"],# vacultima
                inf["ultimoperiodovac"],
                nuevoincremento,# ultima compromacion   
                ))
        conexion.commit()
        conexion.close()
    except (sqlite3.OperationalError, sqlite3.IntegrityError, IndexError) as e:
        print("My Error COD: ", e)
        return 404

def leer_informacion(cedula):
    try:
        conexion=sqlite3.connect(nombre_db)
        cursor=conexion.execute(f"select * from personal WHERE cedula={cedula}")
        cursor.row_factory = sqlite3.Row
        c = dict(cursor.fetchall()[0])
        conexion.close()
        return c
    except (sqlite3.OperationalError,IndexError) as e:
        print(e)
        return 404
    
                                
def actualizar_vacaciones(dato):
    try:
        conexion=sqlite3.connect(nombre_db)   
        sql = ''' UPDATE personal
                  SET vacpendientes = ? ,
                      vacdiaspendientes = ? ,
                      vacultima = ?,
                      ultimoperiodovac = ?
                  WHERE cedula = ?'''
        cur = conexion.cursor()
        cur.execute(sql, dato)
        conexion.commit()
        conexion.close()
    except (sqlite3.OperationalError, sqlite3.IntegrityError, IndexError) as e:
        print("My Error COD: ", e)
        return 404

  

def crear_vacacion(inf):
    try:
        conexion=sqlite3.connect(nombre_db)   
        conexion.execute("insert into vacaciones(cedula, fechainicio, fechafin, diasdisfrutados, ultimoperiodovac) values (?,?,?,?,?)"
            ,(  inf["cedula"], # cedula 
                inf["fechainicio"],# fecha de inicio de las vacaciones
                inf["fechafin"],# ultimio dia de las vacaciones
                inf["diasdisfrutados"],# cuantos dias disfruto
                inf["agregarperiodo"],               
                             
                ))
        conexion.commit()
        conexion.close()
    except (sqlite3.OperationalError, sqlite3.IntegrityError, IndexError) as e:
        print("My Error COD: ", e)
        return 404

def leer_vacacion(cedula):
    try:
        conexion=sqlite3.connect(nombre_db)
        cursor=conexion.execute(f"select * from vacaciones WHERE cedula={cedula}")
        cursor.row_factory = sqlite3.Row
        c = []
        for i in cursor.fetchall():
            c.append(list(i))
        #c = list(cursor.fetchall()[1])
        conexion.close()
        return c
    except (sqlite3.OperationalError,IndexError) as e:
        print(e)
        return 404
################################

def incrementar_vacacion():
        try:
            conexion=sqlite3.connect(nombre_db)
            cursor=conexion.execute(f"select cedula,fechaingreso,vacpendientes,vacdiaspendientes,ultimoincrementovac from personal")
            cursor.row_factory = sqlite3.Row
            c = []
            for i in cursor.fetchall():
                c.append(list(i))
            #c = list(cursor.fetchall()[1])
            for i in c:
                #print(i)
                fecha_comprobacion = datetime.strptime(str(i[4]), '%Y-%m-%d')
                datehoy = datetime.strptime("2031-10-11", '%Y-%m-%d') # datetime.now()
                x = datehoy - fecha_comprobacion                                                                
                if x.days > 365: 
                           sql = ''' UPDATE personal
                                     SET vacpendientes = ? ,
                                         vacdiaspendientes = ? ,
                                         ultimoincrementovac = ?
                                     WHERE cedula = ?'''
                           cur = conexion.cursor()
                           dias = int(i[2]) + 1
                           pendi = int(i[3]) + 35
                           nueva_fecha = f"{datehoy.year}-{fecha_comprobacion.month}-{fecha_comprobacion.day}"
                           cur.execute(sql, [dias, pendi, nueva_fecha, int(i[0])])
                           conexion.commit()
            conexion.close()
            return c
        except (sqlite3.OperationalError,IndexError) as e:
            print(e)
            return 404
    
crear_base_de_datos()
incrementar_vacacion()

ayo = str(date.today().strftime("%Y"))

Festivos=[
f'{ayo}-05-01',
f'{ayo}-04-19',
f'{ayo}-06-24',
f'{ayo}-07-05',
f'{ayo}-07-24',
f'{ayo}-09-08',
f'{ayo}-10-12',
f'{ayo}-12-24',
f'{ayo}-12-25',
f'{ayo}-12-31',
f'{str(int(ayo) + 1)}-01-01',
]

file_paths = "nolaborables.txt"

with open(file_paths, "r") as file:
    lines = file.read()
    lines = lines.split("\n")
    for i in lines[1:]:
        if not (i == ""):      
            ti = str(datetime.strptime(i, '%Y-%m-%d').date())      
            Festivos.append(ti)

#print(Festivos)
def calcular_regreso_trabajo(fecha_de_inicio, dias_de_vacaciones):
    fecha_formateada = datetime.strptime(fecha_de_inicio, '%Y-%m-%d').date()
    
    for i in range(365):
        fecha_final = fecha_formateada + timedelta(days=i) 
        bussy = np.busday_count(fecha_de_inicio, fecha_final,holidays=Festivos)
        if(bussy) == dias_de_vacaciones:
            fecha_extra = fecha_final
    return fecha_extra

