import sys
import subprocess

import Metashape
from PySide2 import QtGui, QtCore, QtWidgets
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely import geometry
import os
import concurrent.futures

from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS

import shapefile


# Checking compatibility
compatible_major_version = "1.6"
found_major_version = ".".join(Metashape.app.version.split('.')[:2])
if found_major_version != compatible_major_version:
    raise Exception("Incompatible Metashape version: {} != {}".format(
        found_major_version, compatible_major_version))


class ImportCameraDlg(QtWidgets.QDialog):
    imageList = ['']
    shapeFile = Polygon
    pathPhotos = ['']
    def __init__(self, parent):

        QtWidgets.QDialog.__init__(self, parent)

        self.setWindowTitle("IMPORT CAMERAS , BY CMG")
        self.resize(300, 150)

        self.btnAdd = QtWidgets.QPushButton("Select Folder")
        self.btnAdd.setFixedSize(200, 23)

        self.btnShp = QtWidgets.QPushButton("Select SHP")
        self.btnShp.setFixedSize(200, 23)

        self.btnQuit = QtWidgets.QPushButton("Cancel")
        self.btnQuit.setFixedSize(200, 23)

        self.btnP1 = QtWidgets.QPushButton("OK")
        self.btnP1.setFixedSize(200, 23)

        layout = QtWidgets.QGridLayout()  # creating layout

        layout.addWidget(self.btnShp, 2, 1)
        layout.addWidget(self.btnAdd, 3, 1)

        layout.addWidget(self.btnP1, 4, 1)
        # layout.addWidget(self.btnQuit, 4, 2)

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

        self.btnAdd.setEnabled(False)
        self.exec()

    def selectShapeFile(self):
        self.shapeFile = Polygon
        shapeFile = QtWidgets.QFileDialog.getOpenFileNames(
            self, 'Open File', 'c\\', 'Image files (*.shp)')
        shp = shapeFile[0][0]
        shapes = shapefile.Reader(shp).shapes()
        shp = shapes[0]
        poly = Polygon(shp.points)
        self.btnAdd.setEnabled(True)
        self.shapeFile = poly
        print(self.shapeFile.wkt)

    def selectFolder(self):
        self.imageList = []
        self.pathPhotos = []

        chunk = Metashape.app.document.chunk

        directoryPath = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Directory")
        dossier = directoryPath.split('/')[-1]

        for (root, dirs, files) in os.walk(directoryPath):

            for file in files:
                extension = os.path.splitext(file)[1].lower()
                if(extension == '.jpg'):
                    path_photo = root + '/' + file
                    self.pathPhotos.append(path_photo)

        print(len(self.pathPhotos))

    def checkPhotos(self, path_photo):
        wgs = Metashape.CoordinateSystem("EPSG::4326")

        lambert = Metashape.CoordinateSystem("EPSG::26191")

        exif = get_exif(path_photo)
        geotags = get_geotagging(exif)
        coord = get_coordinates(geotags)

        cameraLambert = Metashape.CoordinateSystem.transform(
            [float(coord['lon']), float(coord['lat'])],  wgs,  lambert)

        photo = Point(cameraLambert.x, cameraLambert.y)

        if self.shapeFile.contains(photo):
            self.imageList.append(path_photo)

    def importCameras(self):

        print("Import Cameras Script started...")

        with con

        threads = []
        for path_photo in self.pathPhotos:
            t = threading.Thread(target=self.checkPhotos, args=[path_photo])
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()

            # self.checkPhotos(path_photo)

        chunk = Metashape.app.document.chunk

        chunk.addPhotos(self.imageList)

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
    exif = image._getexif()
    image.close()
    return exif

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
