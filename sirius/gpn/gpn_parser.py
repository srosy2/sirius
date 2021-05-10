from owlready2 import *
import json
import random
import re

def randomColor():
    r = lambda: random.randint(0, 255)
    return '#%02X%02X%02X' % (r(), r(), r())


def parseProperies(cl, instance, depth=0, color=None):
    global text, nodes, edges, iterator, urls, colors

    if depth > 2:
        return

    if urls.get(instance.name) != None:

        if urls.get(cl.name) != None and depth != 0:
            edges.append({
                "from": int(urls[cl.name]),
                "to": int(urls[instance.name])
            })

    else:
        if color != None:
            nodes.append({
                "id": iterator,
                "label": instance.prefLabel[0],
                "color": color
            })
        else:
            color = randomColor()
            colors.append(color)
            nodes.append({
                "id": iterator,
                "label": instance.prefLabel[0],
                "color": color
            })

        if urls.get(cl.name) != None and depth != 0:
            edges.append({
                "from": int(urls[cl.name]),
                "to": int(iterator)
            })
        urls[instance.name] = iterator

        label = instance.prefLabel[0].replace(".", "")
        text += f"\n{label} $ {iterator}"

        iterator += 1


    for prop in list(instance.get_properties()):
        key = str(prop).split(".")[1]

        if key not in {"prefLabel", "topConceptOf", "inScheme", "hasTopConcept"}:
            obj = eval(f"instance.{key}[0]")
            parseProperies(cl=instance, instance=obj, depth=depth + 1, color=color)


text = ""
nodes = []
edges = []
urls = {}
colors = []
dcolors = {}
iterator = 0

onto = get_ontology("file:///home/sirius/DELETEME/sirius/files/result_ontology.owl")
onto.load()

classes = list(onto.classes())

for cl in classes:
    index = classes.index(cl)
    print(f"{index}/{len(classes)}")

    nodes.append({
        "id": iterator,
        "label": cl.name,
        "color": "#ff0000"
    })
    urls[cl.name] = iterator

    label = cl.name.replace(".", "")
    text += f"\n{label} $ {iterator}"

    iterator += 1

    instances = cl.instances()
    for instance in instances:
        parseProperies(cl, instance)

text = set(text.split("\n"))
text = '\n'.join(text)

for i in edges:
    a = i["from"]
    b = i["to"]
    color = None

    if dcolors.get(a) != None:
        color = dcolors[a]

    if dcolors.get(b) != None:
        color = dcolors[b]

    if color == None:
        color = randomColor()

    dcolors[a] = color
    dcolors[b] = color

    for j in nodes:
        if j["id"] == a or j["id"] == b:
            j["color"] = color

obj = {
    "nodes": nodes,
    "edges": edges
}

with open('gpn.json', 'w') as fp:
    json.dump(obj, fp, indent=4, ensure_ascii=False)

with open('gpn.txt', 'w') as f:
    f.write(text)

print("Done")
print(len(colors))
