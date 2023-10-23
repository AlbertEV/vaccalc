'''
Albert Espinoza 2023
albertespinozav93@gmail.com
'''
import PySimpleGUI as sg
import main as db
from datetime import timedelta, date, datetime

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
registerFont(TTFont('Arial','ARIAL.ttf'))

sg.theme('reddit') 

registro_vac = []
registro_personal = []
Extras = []
Regresan = []

toprow = ['Fecha de Inicio', 'Fecha de Regreso', 'Dias', 'periodo']
toprow_regresan = ['Cedula', 'Fecha de Reincorporación', 'Dias Disfrutados','Nombre', 'Apellido', 'Dependencia', ]
rows = []
rows_regresan = []
        
lista_dependencia = []
temp = db.leer_dependencia() 
for i in temp:    
    lista_dependencia.append(f"{i[1]}")   
lista_dependencia = list(reversed(lista_dependencia))              

lista_cargo = []
temp = db.leer_cargo() 
for i in temp:    
    lista_cargo.append(f"{i[1]}")   
lista_cargo = list(reversed(lista_cargo))     

def canvax(c, offset, datos, vac):   
    c.setFont("Arial", 11)
    my_Style=ParagraphStyle('My Para style',
    fontName='Arial',
    fontSize=10,
    )     
    c.drawImage("logo.jpg", 1, 760 + offset,width=600, height=30)
    c.drawString(220, 730 + offset, "CONTROL DE VACACIONES")
    c.drawString(10, 710 + offset, "Datos del Empleado")
    c.drawString(10, 690 + offset, f"Apellidos y Nombre {datos['apellido']} {datos['nombre']}")
    c.drawString(430, 690 + offset, f"Cedula {datos['apellido']}")
    c.drawString(10, 670 + offset, f"Cargo {datos['codcargo']}")
    c.drawString(300, 670 + offset, f"Dependencia {datos['coddependencia']}")
    c.drawString(10, 650 + offset, f"Fecha de Ingreso {datos['fechaingreso']}")
    c.drawString(190, 650 + offset, f"Ultimo Periodo Solicitado {vac[2]}")
    c.drawString(420, 650 + offset, f"Dias Habiles a Disfrutar")
    c.drawString(10, 630 + offset, f"Desde {vac[0]}")
    c.drawString(170, 630 + offset, f"Hasta {vac[1]}")
    c.drawString(360, 630 + offset, f"Fecha de Reincorporacio {vac[1]}")
    c.drawString(10, 610 + offset, "El bono vacacional se le cancela en")
    c.drawString(390, 610 + offset, "Del Año")

    c.drawString(10, 590 + offset, "Observacion:")

    c.drawString(50, 530 + offset, "Jefe Div gestion Interna")
    c.drawString(230, 530 + offset, "Supervisor Inmediato")
    c.drawString(420, 530 + offset, "Empleado")

    c.drawString(10, 490 + offset, "Integrados de personal")
    c.drawString(40, 475 + offset, "06/10/2022")


    p1=Paragraph('''OBSERVACION 2: SE RECONOCERAN HASTA DOS PERIODOS DE VACACIONES ACUMULADOS (ART. 199.LOTT) \
                 MANIFIESTO QUE ESTOY EN PLENO CONOCIMIENTO QUE LA SOLICITUD DE LAS VACACIONES CORRESPONDEN AL \
                 PERIODO________________NO SIGNIFICA LA APROBACION DE LA MISMA, POR LO TANTO, NO DEBO AUSENTARME DE MI SITIO DE \
                 TRABAJO HASTA TANTO NO RECIBA EL CORRESPONDIENTE ACUSE DE RECIBO. Y HAGA DEL CONOCIMIENTO A MI JEFE \
                 INMEDIATO \
            ''', my_Style)

    p1.wrapOn(c,580,600)
    p1.drawOn(c,10,405 + offset)

def update_input():
    window['nombre'].update(inf["nombre"])
    window['apellido'].update(inf["apellido"])
    window['coddependencia'].update(inf["coddependencia"])           
    window['fechaingreso'].update(inf["fechaingreso"])
    window['vacpendientes'].update(inf["vacpendientes"])
    window['vacdiaspendientes'].update(inf["vacdiaspendientes"])
    window['vacultima'].update(inf["vacultima"])
    window['codcargo'].update(inf["codcargo"])          
    window['ultimoperiodovac'].update(inf["ultimoperiodovac"])

