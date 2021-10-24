"""
Routes and views for the flask application.
"""
import re
import bcrypt
import os
import base64
import bson
import gridfs
import flask
#import session
from bson.binary import Binary
from datetime import datetime
from flask import render_template
from webOnboardingSite import app
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId

#from app import app

UPLOAD_FOLDER = 'C:\\Proyectos\\Proyectos\\doctos\\'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"

#bcrypt = Bcrypt()
client = MongoClient("mongodb://localhost:27017")
database = client["onboarding"]
collection = database["pyme"]
fs = gridfs.GridFS(database)


#@app.route('/')
@app.route('/addPyme')
def home():
    """Renders the home page."""
    
    #flask.session.pop('file', None)

    query = {"folio": 1234569789}
    cursor = collection.find(query)
    ##print(cursor)
    
    if cursor:
        data = {}
        for doc in cursor:         
            #print(doc)
            session["folio_objectid"] = str(doc["_id"])
            session['regimenopt'] = str(doc["regimen"])
            data["folio"]			= doc["folio"]
            #data["regimen"] 		= doc["regimen"] 
            data["nombre"] 			= doc["nombre"] 
            data["apellido_paterno"]= doc["apellido_paterno"] 
            data["apellido_materno"]= doc["apellido_materno"] 
            data["correo"] 			= doc["correo"] 
            data["telefono"] 		= doc["telefono"] 
            data["nombre_empresa"] 	= doc["nombre_empresa"] 
            data["sector"]			= doc["sector"]
        session["data"] = data
            
    ##print(session["data"])
    return render_template(
        'addPyme.html',
        title='Onboarding',
        titulo="¡Comencemos! Indica bajo qué régimen opera tu empresa",
        tarea="Régimen",
        formAnte = "AddPyme",
        porcentaje ="01/05",
        year=datetime.now().year,
    )

#********************Inincio************************
@app.route('/',methods=['POST','GET'])
def generaFolio():
 #   form = request.form
 #   if request.method=='POST':
  #      if request.form.get('generaFolio'):
 #           otp=form.get('folio')
  #          session['otp']=otp
   #         print(otp)
  #          return render_template('getOTP.html',otp)
        return render_template('inicio.html')
            
    

#********************Inincio************************


@app.route('/inicio', methods=["GET", "POST"])
def inicio():
    context={

    }
    return render_template('inicio.html', **context)

#********************Inincio************************
@app.route('/getOTP', methods=['GET','POST'])
def enviaSMS():
    context={

    }
    return render_template('getOTP.html', **context)
#********************Inincio************************

@app.route('/loadData', methods=["GET", "POST"])
def loadData():
    if request.method == 'POST':
        session['regimenopt'] = request.form.get('hdoptions') #request.form"flexRadioDefault")
        #print(session['regimenopt'] )

    dict = {}
    if(session["data"]):
        dict = session["data"]

    return render_template(       
        'loadData.html',
        title='Datos Generales',
        titulo="Datos generales de tu empresa",
        tarea="Datos generales",
        formAnte = "AddPyme",
        porcentaje ="02/05",
        avance = "40%",
        year=datetime.now().year,
        dict = dict
    )
#@app.route('/loadData')
#def loadData():   
#    return render_template(       
#        'loadData.html',
#        title='Datos Generales',
#        titulo="Datos generales de tu empresa",
#        tarea="Datos generales",
#        formAnte = "AddPyme",
#        porcentaje ="02/05",
#        year=datetime.now().year,
#        dict = None
#    )

#@app.route('/loadCard')
#def loadCard():   
#    return render_template(       
#        'loadCard.html',
#        title='Selecciona tipo de cuenta', 
#        titulo="Elige la cuenta que más se acomoda a tus necesidades",
#        tarea="Tipo de Cuenta",
#        formAnte = "loadData",
#        porcentaje ="03/05",
#        year=datetime.now().year,
#    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/loadCard', methods=["GET", "POST"])
def loadCard():
    context={

    }
    return render_template('loadCard.html', **context)

