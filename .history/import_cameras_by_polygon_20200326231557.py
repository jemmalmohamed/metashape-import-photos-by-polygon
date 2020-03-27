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

        self.btnQuit = QtWidgets.QPushButton("Cancel")
        self.btnQuit.setFixedSize(85, 23)

        self.btnP1 = QtWidgets.QPushButton("OK")
        self.btnP1.setFixedSize(85, 23)

        layout = QtWidgets.QGridLayout()  # creating layout

        # layout.addWidget(self.chkSave, 4, 2)
        layout.addWidget(self.btnP1, 4, 3)
        layout.addWidget(self.btnQuit, 4, 4)

        self.setLayout(layout)

        def proc_import(): return self.importCameras()

        QtCore.QObject.connect(
            self.btnP1, QtCore.SIGNAL("clicked()"), proc_import)
        QtCore.QObject.connect(self.btnQuit, QtCore.SIGNAL(
            "clicked()"), self, QtCore.SLOT("reject()"))

        self.exec()

    def importCameras(self):

        print("Import Cameras Script started...")

        chunk = Metashape.app.document.chunk
        c = 'G:/these/articles/talambot/data/1- pva/100MEDIA/DJI_0001.JPG'
        chunk.importCameras(path=c)
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
            for c in chunk.cameras:

                cameraLambert = Metashape.CoordinateSystem.transform(
                    c.reference.location,  sourceCamera,  lambert)

                photo = Point(cameraLambert.x, cameraLambert.y)
                # print(photo.wkt)

                i = c.key

                if poly.contains(photo):
                    chunk.cameras[i].selected = True
                else:
                    chunk.cameras[i].selected = False

        print("Script finished!")
        return True


def importCameras():
    global doc
    doc = Metashape.app.document

    app = QtWidgets.QApplication.instance()
    parent = app.activeWindow()

    dlg = ImportCameraDlg(parent)


label = "Custom menu/Import Cameras"
Metashape.app.addMenuItem(label, importCameras)
print("To execute this script press {}".format(label))
