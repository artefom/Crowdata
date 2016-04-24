
"""
Основной элемент(класс) многослойной рекурентной матрицы.
Поддерживает добавление элементов и извлечение n-го подслоя

self.depth - глубина
self.resolution - размер матрицы подклеток
self.items - массив всех элементов, содержащихся в подклетках данной клетки
self.coordinates - координаты клетки [[topleft_lat,topleft_lng],[btmright_lat,btmright_lng]]
"""
class DataCell:
    
    def __init__(self, coordinates):
        #[[topleft_lat,topleft_lng],[btmright_lat,btmright_lng]]
        #lattitude decrease gradient: from top to bottom
        #longitude decrease gradient: from right to left
        self.coordinates = coordinates
        self.resolution = 2
        self.depth = 0
        self.items = [] #items, contained in all subcells
        self.subcells = None
                                    
    """
    Углубить клетку на 1 слой
    """                
    def deepen(self): #make datacell more deep
        if (self.depth == 0 or self.subcells == None):
            self.depth = 1   
            latSubdiv = np.linspace(*self.coordinates[:,0],\
                                    num=self.resolution+1,\
                                    endpoint=True)
            lngSubdiv = np.linspace(*self.coordinates[:,1],\
                                    num=self.resolution+1,\
                                    endpoint=True)
            self.subcells = [[DataCell( np.fliplr(np.array([lngSubdiv[j:j+2],latSubdiv[i:i+2]]).T) ) for j in range(self.resolution)] \
                             for i in range(self.resolution)]
            return
        
        self.depth+=1
        for row in range(len(self.subcells)):
            for column in range(len(self.subcells[row])):
                self.subcells[row][column].deepen()
        
    
    """
    Уменьшить глубину на 1
    """
    def shallowen(self): #make datacell more shallow
        if (self.depth == 0):
            return
        if (self.depth == 1):
            self.depth = 0
            self.subcells = None
            return
        for row in range(len(self.subcells)):
            for column in range(len(self.subcells[row])):
                self.subcells[row][column].shallowen()
                
    """
    Проверка на принадлежность координаты клетке
    """
    def inBounds(self,gps_coords): #checks if point contains in cell
        #todo: optimize
        lng_lhb = min(self.coordinates[:,1]) # left hand border
        lng_rhb = max(self.coordinates[:,1]) # right hand border
        lat_tpb = min(self.coordinates[:,0]) # top border
        lat_btb = max(self.coordinates[:,0]) # bottom border
        return (lat_tpb <= gps_coords[0] < lat_btb) and (lng_lhb <= gps_coords[1] < lng_rhb)
    
    """
    Добавление элемента в клетку по слабому указателю
    """
    def addRef(self,item,point):
        #print('attempting to add point')
        #print('point coordinates:',point)
        if not (self.inBounds(point)):
            raise NameError("Addoing invalid point!")
        if not (item in self.items):
            #TODO: Optimize
            if self.depth > 0:
                
                def iterate():
                    for row in range(self.resolution):
                        for col in range(self.resolution):
                            #print('scanning cell:',row,col)
                            cell = self.subcells[row][col]
                            #print('cell coordinates:',cell.coordinates)
                            if cell.inBounds(point):
                                cell.addRef(item,point)
                                return True
                    return False
                added = iterate()
                            
                if added == False:
                    raise NameError("Item is out of range!")

                
            self.items.append(item)
            
#             lat_length = self.coordinates[1][0]-self.coordinates[0][0]
#             lng_length = self.coordinates[1][1]-self.coordinates[0][1]
#             crow = math.floor((self.coordinates[0][0]-lat)/lat_length*self.resolution) #lattitude cell
#             ccol = math.floor((self.coordinates[0][0]-lng)/lng_length*self.resolution) #longitude
            
    """
    Рекурсивная функция обслуживает getLayer
    """
    def getLayerInternal(self,depth,coordinates=(0,0)):

        if depth < 0:
            raise NameError("trying to get negative layer depth")
        if depth == 0:
            raise NameError("trying to get current instance through getLayer (depth = 0)")
        ret = []
        
        coordinates=(coordinates[0]*self.resolution,coordinates[1]*self.resolution)
        
        if depth == 1:
            for row in range(self.resolution):
                for col in range(self.resolution):
                    ret.append( (coordinates[0]+row,coordinates[1]+col,weakref.ref(self.subcells[row][col])) )
            return ret
        
        for row in range(self.resolution):
            for col in range(self.resolution):
                #ret.append( (row,col,weakref.ref(self.subcells[row][col])) )
                ret+=self.subcells[row][col].getLayerInternal(depth-1,(coordinates[0]+row,coordinates[1]+col))
        
        return ret
    
    """
    Совмещает все клетки на глубине depth в одну матрицу
    """
    def getLayer(self,depth):
        data = self.getLayerInternal(depth)
        result = np.zeros((self.resolution**depth,self.resolution**depth),dtype=object)
        for (row,col,ref) in data:
            result[row,col] = ref
        return result
            
    def addRefs():
        pass
                
    def __str__(self):
        return "DC"+str(self.resolution)+str(self.depth)