from geopy. geocoders import Nominatim
from geopy import distance
import time



# Code snippet or function you want to measure




def calcdistance(city1,city2):
    geolocator = Nominatim (user_agent="geoapiExercises")

    l1  = geolocator.geocode (city1)
    l2 = geolocator.geocode (city2)

    loc1 = (l1.latitude, l1.longitude)
    loc2 = (l2.latitude, l2. longitude)


    print(loc1,loc2,sep="/")
    dis = str(distance.distance(loc1,loc2))
    dis = round(float(dis.replace("km","")),3)

    return dis



def dis(c1,c2):
    location = {
        "Thalassery":(11.83565105, 75.64490544488862),
        "Kannur":(11.8763836, 75.3737973)
    }

    loc1 = location[c1]
    loc2 = location[c2]

    return distance.distance(loc1,loc2)

start_time = time.time()
print(calcdistance("Thalassery","Kannur"))
end_time = time.time()

execution_time = end_time - start_time

print(execution_time)