import pyorient
import pymongo

#initializing Orient client
client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect("root", "tiger")

#initializing Mongo client
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["KevinBacon"]
col = mydb["MoviesCOPY"]


#Creates all vertices
def makeVertices():

    all = col.find()

    client.db_open("KevinBacon", "root", "tiger")

    for movie in all:
        cast = movie["cast"]
        title = movie["title"]


        for member in cast:

            title = str(title)
            title = title.strip("\"")
            title = title.strip("\\")
            title = title.strip(" ")
            title = title.replace("\"", "")

            role = str(cast[member])
            role = role.strip("\"")
            role = role.strip("\\")
            role = role.strip(" ")
            role = role.replace("\"", "")

            member = str(member)
            member = member.strip("\"")
            member= member.strip("\\")
            member = member.strip(" ")
            member = member.replace("\"", "")

            


            try:
                 client.command("CREATE VERTEX ActorNode CONTENT { \"actor\" : \"" + member + "\", \"role\" : \"" + role + "\", \"movie\" : \"" + title + "\" }")

            except:
                 print("FAIL")

    pass

def makeActorEdges():
    client.db_open("KevinBacon", "root", "tiger")

    allActors = actorSet()

    iterator = 1
    total = len(allActors)

    for actor in allActors:
        print(str(iterator) + "/" + str(total))
        iterator +=1
        client.command("CREATE EDGE SameActor from (SELECT FROM ActorNode where actor = \"" + actor + "\") TO ( SELECT FROM ActorNode where actor = \"" + actor + "\") CONTENT { \"length\": 0}")


def makeTitleEdges():
    client.db_open("KevinBacon", "root", "tiger")

    allTitles = movieSet()

    iterator = 1

    total = len(allTitles)

    for title in allTitles:
        print(str(iterator) + "/" + str(total))
        iterator +=1
        client.command("CREATE EDGE SameMovie from (SELECT FROM ActorNode where movie = \"" + title + "\") TO ( SELECT FROM ActorNode where movie = \"" + title + "\") CONTENT { \"length\": 1}")


def actorSet():
    
    outputList = []

    all = col.find()

    for movie in all:
        cast = movie["cast"]

        for member in cast:
            member = str(member)
            member = member.replace("\"", "")
            member = member.replace("\\", "")
            member = member.strip(" ")
            outputList.append(member)
    
    finalList = set(outputList)

    return finalList

def movieSet():
    
    outputList = []

    all = col.find()

    for movie in all:
        title = movie["title"]
        title = str(title)
        title = title.strip("\"")
        title = title.strip("\\")
        title = title.strip(" ")
        title = title.replace("\"", "")
        outputList.append(title)
    
    finalList = set(outputList)

    return finalList

makeTitleEdges()