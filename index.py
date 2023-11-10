# line 28, in mostrarDatos
#     tabla.insert('', 0, text=documento["_id"], values=(documento["nombre"], documento["email"], documento["edad"], documento["ciudad"]))     
#                                                                             ~~~~~~~~~^^^^^^^^^
# KeyError: 'email'

# SE DEBE A QUE EL CAMPO REFERIDO COMO KEYWORD NO TIENE EXISTE EN TODOS LOS DOCUMENTOS Y DEBE AGREGARSE PARA 
# PODER LEERLO CON NORMALIDAD


import sys
print(sys.path)
import sys
sys.path.append('c:\\users\\opaal\\appdata\\local\\packages\\pythonsoftwarefoundation.python.3.11_qbz5n2kfra8p0\\localcache\\local-packages\\python311\\site-packages')
import pymongo
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from bson.objectid import ObjectId

TIME_OUT=1000
text_conect="mongodb+srv://Brayan1016:1006878949@electiva.3naiwky.mongodb.net/"
MONGOBD="python"
coleccion="clientes"

cliente=pymongo.MongoClient(text_conect,serverSelectionTimeoutMS=TIME_OUT)
BaseDatos=cliente[MONGOBD]
coleccionbd=BaseDatos[coleccion]
ID_ALUMNO=""

def mostrarDatos(tabla):
    
    try:
        registros=tabla.get_children()
        for registro in registros:
            tabla.delete(registro)
        for documento in coleccionbd.find():
            if documento.get("ciudad") is None:
                tabla.insert('', 0, text=documento["_id"], values=(documento["nombre"], documento["email"], documento["edad"], ""))
            else:
                tabla.insert('', 0, text=documento["_id"], values=(documento["nombre"], documento["email"], documento["edad"], documento["ciudad"]))
            # print(documento)
        # cliente.close()
        # cliente.server_info()
        # print("Conexion exitosa")
        
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print ("No se ha podido conectar al servidor MongoDB",errorTiempo)
    except pymongo.errors.ConnectionFailure as errorCOnexion:
        print("Fallo al conectarse a mongodb "+errorCOnexion)

def insertarDatos():
    if len(nombre.get()) !=0 and len(email.get()) !=0 and len(edad.get()) !=0 :
        try:
            documento={"nombre":nombre.get(),"edad":edad.get(),"ciudad":ciudad.get(),"email":email.get()}
            coleccionbd.insert_one(documento)
            nombre.delete(0,END)
            email.delete(0,END)
            edad.delete(0,END)
            ciudad.delete(0,END)
            
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror(message="LLene los campos")
    mostrarDatos(tabla)


def dobleClickTabla(event):
    global ID_ALUMNO
    ID_ALUMNO=str(tabla.item(tabla.selection())["text"])
    documento=coleccionbd.find({"_id": ObjectId(ID_ALUMNO)})[0]
    nombre.delete(0,END)
    nombre.insert(0,documento["nombre"])
    email.delete(0,END)
    email.insert(0,documento["email"])
    edad.delete(0,END)
    edad.insert(0,documento["edad"])
    ciudad.delete(0,END)
    ciudad.insert(0,documento["ciudad"])
    crear["state"]="disabled"
    editar["state"]="normal"

def editarRegistro():
    global ID_ALUMNO
    if len(nombre.get()) !=0 and len(email.get()) !=0 and len(edad.get()) !=0 and len(ciudad.get()) !=0:
        try:
            idBuscar={"_id":ObjectId(ID_ALUMNO)}
            nuevosValores={"nombre":nombre.get(),"edad":edad.get(),"ciudad":ciudad.get(),"email":email.get()}
            coleccionbd.update_many(idBuscar,{"$set":nuevosValores})
            nombre.delete(0,END)
            email.delete(0,END)
            edad.delete(0,END)
            ciudad.delete(0,END)
            mostrarDatos(tabla)
            
        except pymongo.errors.ConnectionFailure as error :
            print(error)
            messagebox.showerror(message=error)
    else:
        messagebox.showinfo(message="Los campos no pueden estar vacíos")
    crear["state"]="normal"
    editar["state"]="disabled"


def borrarRegistro():
    global ID_ALUMNO
    try:
        idBuscar={"_id":ObjectId(ID_ALUMNO)}
        coleccionbd.delete_one(idBuscar)
        nombre.delete(0,END)
        email.delete(0,END)
        edad.delete(0,END)
        ciudad.delete(0,END)
        mostrarDatos(tabla)
        crear["state"]="normal"
                
    except pymongo.errors.ConnectionFailure as error :
        print(error)
        messagebox.showerror(message=error)

def buscarRegistro():
    global ID_ALUMNO
    nombreBuscar={"nombre":buscarNombre.get()}
    documento = coleccionbd.find_one(nombreBuscar)
    if documento is not None:
        try:
            registros=tabla.get_children()
            for registro in registros:
                tabla.delete(registro)
            tabla.insert('', 0, text=documento["_id"], values=(documento["nombre"], documento["email"], documento["edad"], documento["ciudad"]))
            messagebox.showinfo(message=(documento["_id"]))
            nombre.delete(0,END)
            email.delete(0,END)
            edad.delete(0,END)
            ciudad.delete(0,END)
        except:
            
            messagebox.showerror("Error de busqueda",message="No se encontro el nombre")
    else:
        messagebox.showerror("Error de busqueda2",message="No se encontro el nombre")
ventana=Tk()
tabla=ttk.Treeview(ventana,columns=[f"#{n}" for n in range(1, 5)])
tabla.grid(row=1,column=0,columnspan=2)
tabla.heading("#0",text="ID")
tabla.heading("#1",text="NOMBRE")
tabla.heading("#2",text="EMAIL")
tabla.heading("#3",text="EDAD")
tabla.heading("#4",text="CIUDAD")
tabla.bind("<Double-Button-1>",dobleClickTabla)

#nombre
Label(ventana,text="Nombre").grid(row=2,column=0)
nombre=Entry(ventana)
nombre.grid(row=2,column=1)
# #email
Label(ventana,text="Email").grid(row=3,column=0)
email=Entry(ventana)
email.grid(row=3,column=1)
# #edad
Label(ventana,text="Edad").grid(row=4,column=0)
edad=Entry(ventana)
edad.grid(row=4,column=1)
# #ciudad
Label(ventana,text="Ciudad").grid(row=5,column=0)
ciudad=Entry(ventana)
ciudad.grid(row=5,column=1)
#boton crear
crear=Button(ventana,text="Agregar",command=insertarDatos,bg="green",fg="white")
crear.grid(row=6,columnspan=2,sticky=W+E)
#boton editar
editar=Button(ventana,text="Editar",command=editarRegistro,bg="yellow")
editar.grid(row=7,columnspan=2,sticky=W+E)
editar["state"]="disabled"
#boton borrar
borrar=Button(ventana,text="Eliminar",command=borrarRegistro,bg="red",fg="white")
borrar.grid(row=8,columnspan=2,sticky=W+E)

#buscar nombre
buscar=Button(ventana,text="buscar",command=buscarRegistro,bg="blue",fg="white")
buscar.grid(row=10,columnspan=2,sticky=W+E)
#buscar nombre
Label(ventana,text="Buscar por nombre").grid(row=9,column=0)
buscarNombre=Entry(ventana)
buscarNombre.grid(row=9,column=1)
mostrarDatos(tabla)
ventana.mainloop()
