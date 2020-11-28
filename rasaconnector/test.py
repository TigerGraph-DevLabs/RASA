import pyTigerGraph as tg

#######################################""
configs = {
    "host": "https://<your_box>.i.tgcloud.io",
    "password": "<your_password>",
    "graphname": "<your_graph>",
    "secret" : "<your_secret>"
    }
#######################################"




conn = tg.TigerGraphConnection(host=configs['host'], password=configs['password'], gsqlVersion="3.0.5", useCert=True, graphname=configs['graphname'])
conn.apiToken = conn.getToken(configs['secret'])
conn.gsql("USE graph {}".format(configs['graphname']))
#######################################"

def nlu_md():
    res = conn.gsql("SELECT type,intent,value FROM nlu LIMIT 100")
    intent = ""
    nlus = {}
    order = []
    for element in res:
        order.append(element["v_id"])
    order = sorted([int(x) for x in order])
    for element in order:
        for e in res:
            if int(e["v_id"]) == element:
                if e["attributes"]["intent"] in nlus:
                    nlus[e["attributes"]["intent"]].append(e["attributes"]["value"])
                else:
                    nlus[e["attributes"]["intent"]] = [e["attributes"]["value"]]
                break
    f = open("nlu.md","w")
    for intent in nlus:
        f.write("## intent:{}\n".format(intent))
        for value in nlus[intent]:
            f.write(" - {}\n".format(value))
    f.close()


def stories_md():
    res = conn.gsql("SELECT type,info,intent,value FROM stories LIMIT 100")
    info = ""
    intent = ""
    f = open("stories.md","w")
    story = {}
    order = []
    for element in res:
        order.append(element["v_id"])
    order = sorted([int(x) for x in order])
    for element in order:
        for e in res:
            if int(e["v_id"]) == element:
                if e["attributes"]["info"] in story:
                    if e["attributes"]["intent"] in story[e["attributes"]["info"]]:
                        story[e["attributes"]["info"]][e["attributes"]["intent"]].append(e["attributes"]["value"])
                    else:
                        story[e["attributes"]["info"]][e["attributes"]["intent"]] = [e["attributes"]["value"]]
                else:
                    story[e["attributes"]["info"]] = {e["attributes"]["intent"]:[e["attributes"]["value"]]}
                break
    for info in story:
        f.write("## {}\n".format(info))
        for intent in story[info]:
            f.write("* {}\n".format(intent))
            for value in story[info][intent]:
                f.write(" - {}\n".format(value))      
    f.close()






def nlu_yml():
    res = conn.gsql("SELECT type,intent,value FROM nlu LIMIT 100")
    intent = ""
    nlus = {}
    order = []
    for element in res:
        order.append(element["v_id"])
    order = sorted([int(x) for x in order])
    for element in order:
        for e in res:
            if int(e["v_id"]) == element:
                if e["attributes"]["intent"] in nlus:
                    nlus[e["attributes"]["intent"]].append(e["attributes"]["value"])
                else:
                    nlus[e["attributes"]["intent"]] = [e["attributes"]["value"]]
                break
    f = open("nlu.yml","w")
    f.write('version: "2.0"\n')
    f.write("nlu:\n")
    for intent in nlus:
        f.write("- intent: {}\n".format(intent))
        f.write("  examples: |\n")
        for value in nlus[intent]:
            f.write(" - {}\n".format(value))
    f.close()


def stories_yml():
    res = conn.gsql("SELECT type,info,intent,value FROM stories LIMIT 100")
    info = ""
    intent = ""
    f = open("stories.yml","w")
    story = {}
    order = []
    f.write('version: "2.0"\n')
    f.write("stories:\n")
    for element in res:
        order.append(element["v_id"])
    order = sorted([int(x) for x in order])
    for element in order:
        for e in res:
            if int(e["v_id"]) == element:
                if e["attributes"]["info"] in story:
                    if e["attributes"]["intent"] in story[e["attributes"]["info"]]:
                        story[e["attributes"]["info"]][e["attributes"]["intent"]].append(e["attributes"]["value"])
                    else:
                        story[e["attributes"]["info"]][e["attributes"]["intent"]] = [e["attributes"]["value"]]
                else:
                    story[e["attributes"]["info"]] = {e["attributes"]["intent"]:[e["attributes"]["value"]]}
                break
    for info in story:
        f.write("-story: {}\n".format(info))
        f.write("  steps:\n")
        for intent in story[info]:
            f.write("  - intent: {}\n".format(intent))
            for value in story[info][intent]:
                f.write("  - action: {}\n".format(value))      
    f.close()


################### RUN YML ##############"
nlu_yml()
stories_yml()


################### RUN MD ##############"
nlu_md()
stories_md()





