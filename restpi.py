#!flask/bin/python

from flask import Flask, jsonify, make_response, request, abort
from flask.ext.uuid import FlaskUUID
import socket
import json

app = Flask(__name__)
FlaskUUID(app)

networks = []
TCP_IP = '127.0.0.1'
TCP_PORT = 21003
BUFFER_SIZE = 2048
pipe_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send_to_pipe(method, data, url):
    jsonrpc = {
        'jsonrpc': '2.0',
        'id': '1234',
        'method': method,
        'params': {
            'data': data,
            'url': url
        }
    }
    pipe_socket.connect((TCP_IP, TCP_PORT))
    pipe_socket.send(json.dumps(jsonrpc).encode())   
    response = pipe_socket.recv(BUFFER_SIZE)
    print('Response {}'.format(response))
    pipe_socket.close()


@app.errorhandler(404)
def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/network', methods=['GET'])
def get_networks():
    return jsonify({'network': networks})

@app.route('/network/', methods=['GET'])
def get_networks_():
    return get_networks() 



@app.route('/network/<uuid:network_id>', methods=['GET'])
def get_network(network_id):
    net = [net for net in networks if net[':id'] == str(network_id)]
    if len(net) == 0:
        abort(404)
    return jsonify({'network': net[0]})

@app.route('/network/<uuid:network_id>/', methods=['GET'])
def get_network_(network_id):
    return get_network(network_id)


@app.route('/network/<uuid:network_id>/device/<uuid:device_id>', methods=['GET'])
def get_device(network_id, device_id):
    net = [net for net in networks if net[':id'] == str(network_id)]
    if len(net) == 0:
        abort(404)
    device = [device for device in net[0]['device'] if device[':id'] == str(device_id)]
    if len(device) == 0:
        abort(404)
    return jsonify({'device': device[0]})

@app.route('/network/<uuid:network_id>/device/<uuid:device_id>/', methods=['GET'])
def get_device_(network_id, device_id):
    return get_device(network_id, device_id)

@app.route('/device/<uuid:device_id>', methods=['GET'])
def get_device2(device_id):
    for network in networks:
        for device in network['device']:
            if device[':id'] == str(device_id):
                return jsonify({'device': device})

    abort(404)

@app.route('/device/<uuid:device_id>/', methods=['GET'])
def get_device2_(device_id):
    return get_device2(device_id)


@app.route('/network/<uuid:network_id>/device/<uuid:device_id>/value/<uuid:value_id>', methods=['GET'])
def get_value(network_id, device_id, value_id):
    net = [net for net in networks if net[':id'] == str(network_id)]
    if len(net) == 0:
        abort(404)
    device = [device for device in net[0]['device'] if device[':id'] == str(device_id)]
    if len(device) == 0:
        abort(404)
    value = [value for value in device[0]['value'] if value[':id'] == str(value_id)]
    if len(value) == 0:
        abort(404)
    return jsonify({'value': value[0]})

@app.route('/network/<uuid:network_id>/device/<uuid:device_id>/value/<uuid:value_id>/', methods=['GET'])
def get_value_(network_id, device_id, value_id):
    return get_value(network_id, device_id, value_id)

@app.route('/value/<uuid:value_id>', methods=['GET'])
def get_value2(value_id):
    for network in networks:
        for device in network['device']:
            for value in device['value']:
                if value[':id'] == str(value_id):
                    return jsonify({'value': value})
    abort(404)

@app.route('/value/<uuid:value_id>/', methods=['GET'])
def get_value2_(value_id):
    return get_value2(value_id)

@app.route('/network/<uuid:network_id>/device/<uuid:device_id>/value/<uuid:value_id>/state/<uuid:state_id>', methods=['GET'])
def get_state(network_id, device_id, value_id, state_id):
    net = [net for net in networks if net[':id'] == str(network_id)]
    if len(net) == 0:
        abort(404)
    device = [device for device in net[0]['device'] if device[':id'] == str(device_id)]
    if len(device) == 0:
        abort(404)
    value = [value for value in device[0]['value'] if value[':id'] == str(value_id)]
    if len(value) == 0:
        abort(404)
    state = [state for state in value[0]['state'] if state[':id'] == str(state_id)]
    if len(state) == 0:
        abort(404)

    return jsonify({'state': state[0]})


