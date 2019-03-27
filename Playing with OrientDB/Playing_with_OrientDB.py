import pyorient

client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect("root", "tiger")

client.shutdown('root', 'tiger')