def clear_input():
    window['nombre'].update("")
    window['apellido'].update("")
    window['coddependencia'].update(values = lista_dependencia)            
    window['fechaingreso'].update("")
    window['vacpendientes'].update("")
    window['vacdiaspendientes'].update("")
    window['vacultima'].update("")
    window['codcargo'].update(values = lista_dependencia)                       
    window['ultimoperiodovac'].update("") 
    data = []  
    window['-TABLE-'].update(values=data)  

'''
###### registro_personal #####
registro_personal += [ 

    [sg.Text('Cedula:'), sg.Input(key='cedula',size=(12,1)),
     sg.Button('Buscar'),
     sg.Text('Nombre:', ), sg.Input(key='nombre',),
     sg.Text('Apellido:', ), sg.Input(key='apellido',)],
    
    [sg.Text('')], 

    [sg.Text('Codigo de Dependencia:', ), sg.Input(key='codplantel', size=(12,1)),
     sg.Text('Descipcion de Dependencia:', ), sg.Input(key='nombreplantel',)],
    
    [sg.Text('')], 

    [sg.Text('Codigo Cargo:'), sg.Input(key='codcargo',size=(12,1)),
     sg.Text('Descipcion de Cargo:'), sg.Input(key='descipccioncargo',size=(30,1))],

    [sg.Text('')], 

    [sg.Text('Tipo Cargo:'), sg.Input(key='tipocargo',size=(12,1)),
      sg.Text('Fecha de ingreso:'), sg.Input(key='fechaingreso',size=(12,1)),
      sg.Text('Mes de ingreso:'), sg.Input(size=(12,1))],

    [sg.Text('')], 
     
    # no sepuede modificar Desactivar
    [sg.Text('Año Ultima vacacione:'), sg.Input(key='vacultima',size=(12,1)),
      sg.Text('Vacaciones pendientes:'), sg.Input(key='vacpendientes',size=(8,1)),
      sg.Text('Dias pendientes:'), sg.Input(key='vacdiaspendientes',size=(8,1))],

    [sg.Text('')], 

    #[sg.Text('Contraseña:'),sg.Input(key='reg_cedula',size=(8,1)), 
     [sg.Button('Agregar')]
]
#######################
'''
###### registro_vacaciones #######
registro_vac += [ 
    
    [sg.Text('Cedula:'), sg.Input(key='cedula',size=(12,1)),
     sg.Button('Buscar', key="BuscarVac"),
     sg.Text('Nombre:', ), sg.Input(key='nombre',),
     sg.Text('Apellido:', ), sg.Input(key='apellido',)],
    
    [sg.Text('')], 

    [sg.Text('Cargo:'), sg.Combo(lista_cargo, enable_events=True,  readonly=False, key='codcargo', size=(35,1)),
     sg.Text('Dependencia:', ), sg.Combo(lista_dependencia, default_value="", enable_events=True,  readonly=False, key='coddependencia', size=(35,1))],
    
    [sg.Text('')], 


   
    [#sg.Text('Tipo Cargo:'), sg.Input(key='tipocargo',size=(12,1)),
      sg.Text('Fecha de ingreso:'), sg.Input(key='fechaingreso',size=(12,1)), sg.CalendarButton('Seleccionar fecha', month_names=('Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'), day_abbreviations=('Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado'),close_when_date_chosen=True,  target='fechaingreso', format='%Y-%m-%d', no_titlebar=False, ),
      sg.Text('Ultimo periodo vacaciones:'), sg.Input(key='ultimoperiodovac',size=(12,1)),
      sg.Text('Ultimo Año Vacaciones:'), sg.Input(key='vacultima',size=(12,1)),
      #sg.Text('Mes de ingreso:'), sg.Input(size=(12,1))
      ],

    [sg.Text('')], 
     
    # no sepuede modificar Desactivar
    #[sg.Text('Año Ultima vacacione:'), sg.Input(key='vacultima',size=(12,1)),
      [sg.Text('Vacaciones pendientes:'), sg.Input(key='vacpendientes',size=(8,1)),
      sg.Text('Dias pendientes:'), sg.Input(key='vacdiaspendientes',size=(8,1))],

    [sg.Table(values=rows, headings=toprow,
    auto_size_columns=True,
    display_row_numbers=False,
    justification='center', key='-TABLE-',
    selected_row_colors='red on yellow',
    enable_events=True,
    expand_x=True,
    expand_y=True,
    enable_click_events=True,
    size=(2,6))],

    [sg.Text('')], 

    #[sg.Text('Contraseña:'),sg.Input(key='reg_cedula',size=(8,1)), 
    [sg.Button('Agregar Nuevo Personal', key="Agregar"), 
     #sg.Button('Editar Personal', key="editpersonal"),
     sg.Button('Informe', key="Informe")],
    
    [sg.Text('')], 
    [sg.Text('')], 
]

