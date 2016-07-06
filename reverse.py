from qgis.core import *
from qgis.gui import *

class ClickTool(QgsMapTool):
    def __init__(self,iface, callback):
        QgsMapTool.__init__(self,iface.mapCanvas())
        self.iface      = iface
        self.callback   = callback
        self.canvas     = iface.mapCanvas()
        return None


    def canvasReleaseEvent(self,e):
        '''point = self.canvas.getCoordinateTransform().toMapPoint(e.pos().x(),e.pos().y())
        '''
        point = (-122.42238,37.75134)
        self.callback(point)
        
        return None


def pointToWGS84(point, crs):
    """
    crs is the renderer crs
    """
    t=QgsCoordinateReferenceSystem()
    t.createFromSrid(4326)
    f=crs #QgsCoordinateReferenceSystem()
    #f.createFromProj4(proj4string)
    transformer = QgsCoordinateTransform(f,t)
    pt = transformer.transform(point)
    print "Printing something"

    return pt

def pointFromWGS84(point, crs):
    f=QgsCoordinateReferenceSystem()
    f.createFromSrid(4326)
    t=crs # QgsCoordinateReferenceSystem()
    #t.createFromProj4(proj4string)
    transformer = QgsCoordinateTransform(f,t)
    pt = transformer.transform(point)
    print "Printing something"
    return pt


#print transformer.transform(point)
