import sys
import subprocess

import Metashape
from PySide2 import QtGui, QtCore, QtWidgets
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely import geometry
import os

from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS

import shapefile
import pygeoif

# Checking compatibility
compatible_major_version = "1.6"
found_major_version = ".".join(Metashape.app.version.split('.')[:2])
if found_major_version != compatible_major_version:
    raise Exception("Incompatible Metashape version: {} != {}".format(
        found_major_version, compatible_major_version))


class ImportCameraDlg(QtWidgets.QDialog):
    imageList = list
    shapeFile = ''
    def __init__(self, parent):

        QtWidgets.QDialog.__init__(self, parent)

        self.setWindowTitle("IMPORT CAMERAS , BY CMG")
        self.resize(300, 150)

        self.btnAdd = QtWidgets.QPushButton("Select Folder")
        self.btnAdd.setFixedSize(85, 23)

        self.btnShp = QtWidgets.QPushButton("Select SHP")
        self.btnShp.setFixedSize(85, 23)

        self.btnQuit = QtWidgets.QPushButton("Cancel")
        self.btnQuit.setFixedSize(85, 23)

        self.btnP1 = QtWidgets.QPushButton("OK")
        self.btnP1.setFixedSize(85, 23)

        layout = QtWidgets.QGridLayout()  # creating layout

        layout.addWidget(self.btnAdd, 3, 3)
        layout.addWidget(self.btnShp, 3, 4)

        layout.addWidget(self.btnP1, 4, 3)
        layout.addWidget(self.btnQuit, 4, 4)

        self.setLayout(layout)

        def proc_import(): return self.importCameras()
        def selectFolder(): return self.selectFolder()
        def selectShpFile(): return self.selectShapeFile()

        QtCore.QObject.connect(
            self.btnAdd, QtCore.SIGNAL("clicked()"), selectFolder)

        QtCore.QObject.connect(
            self.btnShp, QtCore.SIGNAL("clicked()"), selectShpFile)

        QtCore.QObject.connect(
            self.btnP1, QtCore.SIGNAL("clicked()"), proc_import)

        QtCore.QObject.connect(self.btnQuit, QtCore.SIGNAL(
            "clicked()"), self, QtCore.SLOT("reject()"))

        self.exec()

    def selectShapeFile(self):
        shapeFile = QtWidgets.QFileDialog.getOpenFileNames(
            self, 'Open File', 'c\\', 'Image files (*.shp)')
        shp = shapeFile[0][0]

        shapes = shapefile.Reader(shp).shapes()
        shp = shapes[0]

    def selectFolder(self):

        wgs = Metashape.CoordinateSystem("EPSG::4326")
        merc = Metashape.CoordinateSystem("EPSG::3857")
        lambert = Metashape.CoordinateSystem("EPSG::26191")

        chunk = Metashape.app.document.chunk
        # files = QtWidgets.QFileDialog.getOpenFileNames(
        #     self, 'Open File', 'c\\', 'Image files (*.jpg)')

        # self.IMAGELIST = files[0]

        # imageList.append(imagePath)
        directoryPath = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Directory")
        dossier = directoryPath.split('/')[-1]

        for (root, dirs, files) in os.walk(directoryPath):

            for shape in chunk.shapes:

                shape.vertices = [Metashape.CoordinateSystem.transform(
                    v, source, lambert) for v in s.vertices]
                # print(shape.vertices)
                poly = geometry.Polygon([[p.x, p.y] for p in shape.vertices])
                print(poly.wkt)
                for file in files:
                    extension = os.path.splitext(file)[1].lower()
                    if(extension == '.jpg'):
                        path_photo = root + '/' + file
                        exif = get_exif(path_photo)
                        geotags = get_geotagging(exif)
                        coord = get_coordinates(geotags)
                        photo = Point(float(coord['lat']), float(coord['lon']))
                        print(photo.wkt)
                        if poly.contains(photo):
                            print(path_photo)

                        else:
                            print('no')
                #             self.IMAGELIST.append(path_photo)
                # for f in self.imageList:
                #     print(f)

    def checkPhotoInPolygon(coord, polygon):

        wgs = Metashape.CoordinateSystem("EPSG::4326")
        merc = Metashape.CoordinateSystem("EPSG::3857")
        lambert = Metashape.CoordinateSystem("EPSG::26191")

    def importCameras(self):

        print("Import Cameras Script started...")

        # chunk = Metashape.app.document.chunk

        # chunk.addPhotos(self.IMAGELIST)
        # source = chunk.shapes.crs

        wgs = Metashape.CoordinateSystem("EPSG::4326")
        merc = Metashape.CoordinateSystem("EPSG::3857")
        lambert = Metashape.CoordinateSystem("EPSG::26191")

        # for shape in chunk.shapes:

        #     print(chunk.shapes.crs)
        #     # s.vertices = [Metashape.CoordinateSystem.transform(v, source, lambert) for v in s.vertices]
        #     print(shape.vertices)
        #     poly = geometry.Polygon([[p.x, p.y] for p in shape.vertices])
        #     print(poly.wkt)
        #     photo = Point(cameraLambert.x, cameraLambert.y)

        #     # print(photo.wkt)
        # for c in chunk.cameras:

        #     cameraLambert = Metashape.CoordinateSystem.transform(
        #         c.reference.location,  sourceCamera,  lambert)

        #     photo = Point(cameraLambert.x, cameraLambert.y)
        #     # print(photo.wkt)

        #     i = c.key

        #     if poly.contains(photo):
        #         chunk.cameras[i].selected = True
        #     else:
        #         chunk.cameras[i].selected = False

        print("Script finished!")
        return True

# get x y from image


def get_decimal_from_dms(dms, ref):

    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)


def get_coordinates(geotags):
    lat = get_decimal_from_dms(
        geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(
        geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return {'lat': lat, 'lon': lon}


def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging


def get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val

    return labeled


def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

    print('--------------------------------')


def importCameras():
    global doc

    doc = Metashape.app.document

    app = QtWidgets.QApplication.instance()
    parent = app.activeWindow()

    dlg = ImportCameraDlg(parent)


label = "Custom menu/Import Cameras"
Metashape.app.addMenuItem(label, importCameras)
print("To execute this script press {}".format(label))