@app.route('/network/<uuid:network_id>/device/<uuid:device_id>/value/<uuid:value_id>/state/<uuid:state_id>/', methods=['GET'])
def get_state_(network_id, device_id, value_id, state_id):
    return get_state(network_id, device_id, value_id, state_id)

@app.route('/state/<uuid:state_id>', methods=['GET'])
def get_state2(state_id):
    for network in networks:
        for device in network['device']:
            for value in device['value']:
                for state in value['state']:
                    if state[':id'] == str(state_id):
                        return jsonify({'state': state})
    abort(404)

@app.route('/state/<uuid:state_id>/', methods=['GET'])
def get_state2_(state_id):
    return get_state2(state_id)


## ---------------------------- PUT --------------------------

@app.route('/network/<uuid:network_id>/device/<uuid:device_id>/value/<uuid:value_id>/state/<uuid:state_id>',methods=['PUT'])
def update_state(network_id, device_id, value_id, state_id):
    net = [net for net in networks if net[':id'] == str(network_id)]
    if len(net) == 0:
        abort(404)
    device = [device for device in net[0]['device'] if device[':id'] == str(device_id)]
    if len(device) == 0:
        abort(404)
    value = [value for value in device[0]['value'] if value[':id'] == str(value_id)]
    if len(value) == 0:
        abort(404)
    state = [state for state in value[0]['state'] if state[':id'] == str(state_id)]
    if len(state) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if not ':id' in request.json or not ':type' in request.json or not 'data' in request.json:
        abort(400)

    state[0]['data'] = request.json['data']

    url = '/network/{network_id}/device/{device_id}/value/{value_id}/state/{state_id}'
    send_to_pipe('PUT', request.json, url) 

    return jsonify({'state': state[0]})

@app.route('/network/<uuid:network_id>/device/<uuid:device_id>/value/<uuid:value_id>/state/<uuid:state_id>/',methods=['PUT'])
def update_state_(network_id, device_id, value_id, state_id):
    return update_state(network_id, device_id, value_id, state_id)


@app.route('/state/<uuid:state_id>',methods=['PUT'])
def update_state2(state_id):
    if not ':id' in request.json or not ':type' in request.json or not 'data' in request.json:
        abort(400)
    for network in networks:
        for device in network['device']:
            for value in device['value']:
                for state in value['state']:
                    if state[':id'] == str(state_id):
                        state['data'] = request.json['data']
                        url = '/network/' + network[':id'] + '/device/' + device[':id'] + '/value/' + value[':id'] + '/state/' + state[':id'] 
                        send_to_pipe(method='PUT', data=request.json, url=url)
                        return jsonify({'state': state})
    abort(404)

@app.route('/state/<uuid:state_id>/',methods=['PUT'])
def update_state2_(state_id):
    return update_state2(state_id)



### --------------- POST -------------------------
@app.route('/network', methods=['POST'])
def create_network():
    if not request.json:
        print('It iss not a JSON')
        abort(400)
    if not ':id' in request.json or not ':type' in request.json:
        print('Missing ":id" or ":type" in JSON request')
        abort(400)
    network = {
        ':id': request.json[':id'],
        ':type': request.json[':type'],
        'device': []
    }
    networks.append(network)
    return jsonify({'network': network}), 201

@app.route('/network/', methods=['POST'])
def create_network_():
    return create_network()

