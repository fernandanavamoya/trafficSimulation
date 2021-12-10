from model import *
from flask import Flask, request, jsonify
from agent import *

numberCars = 1
trafficModel = None
currentStep = 0
width = 0
height = 0

with open("base.txt") as baseFile:
    lines = baseFile.readlines()
    width = len(lines[0])-1
    height = len(lines)

app = Flask("Traffic Model")

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global currentStep, trafficModel, numberCars
    
    if request.method == 'POST':
        # pide variables al servidor
        numberCars = int(request.form.get('NAgents'))
        maxIterations = int(request.form.get('maxIterations'))
        currentStep = 0 # se inicializa en 0 porque no ha empezado la simulación

        print(request.form)
        print(numberCars)
        # crea un objeto el model de BoxRobot
        trafficModel = RandomModel(numberCars, maxIterations)

        return jsonify({"message":"Parameters recieved, model initiated."})

# obtiene la posición de los agentes tipo Car
@app.route('/getCars', methods=['GET'])
def getCars():
    global trafficModel
    if request.method == 'GET':
        carPositions = []
        for (a, x, z) in trafficModel.grid.coord_iter():
            for b in a:
                if isinstance(b, Car):
                    carPositions.append({"x": x, "y":0, "z":z, "w":b.unique_id})
        print(carPositions)
        return jsonify({'positions': carPositions})

# obtiene la posición y el estado de los agentes tipo Traffic_Light
@app.route('/getTrafficLights', methods=['GET'])
def getTrafficLights():
    global trafficModel

    if request.method == 'GET':
        # busca la posición de los destinos
        trafficLightPositions = [{"x": x, "y":1, "z":z, "state":a.state} for (a, x, z) in trafficModel.grid.coord_iter() if isinstance(a, Traffic_Light)]
        # regresa estas posiciones a Unity
        return jsonify({'positions': trafficLightPositions})

@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, trafficModel
    if request.method == 'GET':
        if trafficModel.running == True:
            trafficModel.step()
            currentStep += 1
            return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})
        else:
            return jsonify({'message':f'Model running == False'})

if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)