### registrar fecha vacaciones
registro_vac += [ 
    [sg.Text('Datos de Vacaciones a Disfrutar', font = (14))], 

    [sg.Text('Dias no laborables este año: '), sg.Text(str(len(db.Festivos)))],  
    
     [sg.Text('Dias a disfrutar:', ), sg.Input(key='diasdisfrutados')],
     [sg.Text('Fecha de inicio:', ), sg.Input(key='fechainicio'), sg.Button('Date Popup')],
     [sg.Text('Año a disfrutar'), sg.Input(key='ayodisfrutado',)],
    
    [sg.Text('Fecha Reincorporacio'), sg.Input(key='fechafin',size=(15,1)),
    sg.Text('Ultimo periodo'), sg.Input(key='agregarperiodo',size=(15,1))],
    #sg.Text('Fecha a Incorporarse'), sg.Input(key='fecha-regreso',size=(15,1))],

    [sg.Button('Agregar Vacaciones', key="AgregarVacacion"), ],
    [sg.Text('')], 
    [sg.Text('')], 

#############################
]
########################

### extra agregar dependencia
Extras += [ 
    [sg.Text('Agregar Dependencia', font = (14))],   
    
    [sg.Text('Codigo Dependencia:', ), sg.Input(key='codigodependencia')],
    [sg.Text('Nombre Dependencia:', ), sg.Input(key='nombredependencia')],
  
    [sg.Button('Agregar', key="AgregarDependencia"), ],
    [sg.Text('')], 
    [sg.Text('')], 
    ]

### extra agregar cargo
Extras += [ 
    [sg.Text('Agregar Cargo', font = (14))],   
    
    [sg.Text('Codigo Cargo:', ), sg.Input(key='codigocargo')],
    [sg.Text('Nombre Cargo:', ), sg.Input(key='nombrecargo')],
  
    [sg.Button('Agregar', key="AgregarCargo"), ],
    [sg.Text('')], 
    [sg.Text('')], 
    ]
#############################

       
           
#### proximo a regresar de vacaciones
tabla = db.leer_personal_vacacion()            
data_regresan = []
#print(tabla)
for i in tabla:  
    inf_aux = db.leer_informacion(i[0])
    
    i.append(inf_aux["nombre"]) 
    i.append(inf_aux["apellido"])
    i.append(inf_aux["coddependencia"])    
    data_regresan.append(i)   



data_regresan = list(reversed(data_regresan))  
data_regresan = sorted(data_regresan, key=lambda item: (item[1]))  


print(data_regresan)


Regresan += [ 
    [sg.Table(values=data_regresan, headings=toprow_regresan,
    auto_size_columns=True,
    display_row_numbers=False,
    justification='center', key='-TABLE2-',
    selected_row_colors='red on yellow',
    enable_events=True,
    expand_x=False,
    expand_y=False,
    enable_click_events=True,
    size=(2,40))],
    [sg.Text('')], 
    [sg.Text('')], 
    ]


###################################


menu_def = [ ['Contacto', 'albertespinozav93@gmail.com'], ]
registro_vac += [[sg.Menu(menu_def)]]

tabgrp = [[sg.TabGroup([ [sg.Tab('Vacaciones', registro_vac, tooltip='Personal details'),
                         sg.Tab('En vacaciones', Regresan, tooltip='Personal details'),
                         sg.Tab('Extra', Extras, tooltip='Personal details'),
                    
                    ]],)]]  
        
window = sg.Window('Calculadora de Vacaciones', tabgrp)