@app.route('/network/<uuid:network_id>/device', methods=['POST'])
def create_device(network_id):
    net = [net for net in networks if net[':id'] == str(network_id)]
    if len(net) == 0:
        print("Not found network_id {} ", network_id)
        abort(404)
    if not request.json or not ':id' in request.json or not ':type' in request.json:
        print("Not found ':id' or ':type' in json")
        abort(404)

    name = request.json['name'] if 'name' in request.json else "" 
    manufacturer = request.json['manufacturer'] if 'manufacturer' in request.json else ""
    product = request.json['product'] if 'product' in request.json else ""
    version = request.json['version'] if 'version' in request.json else ""
    serial = request.json['serial'] if 'serial' in request.json else ""
    description = request.json['description'] if 'description' in request.json else ""
    protocol = request.json['protocol'] if 'protocol' in request.json else ""
    communication = request.json['communication'] if 'communication' in request.json else ""
    included = request.json['included'] if 'included' in request.json else ""

    device = {
        ':id': request.json[':id'],
        ':type': request.json[':type'],
        'name': name,
        'manufacturer': manufacturer,
        'product': product,
        'version': version,
        'serial': serial,
        'description': description,
        'protocol': protocol,
        'communication': communication,
        'included': included,
        'value': []
    }
    net[0]['device'].append(device)
    return jsonify({'device': device}), 201

@app.route('/network/<uuid:network_id>/device/', methods=['POST'])
def create_device_(network_id):
    return create_device(network_id)



@app.route('/network/<uuid:network_id>/device/<uuid:device_id>/value', methods=['POST'])
def create_value(network_id, device_id):
    net = [net for net in networks if net[':id'] == str(network_id)]
    if len(net) == 0:
        abort(404)
    device = [device for device in net[0]['device'] if device[':id'] == str(device_id)]
    if len(device) == 0:
        abort(404)
    if not request.json or not ':id' in request.json or not ':type' in request.json:
        print("Not found ':id' or ':type' in json")
        abort(404)

    name = request.json['name'] if 'name' in request.json else ''
    permission = request.json['permission'] if 'permission' in request.json else ''
    value_type = request.json['type'] if 'type' in request.json else ''
    number = request.json['number'] if 'number' in request.json else ''
    if number:
        number_min = request.json['number']['min']
        number_max = request.json['number']['max']
        number_step = request.json['number']['step']
        number_unit = request['number']['unit'] if 'unit' in request.json['number'] else ''

    #string = request.json['string'] if 'string' in request.json else ''
    # TODO
    value = {
        ':id': request.json[':id'],
        ':type':  request.json[':type'],
        'name': name,
        'permission': permission,
        'type': value_type,
        'number': {
            'min': number_min,
            'max': number_max,
            'step': number_step,
            'unit': number_unit
        },
        'state': []
    }
    device[0]['value'].append(value)
    return jsonify({'value': value}), 201

@app.route('/network/<uuid:network_id>/device/<uuid:device_id>/value/', methods=['POST'])
def create_value_(network_id, device_id):
    return create_value(network_id, device_id)


@app.route('/network/<uuid:network_id>/device/<uuid:device_id>/value/<uuid:value_id>/state', methods=['POST'])
def create_state(network_id, device_id, value_id):
    net = [net for net in networks if net[':id'] == str(network_id)]
    if len(net) == 0:
        abort(404)
    device = [device for device in net[0]['device'] if device[':id'] == str(device_id)]
    if len(device) == 0:
        abort(404)
    value = [value for value in device[0]['value'] if value[':id'] == str(value_id)]
    if len(value) == 0:
        abort(404)

    state = {
        ':id': request.json[':id'],
        ':type': request.json[':type'],
        'type': request.json['type'],
        'timestamp': request.json['timestamp'],
        'data': request.json['data']
    }
    value[0]['state'].append(state)
    return jsonify({'state': state}), 201

@app.route('/network/<uuid:network_id>/device/<uuid:device_id>/value/<uuid:value_id>/state/', methods=['POST'])
def create_state_(network_id, device_id, value_id):
    return create_state(network_id, device_id, value_id)


if __name__ == '__main__':
    app.run(debug=True)


