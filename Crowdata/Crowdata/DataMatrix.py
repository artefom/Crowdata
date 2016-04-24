"""
Хранит главный DataCell и обслуживает его
"""
class DataMatrix:
    
    def __init__(self,depth):
        
        self.socialData = []
        
        self.dataCell = DataCell(np.array([[55.92150795277898,37.371368408203125],
                                           [55.56747507540021,37.863006591796875]]))
        for i in range(depth):
            self.dataCell.deepen()
    
    def addRawInfoList(self,rawList):
        stats = 0
        for i in range(len(rawList)):
            if not (rawList[i] in self.socialData):
                #futher sorting weakrefs by cells
                coordinates = rawList[i].data['coordinates']
                if (self.dataCell.inBounds(coordinates)):
                    self.socialData.append(rawList[i])
                    self.dataCell.addRef(weakref.ref(rawList[i]),coordinates)
                    stats += 1
        print('allocated stats:',stats)