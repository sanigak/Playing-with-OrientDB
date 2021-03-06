import pyorient
import pymongo

#initializing Orient client
client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect("root", "tiger")
client.db_open("KevinBaconTEST", "root", "tiger")

#initializing Mongo client
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["KevinBacon"]
col = mydb["MoviesCOPY"]


#Creates all vertices
def makeVertices():

    all = col.find()


    for movie in all:
        cast = movie["cast"]
        title = movie["title"]


        for member in cast:

            title = str(title)
            title = title.strip("\"")
            title = title.strip("\\")
            title = title.strip(" ")
            title = title.replace("\"", "")
            title = title.replace(" - IMDb", "")
            title = title.replace(")", "")
            title = title.replace("(", "- ")
            

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

    allActors = actorSetORIENT()

    iterator = 1
    total = len(allActors)

    for actor in allActors:
        print(str(iterator) + "/" + str(total))
        iterator +=1
        client.command("CREATE EDGE SameActor from (SELECT FROM ActorNode where actor = \"" + actor + "\") TO ( SELECT FROM ActorNode where actor = \"" + actor + "\") CONTENT { \"length\": 0}")


def makeTitleEdges():
    
    allTitles = movieSetORIENT()

    iterator = 1

    total = len(allTitles)

    for title in allTitles:
        print(str(iterator) + "/" + str(total))
        iterator +=1
        client.command("CREATE EDGE SameMovie from (SELECT FROM ActorNode where movie = \"" + title + "\") TO ( SELECT FROM ActorNode where movie = \"" + title + "\") CONTENT { \"length\": 1}")


def actorSetMONGO():
    
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

def actorSetORIENT():
    
    outputList = []
    ans = client.query("select actor from ActorNode", 200000)
    for item in ans:
        outputList.append(item.oRecordData['actor'])
    finalList = set(outputList)
    return finalList

def movieSetMONGO():
    
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

def movieSetORIENT():
    
    outputList = []
    ans = client.query("select movie from ActorNode", 200000)
    for item in ans:
        outputList.append(item.oRecordData['movie'])
    finalList = set(outputList)
    return finalList

def actorCount(actor):
    

    ans = client.query("select count(actor) from ActorNode where actor = \"" + actor + "\"")
    for item in ans:
        return int(item.oRecordData['count'])

def actorDelete(actor):
    command = "delete vertex from ActorNode where actor = \"" + actor + "\""
    print(command)
    client.command(command)

def movieDelete(movie):
    command = "delete vertex from ActorNode where movie = \"" + movie + "\""
    print(command)
    client.command(command)

def purgeDB():
    actors = actorSetORIENT()
    tot = len(actors)
    iterator = 1

    for actor in actors:
        print(str(iterator) + "/" + str(tot))
        iterator +=1
        count = actorCount(actor)
        if count < 5:
            actorDelete(actor)
    pass
 
def actorSetORIENTandCOUNT():
    outputList = []
    ans = client.query("select count(*), actor from ActorNode group by actor", 200000)
    for item in ans:
        count = item.oRecordData['count']
        count = int(count)
        if count < 5:
            actor = item.oRecordData['actor']
            actor = str(actor)
            outputList.append(actor)

    finalList = set(outputList)
    return finalList

def movieSetORIENTandCOUNT():
    outputList = []
    ans = client.query("select count(*), movie from ActorNode group by movie", 200000)
    for item in ans:
        count = item.oRecordData['count']
        count = int(count)
        if count < 2:
            movie = item.oRecordData['movie']
            movie = str(movie)
            outputList.append(movie)

    finalList = set(outputList)
    return finalList

def newActorPurge():
    iterator = 1
    listy = actorSetORIENTandCOUNT()
    count = len(listy)
    for actor in listy:
        print(str(iterator) + "/" + str(count))
        iterator+=1
        actorDelete(actor)
    
def newMoviePurge():
    iterator = 1
    listy = movieSetORIENTandCOUNT()
    count = len(listy)
    for movie in listy:
        print(str(iterator) + "/" + str(count))
        iterator+=1
        movieDelete(movie)

#newActorPurge()
#newMoviePurge()

#makeActorEdges()
makeTitleEdges()