@app.route('/loadDocument', methods=["GET", "POST"])
def loadDocument():

    cuenta = ""
    if request.form.get("cuentacorrienteempresa"):
        cuenta = "Cuenta Corriente Empresas"
    elif request.form.get("cuentaCorrienteremunerada"):
        cuenta = "Cuenta Corriente Remunerada"
    elif request.form.get("cuentaCorrientetradicional"):
        cuenta = "Cuenta Corriente Tradicional"
    elif request.form.get("cuentaahorroempresarial"):
        cuenta = "Cuenta de Ahorro Empresarial"
    elif request.form.get("cuentaahorrofijo"):
        cuenta = "Cuenta de Ahorro Fijo"
    elif request.form.get("cuentaahorrodiario"):
        cuenta = "Cuenta Ahorradiario"

    session["cuenta"] = cuenta

    doctoidentidadvis = "hidden"
    loadFiles()

    return render_template(
        'loadDocument.html',
        title='About',
        titulo="Has seleccionado " + cuenta + ". Por favor sube los siguientes documentos",
        tarea="Documentos Oficiales",
        formAnte = "loadCard",
        porcentaje ="04/05",
        avance= "80%",
        year=datetime.now().year,
        file = session["file"],
        doctoidentidadvis=doctoidentidadvis)
    
    #if session.get('file') == True:
    #    print("variable de sesion")
    #    print(session["file"])
    #    return render_template(
    #    'loadDocument.html',
    #    title='About',
    #    titulo="Has seleccionado " + cuenta + ". Por favor sube los siguientes documentos",
    #    tarea="Documentos Oficiales",
    #    formAnte = "loadCard",
    #    porcentaje ="04/05",
    #    avance= "80%",
    #    year=datetime.now().year,
    #    file = session["file"],
    #    doctoidentidadvis=doctoidentidadvis
    #)
    #else:
    #    return render_template(
    #    'loadDocument.html',
    #    title='About',
    #    titulo="Has seleccionado " + cuenta + ". Por favor sube los siguientes documentos",
    #    tarea="Documentos Oficiales",
    #    formAnte = "loadCard",
    #    porcentaje ="04/05",
    #    avance= "80%",
    #    year=datetime.now().year,
    #    file = None,
    #    doctoidentidadvis=doctoidentidadvis)



    #print("datos a cargar en load document cuando file existe")
    #print(session.get('file'))
    #print(archivo)
    #return render_template(
    #    'loadDocument.html',
    #    title='About',
    #    titulo="Has seleccionado " + cuenta + ". Por favor sube los siguientes documentos",
    #    tarea="Documentos Oficiales",
    #    formAnte = "loadCard",
    #    porcentaje ="04/05",
    #    avance= "80%",
    #    year=datetime.now().year,
    #    file = archivo,
    #    doctoidentidadvis=doctoidentidadvis
    #)

def loadFiles():
    file = {}
    
    query = {"file" : {"$exists": "True"}, "folio" : 1234569789 }
    result = collection.find_one(query) #{"$and":[ {"file":{"$exists": True}}, {"folio":{"$eq": "1234569789"}}]})
    #collection.find(query)

    print("result")
    print(result)

    if result:
        query = {"folio": 1234569789}
        cursor = collection.find(query)
        print("cursor")
        print(cursor)
    
        if cursor:        
            for doc in cursor:         
                ##print(doc["file"]["name"])
                #file = doc["file"] 
                #if doc["file"] != None:
                #if "file" in doc:
                print(doc["file"]["tipo_docto"])
                if doc["file"]["tipo_docto"] == "Documento de Identidad":
                    file["doctoidentidadname"] = doc["file"]["name"]
                    file["doctoidentidadid"] = str(doc["file"]["_id"])
                    doctoidentidadvis = "visible"
                    session["file"] = file
        else:
            file = None
    else:
        session["file"] = None
        #print(file)


#@app.route('/saveRegimen', methods=["GET", "POST"])
#def saveRegimen():
#    if request.method == 'POST':
#        session['regimenopt'] = request.form.get('hdoptions') #request.form"flexRadioDefault")
#        #print(session['regimenopt'] )
        
#    return render_template(       
#        'loadData.html',
#        title='Datos Generales',
#        titulo="Datos generales de tu empresa",
#        tarea="Datos generales",
#        formAnte = "AddPyme",
#        porcentaje ="02/05",
#        year=datetime.now().year,
#        dict = None
#    )







