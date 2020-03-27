import Metashape
from PySide2 import QtGui, QtCore, QtWidgets
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely import geometry


# Checking compatibility
compatible_major_version = "1.6"
found_major_version = ".".join(Metashape.app.version.split('.')[:2])
if found_major_version != compatible_major_version:
    raise Exception("Incompatible Metashape version: {} != {}".format(
        found_major_version, compatible_major_version))


class ImportCameraDlg(QtWidgets.QDialog):

    def __init__(self, parent):

        QtWidgets.QDialog.__init__(self, parent)

        self.setWindowTitle("IMPORT CAMERAS , BY CMG")
        self.resize(300, 150)

        self.btnAdd = QtWidgets.QPushButton("Select Folder")
        self.btnAdd.setFixedSize(85, 23)
        # self.btnAdd.clicked.connect(self)

        self.btnQuit = QtWidgets.QPushButton("Cancel")
        self.btnQuit.setFixedSize(85, 23)

        self.btnP1 = QtWidgets.QPushButton("OK")
        self.btnP1.setFixedSize(85, 23)

        layout = QtWidgets.QGridLayout()  # creating layout

        layout.addWidget(self.btnAdd, 3, 3)

        layout.addWidget(self.btnP1, 4, 3)
        layout.addWidget(self.btnQuit, 4, 4)

        self.setLayout(layout)

        def proc_import(): return self.importCameras()
        def selectFolder(): return self.selectFolder()

        QtCore.QObject.connect(
            self.btnAdd, QtCore.SIGNAL("clicked()"), selectFolder)

        QtCore.QObject.connect(
            self.btnP1, QtCore.SIGNAL("clicked()"), proc_import())

        QtCore.QObject.connect(self.btnQuit, QtCore.SIGNAL(
            "clicked()"), self, QtCore.SLOT("reject()"))

        self.exec()

    def selectFolder(self):

        imageList = []
        fname = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open File', 'c\\', 'Image files (*.jpg)')
        imagePath = fname[0]
        imageList.append(imagePath)
        print(imageList)

    def importCameras(self, imagePath):

        print("Import Cameras Script started...")

        chunk = Metashape.app.document.chunk
        c = 'G:/these/articles/talambot/data/1- pva/100MEDIA/DJI_0001.JPG'
        chunk.addPhotos([c])
        source = chunk.shapes.crs

        wgs = Metashape.CoordinateSystem("EPSG::4326")
        merc = Metashape.CoordinateSystem("EPSG::3857")
        lambert = Metashape.CoordinateSystem("EPSG::26191")

        for shape in chunk.shapes:

            print(chunk.shapes.crs)
            # s.vertices = [Metashape.CoordinateSystem.transform(v, source, lambert) for v in s.vertices]
            print(shape.vertices)
            poly = geometry.Polygon([[p.x, p.y] for p in shape.vertices])
            print(poly.wkt)
            photo = Point(cameraLambert.x, cameraLambert.y)

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