table_inicio = ""
table_fin = ""
table_periodo = ""
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    print(event)
    if event == 'Date Popup':        
        date = sg.popup_get_date(close_when_chosen=False)
        if date:
            m, d, y = date
            fecha = f'{y:0>4d}-{m:0>2d}-{d:0>2d}'
            
            if values['diasdisfrutados'] == '':
                dias = 1
            else:
                dias = values['diasdisfrutados']   
            
            vacacion = int(values["vacpendientes"])
            input = int(values["diasdisfrutados"])
            vacacion -= divmod(input,35)[0]
            
            
            start_date = datetime.strptime(f'{y:0>4d}-{m:0>2d}-{d:0>2d}', '%Y-%m-%d')    

            periodo = (start_date - timedelta(days=(365.3 * vacacion))).year

            print(start_date, vacacion)

            periodo = f"{periodo - 1}-{periodo}"
            

            regreas = db.calcular_regreso_trabajo(str(fecha), int(dias))  
            
            window['ayodisfrutado'].update(f"{y:0>4d}")
            window['fechainicio'].update(fecha)
            window['fechafin'].update(regreas)
            window['agregarperiodo'].update(periodo)
    
    if event == 'BuscarVac':         
        inf = db.leer_informacion(values['cedula'])   
        if(inf == 404):                 
            clear_input()        

        else:    
            tabla = db.leer_vacacion(values['cedula'])            
            data = []
            #print(tabla)
            for i in tabla:
                #i[0], i[4] = i[4], i[0]
                data.append(i[1:])   
            data = list(reversed(data))              
            window['-TABLE-'].update(values=data)  
            update_input()

    if event == 'Agregar':    
        if values["cedula"]:    
           db.crear_informacion(values) 
    
    if event == 'AgregarVacacion':  
        if values["diasdisfrutados"] and values["fechainicio"] and values["cedula"]:            
            nuevavacacion = datetime.strptime(values["fechainicio"], '%Y-%m-%d')    
            hoy = datetime.today()
            fechaduplicada = False
            # revisamos la base de datos en busca de vacaciones duplicadas
            for i in reversed(db.leer_vacacion(values["cedula"])):    
                mivacaciones = datetime.strptime(i[2], '%Y-%m-%d')                     
                if (nuevavacacion <= mivacaciones) or (nuevavacacion <= hoy):
                    print("Fecha duplicada", nuevavacacion, mivacaciones)
                    fechaduplicada = True

            if fechaduplicada:
                fechaduplicada = False
                sg.Popup('Periodo vacacional existe', keep_on_top=True)
                continue    
        
        if values["diasdisfrutados"] and values["fechainicio"] and values["cedula"]:
            db.crear_vacacion(values) 
            vacacion = int(values["vacpendientes"])
            dias = int(values["vacdiaspendientes"])

            input = int(values["diasdisfrutados"])

            vacacion -= divmod(input,35)[0]
            dias -= input

            #orden para almacenar en la base de datos
            x = (vacacion, dias, values["ayodisfrutado"],values["agregarperiodo"] , values["cedula"])
            db.actualizar_vacaciones(x)
           
            tabla = db.leer_vacacion(values['cedula'])            
            data = []
            #print(tabla)
            for i in tabla:
                #i[0], i[4] = i[4], i[0]
                data.append(i[1:])   
            data = list(reversed(data))              
            window['-TABLE-'].update(values=data)  
   
    if event == 'Informe':  
        if values["cedula"] and values["-TABLE-"]:
            roww = values["-TABLE-"][0]  
            vac = [data[roww][0],data[roww][1],data[roww][3]]  
            c = canvas.Canvas(f'{values["cedula"]}-{values["vacultima"]}({vac[2]}).pdf', pagesize=letter)
            canvax(c, 0, values, vac)
            canvax(c, -400,values, vac)
            c.showPage()
            c.save()
   
    if event == 'AgregarDependencia':    
        if values["codigodependencia"] and values["nombredependencia"]:    
           db.crear_dependencia(values) 
   
    if event == 'AgregarCargo':    
        if values["codigocargo"] and values["nombrecargo"]:    
           db.crear_cargo(values) 
    
    '''
    if event[:2] == ('-TABLE-', '+CLICKED+'):
        row, col = position = event[2]
        print("holis",event[2])
        if None not in position and row >= 0:    
            print(data[row][0])
            print(data[row][1])
            print(data[row][3])
    '''
         

window.close()