@app.route("/saveDocto", methods=["GET", "POST"])


def saveDocto():
    context={

    }
    return render_template('spinner.html', **context)
 
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




#def delete():
#    fileId = ObjectId("6171bbed152b45b44fad4caa")
#    fs.delete(fileId); #delete(ObjectId(id));
#    return "delete"



def delete(_id, file_id):
    print("file_id: "+ file_id)
    collection.update_one({"_id": bson.ObjectId(_id)}, 
                           {
                               #"$push": {"file._id": bson.ObjectId(file_id)}
                               "$unset": {"file": { "_id": bson.ObjectId(file_id) }}
                                
                            })
    fs.delete(bson.ObjectId(file_id) ); 
    return "delete"




def download():
    id = "6172d9705e66ba9bc108b50e"
    grid_fs_file =  fs.get(ObjectId(id)) #fs.find_one({'filename': file_name})
    response = flask.Response(grid_fs_file.read())
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers["Content-Disposition"] = "attachment; filename={}".format("Paola.docx")
    return response


    
    #response = flask.Response(grid_fs_file.__iter__())
    #response.headers['Content-Type'] = 'application/octet-stream'
    #response.headers["Content-Disposition"] = "attachment; filename={}".format("C:\Proyectos\Proyectos\doctos\Paola.jpg")
    #return grid_fs_file




    #response = make_response(grid_fs_file.read())
    #response.headers['Content-Type'] = 'application/octet-stream'
    #response.headers["Content-Disposition"] = "attachment; filename={}".format("namefile")
    #return response


    ####file = fs.get(ObjectId(id)) #GridFS(getDBConnection().upload).get(ObjectId(id))
    #####print("file by objectID")
    #####print(file)
    #####response =  flask.Response(file)
    #####response['Content-Disposition'] = 'attachment; filename=%s' % str("Paola")
    #####response['Content-Length']      = file.length 
    ####response = flask.Response(file.__iter__())
    #####print(response)
    #####print("response")
    #####print(file.metadata)
    #####response.headers['content-type'] = file.metadata['content_type']
    #####print("content_type")
    ####response.content_length = file.length

    ####return response

def downloadDocument():
    if request.method == 'POST':
        #fsg = MotorGridFSBucket(database)
        file_id = "6171bbed152b45b44fad4caa"
        #file = open('C:\Proyectos\Proyectos\doctos\myfile.jpg','wb+')
        #fsg.download_to_stream(file_id, file)
        #file.seek(0)
        #contents = file.read()
       
    #downloadStream = gridFSBucket.openDownloadStream(fileId)
    #fileLength = downloadStream.getGridFSFile().getLength();
    #fs = GridFSBucket(database)
    # Get file to write to
    #if not os.path.exists('my_directory'):
    #    os.makedirs('my_directory')

    #file = open('C:\Proyectos\Proyectos\doctos','wb')
    #fs.download_to_stream_by_id("test_file", file)

#    ObjectId fileId = new ObjectId("60345d38ebfcf47030e81cc9");
#try (GridFSDownloadStream downloadStream = gridFSBucket.openDownloadStream(fileId)) {
#    int fileLength = (int) downloadStream.getGridFSFile().getLength();
#    byte[] bytesToWriteTo = new byte[fileLength];
#    downloadStream.read(bytesToWriteTo);
#    System.out.#println(new String(bytesToWriteTo, StandardCharsets.UTF_8));
#}
@app.route("/validateOTP")
def validateOTP():
    """Renders the validateOTP page."""
    return render_template(
            'validateOTP.html',
            title='Código',
            year=datetime.now().year,
            message='Security code validation'
        )

@app.route("/folio")
def folio():
    """Renders the folio page."""
    return render_template(
            'folio.html',
            title='Folio',
            year=datetime.now().year,
            message='Folio de sesion'
        )  

@app.route("/account", methods=['GET','POST'])
def account():
    context={

    }
    return render_template('account.html', **context)


@app.route("/spinner")
def spinner():
    """Renders the spinner page."""
    return render_template(
            'spinner.html',
            title='spinner',
            year=datetime.now().year,
            message='spinner de sesion'
        ) 

@app.route("/final")

def final():
    context={

    }
    return render_template('final.html', **context)