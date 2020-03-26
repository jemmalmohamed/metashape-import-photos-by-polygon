# This is python script for Metashape Pro. Scripts repository: https://github.com/agisoft-llc/metashape-scripts

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

FILTERING = {"3": Metashape.NoFiltering,
             "0": Metashape.MildFiltering,
             "1": Metashape.ModerateFiltering,
             "2": Metashape.AggressiveFiltering}

MESH = {"Arbitrary": Metashape.SurfaceType.Arbitrary,
        "Height Field": Metashape.SurfaceType.HeightField}

DENSE = {"Ultra":  1,
         "High":   2,
         "Medium": 4,
         "Low":    8,
         "Lowest": 16}


MATCHING_QUALITY = {"Highest": 0,
                    "High": 1,
                    "Medium": 2,
                    "Low": 4,
                    "Lowest": 8
                    }

REFERENCE_PRESELECTION = {"Source": 0}


class SplitDlg(QtWidgets.QDialog):

    def __init__(self, parent):

        QtWidgets.QDialog.__init__(self, parent)

        self.setWindowTitle("ALIGN PHOTOS , BY CMG")
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

        def proc_split(): return self.alignChunk()

        QtCore.QObject.connect(
            self.btnP1, QtCore.SIGNAL("clicked()"), proc_split)
        QtCore.QObject.connect(self.btnQuit, QtCore.SIGNAL(
            "clicked()"), self, QtCore.SLOT("reject()"))

        self.exec()

    def alignChunk(self):

        print("Align Script started...")

        chunk = Metashape.app.document.chunk

        source = chunk.shapes.crs
        print('source shps')
        print(source)
        sourceCamera = chunk.crs
        print('source cemara')
        print(sourceCamera)
        wgs = Metashape.CoordinateSystem("EPSG::4326")
        merc = Metashape.CoordinateSystem("EPSG::3857")
        lambert = Metashape.CoordinateSystem("EPSG::26191")
        print('source lambert')
        print(lambert)
        for c in chunk.cameras:
            i = c.key
            chunk.cameras[i].selected = False
        print(len(chunk.shapes))

        for shape in chunk.shapes:
            s = shape
            print('flag')
            print(chunk.shapes.crs)
            print('avant')
            print(shape.vertices)
            if ALIGN == True:
                s.vertices = [Metashape.CoordinateSystem.transform(
                    v, source, lambert) for v in s.vertices]

            print('apres')
            print(s.vertices)
            poly = geometry.Polygon([[p.x, p.y] for p in s.vertices])
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

            selected = [
                camera for camera in chunk.cameras if camera.selected]

            # chunk.alignCameras(selected, min_image=2, adaptive_fitting=False,
            #                    reset_alignment=False, subdivide_task=True)

            # shape.vertices = [Metashape.CoordinateSystem.transform(
            #     v, lambert, source) for v in shape.vertices]
            ALIGN = False
        print("Script finished!")
        return True


def align_in_chunks():
    global doc
    doc = Metashape.app.document

    app = QtWidgets.QApplication.instance()
    parent = app.activeWindow()

    dlg = SplitDlg(parent)


label = "Custom menu/Align Photos"
Metashape.app.addMenuItem(label, align_in_chunks)
print("To execute this script press {}".format(label))
