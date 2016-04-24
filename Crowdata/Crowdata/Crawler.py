"""
Сборщик инфы с инстаграмма
"""
class Crawler:
    
    ACCESS_TOKEN = "1214212227.1fb234f.2958fdcfdd264e67b94606cfb89fef04"
    
    def __init__(self):
        self.responses = None
        self.aggregatedresponses = None
        self.success = None
    
    def crawl(self,coordinates):
        
        latres = 10
        lngres = 10
        
        lat_dist = geoDistance(coordinates[0],(coordinates[1][0],coordinates[0][1]))*1000 # height in meters
        lng_dist = geoDistance(coordinates[0],(coordinates[0][0],coordinates[1][1]))*1000 # width in meters
        
        print('lat dist:',lat_dist)
        print('lng dist:',lng_dist)
        
        dist = 5000 #circle radius in meters
        latres = math.ceil(lat_dist/(dist*2*0.7))
        lngres = math.ceil(lat_dist/(dist*2*0.7))
        
        print('latres:',latres)
        print('lngres:',lngres)
        
        latSubdiv = np.linspace(*coordinates[:,0],\
                                num=latres,\
                                endpoint=True)
        lngSubdiv = np.linspace(*coordinates[:,1],\
                                num=lngres,\
                                endpoint=True)
        
        self.success = np.zeros((latres,lngres),dtype=bool)
        self.responses = np.zeros((latres,lngres),dtype=object)
        self.aggregatedresponses = np.zeros((latres,lngres),dtype=object)
        
        total = latres*lngres
        count = 0
        for row,lat in enumerate(latSubdiv):
            for col,lng in enumerate(lngSubdiv):
                count += 1
                print 'processing',count,'out of',total
                self.responses[row,col] = getMediaByCoordinates(lat,lng,dist)
                self.aggregatedresponses[row,col] = RawInfo_instagram.listFromResponse(self.responses[row,col])
                time.sleep(0.1)
                ok = self.responses[row,col].ok
                if ok:
                    print 'OK' 
                else:
                    print 'Fail' 
                self.success[row,col] = ok
                
        #mediaResponse = self.getMediaByCoordinates(lat,lng,dist=5000)
        #RawInfoLst = RawInfo_instagram.listFromResponse(mediaResponse)
        #pass
    
    @staticmethod
    def getMediaByCoordinates(lat, lng, dist = 5000):
        return requests.get("https://api.instagram.com/v1/media/search?"+\
                            "lat="+str(lat)+\
                            "&lng="+str(lng)+\
                            "&distance="+str(dist)+\
                            "&access_token="+ACCESS_TOKEN)