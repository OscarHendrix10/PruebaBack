from flask import Flask, request
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@localhost/pruebaits'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

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

db.create_all()

class ConductoresSchema(ma.Schema):
    class Meta:
        fields = ('idConductor','nombreCompleto','puesto','departamento',
                  'tipoLicencia','edad','fechaIngreso','antiguedad','ubicacion')

task_schema = ConductoresSchema()
tasks_schema = ConductoresSchema(many=True)


@app.route('/agregar', methods=['POST'])
def create():
       nombre = request.json["nombreCompleto"],
       puesto = request.json["puesto"],
       departamento = request.json["departamento"],
       tipoLicencia = request.json["tipoLicencia"],
       edad = request.json["edad"],
       fechaIngreso = request.json["fechaIngreso"],
       antiguedad = request.json["antiguedad"],
       ubicacion = request.json["ubicacion"]
       
       new_conductor = Conductores(nombre, puesto, departamento, tipoLicencia, 
                                         edad, fechaIngreso, antiguedad, ubicacion)
       db.session.add(new_conductor)
       db.session.commit()
       return task_schema.jsonify(new_conductor)
   
@app.route('/consultar', methods=['GET'])
def Conusltar():
    all_conductores = Conductores.query.all()
    result =  tasks_schema.dump(all_conductores)
    return jsonify(result)

@app.route('/buscar/<id>', methods=['GET'])
def buscar(id):
    conductor = Conductores.query.get(id)
    return task_schema.jsonify(conductor)
    
@app.route('/editar/<id>', methods=['PUT'])
def editar(id):
    conductor = Conductores.query.get(id)
    
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
    
    db.session.commit()
    return task_schema.jsonify(conductor)

@app.route('/eliminar/<id>', methods=['DELETE'])
def delete(id):
    conductor = Conductores.query.get(id)
    db.session.delete(conductor)
    db.session.commit()
    return task_schema.jsonify(conductor)


if __name__ == "__main__":
    app.run(debug=True)