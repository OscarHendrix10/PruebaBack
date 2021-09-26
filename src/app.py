#importacion de clases flask para el consumop de APIS 
from flask import Flask, request
from flask.json import jsonify
#importacion de SQLAlchemy para la conexion a la base de datos 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

#iniciamos la aplicacion web
app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Conexion a la base de datos con usuario contraseña servidor y base de datos 
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@localhost/pruebaits'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

#intanciamos una variable de sqlalchemy y marhmellow 
db = SQLAlchemy(app)
ma = Marshmallow(app)

#creamos la clase de consuctores que en si es nuestra tabla a la base de datos por
#lo cual no es nesesario crear la query en MySql 
class Conductores(db.Model):
    __tablename__ = 'conductores'
    idConductor = db.Column(db.Integer, primary_key=True)
    nombreCompleto = db.Column(db.String(200))
    puesto = db.Column(db.String(50))
    departamento = db.Column(db.String(50))
    tipoLicencia = db.Column(db.String(50))
    edad = db.Column(db.Integer)
    fechaIngreso = db.Column(db.String(25))
    antiguedad = db.Column(db.Integer)
    ubicacion = db.Column(db.String(150))
    
    #definimos el contructor
    def __init__(self, nombreCompleto, puesto, departamento, tipoLicencia,
                 edad, fechaIngreso, antiguedad, ubicacion):
        
        self.nombreCompleto = nombreCompleto
        self.puesto = puesto
        self.departamento = departamento
        self.tipoLicencia = tipoLicencia
        self.edad = edad
        self.fechaIngreso = fechaIngreso
        self.antiguedad = antiguedad
        self.ubicacion = ubicacion
        
#creamos la tabla de conductores 
db.create_all()

#reacmos un metodo svhema para aginar los parametros que vamos a recibir
class ConductoresSchema(ma.Schema):
    class Meta:
        fields = ('idConductor','nombreCompleto','puesto','departamento',
                  'tipoLicencia','edad','fechaIngreso','antiguedad','ubicacion')

task_schema = ConductoresSchema()
tasks_schema = ConductoresSchema(many=True)

#primera ruta para incertar en la base de datatos dandole el metodo post 
@app.route('/agregar', methods=['POST'])
#cracion del metodo para el consumo de la API
def create():
       nombre = request.json["nombreCompleto"],
       puesto = request.json["puesto"],
       departamento = request.json["departamento"],
       tipoLicencia = request.json["tipoLicencia"],
       edad = request.json["edad"],
       fechaIngreso = request.json["fechaIngreso"],
       antiguedad = request.json["antiguedad"],
       ubicacion = request.json["ubicacion"]
       # el contructor recibe los parametroa y lo guardamos en una variable 
       new_conductor = Conductores(nombre, puesto, departamento, tipoLicencia, 
                                         edad, fechaIngreso, antiguedad, ubicacion)
       #agregamos el contructor en la bd
       db.session.add(new_conductor)
       db.session.commit()
       #retornamos el json que recibimos en la peticion 
       return task_schema.jsonify(new_conductor)
 
 #metodo para consultar todos los registros existente en la bd  
@app.route('/consultar', methods=['GET'])
def Conusltar():
    #consulta de Select * from conductores
    all_conductores = Conductores.query.all()
    result =  tasks_schema.dump(all_conductores)
    #returna un json con todos los parametros
    return jsonify(result)

#metodo para buscar el registro exixtenete en la bd buscando por el id del conductor
@app.route('/buscar/<id>', methods=['GET'])
def buscar(id):
    #generamos una variable para el resultado que nos arrogara el en el conductor
    conductor = Conductores.query.get(id)
    return task_schema.jsonify(conductor)
    
#metodo para editar los registros del conductor en la base de datos
@app.route('/editar/<id>', methods=['PUT'])
def editar(id):
    #amlacenamos la variable que nos trae el get.
    conductor = Conductores.query.get(id)
    #hacemos el resquest n json para insercion de datos
    nombre = request.json["nombreCompleto"],
    puesto = request.json["puesto"],
    departamento = request.json["departamento"],
    tipoLicencia = request.json["tipoLicencia"],
    edad = request.json["edad"],
    fechaIngreso = request.json["fechaIngreso"],
    antiguedad = request.json["antiguedad"],
    ubicacion = request.json["ubicacion"]
    
    conductor.nombreCompleto = nombre,
    conductor.puesto = puesto,
    conductor.departamento = departamento,
    conductor.tipoLicencia = tipoLicencia,
    conductor.edad = edad,
    conductor.fechaIngreso = fechaIngreso,
    conductor.antiguedad = antiguedad,
    conductor.ubicacion = ubicacion
    #gusrdamos los cambios 
    db.session.commit()
    #retornamos el json modificado
    return task_schema.jsonify(conductor)

#metodo para eliminar todos los registros de la base de datos de un conductor
@app.route('/eliminar/<id>', methods=['DELETE'])
def delete(id):
    
    conductor = Conductores.query.get(id)
    db.session.delete(conductor)
    db.session.commit()
    return task_schema.jsonify(conductor)

#metodo para levantar el servidor local
if __name__ == "__main__":
    app.run(debug=True)