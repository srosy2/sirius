from flask import Flask, request, session, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import pandas as pd
import json
from run import run


UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['doc', 'docx', 'pdf', 'txt'])

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload/current/<int:id>', methods=['POST'])
def fileUpload(id):

    target=os.path.join(UPLOAD_FOLDER,'current/train_data')

    for f in os.listdir("/".join([app.root_path, target])):
        os.remove("/".join([app.root_path, os.path.join(target, f)]))

    for file in request.files.getlist("competentions"):
        filename = secure_filename(file.filename)
        destination = "/".join([app.root_path, target, filename])
        file.save(destination)

    session['uploadFilePath'] = destination
    competentions = getGraphDataGpn(id)

    for f in os.listdir("/".join([app.root_path, target])):
        os.remove("/".join([app.root_path, os.path.join(target, f)]))

    for file in request.files.getlist("needs"):
        filename = secure_filename(file.filename)
        destination = "/".join([app.root_path, target, filename])
        file.save(destination)

    session['uploadFilePath'] = destination
    needs = getGraphDataGpn(id)

    with open(os.path.abspath("./gpn.json"), "r") as f:
        ontology = json.load(f)

    routes = []
    tmp_nodes = needs["nodes"][:]
    for node in competentions["nodes"]:
        if node in tmp_nodes:
            tmp_nodes.remove(node)

    tmp_edges = needs["edges"][:]
    for edge in competentions["edges"]:
        if edge not in tmp_edges:
            tmp_edges.append(edge)
    tmp = {"nodes": tmp_nodes, "edges": tmp_edges}
    for start in competentions["nodes"]:
        route = []
        getRoute(start, tmp, route)
        if len(route) > 1:
            routes.append(route)

    obj = {
        "competentions": competentions,
        "needs": needs,
        "routes": routes
    }

    return jsonify(obj)


def getGraphDataGpn(terminology):
    filepath = "./gpn.json"
    if terminology == 1:
        filepath = "./tpu.json"

    run({'path': '/uploads/current/train_data', 'type_file': 'doc', 'type': 'doc'}, {'path': '/uploads/current/'
                                                                                             'termin_train',
                                                                    'type_file': 'txt', 'type': 'term'}, terminology)

    df = pd.read_csv("./doc_term.csv")
    nodes_id = []
    nodes = []
    edges = []

    for i in df.index:
        for j in df.columns:
            if df.loc[i, j] < 0.25 and df.loc[i, j] != 0:
                nodes_id.append(int(j))

    nodes_id = list(set(nodes_id))

    with open(os.path.abspath(filepath), "r") as f:
        data = json.load(f)

    for edge in data["edges"]:
        if int(edge["from"]) in nodes_id and int(edge["to"]) in nodes_id:
            if edge["from"] != edge["to"]:
                edges.append(edge)

    for id in nodes_id:
        for node in data["nodes"]:
            if node["id"] == id:
                nodes.append(node)

    return {"edges": edges, "nodes": nodes}

def getNodeById(id, ontology):
    for node in ontology["nodes"]:
        if node["id"] == id:
            return node

def getNodeEdgesById(id, data):
    edges = []
    for edge in data["edges"]:
        if edge["from"] == id or edge["to"] == id:
            edges.append(edge)

    return edges

def getNodeChildren(id, data):
    children = []
    edges = data["edges"]
    nodes = data["nodes"]
    for edge in edges:
        if int(edge["from"]) == id or int(edge["to"]) == int(id):
            child_id = int(edge["from"]) if int(edge["from"]) != int(id) else int(edge["to"])
            for node in nodes:
                if int(node["id"]) == child_id:
                    if node not in children:
                        children.append(node)
    return children

def getRoute(node, data, path):
    if node in path:
        return
    path.append(node)
    for child in getNodeChildren(node["id"], data):
        getRoute(child, data, path)


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run()