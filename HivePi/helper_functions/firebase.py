def pushTemps(db, outside, inside, base):
	db.child("hives").child(1).child("values").child(now).child("temperature").child("outside").set(25)
	db.child("hives").child(1).child("values").child(now).child("temperature").child("inside").set(20)
	db.child("hives").child(1).child("values").child(now).child("temperature").child("base").set(24.3)

def pushHumidity(db, outside, inside, base):
	hive_db.child("hives").child(1).child("values").child(now).child("humidity").child("outside").set(75)
	hive_db.child("hives").child(1).child("values").child(now).child("humidity").child("inside").set(80)
	hive_db.child("hives").child(1).child("values").child(now).child("humidity").child("base").set(76)
	
def pushPressure(db, pressure):
