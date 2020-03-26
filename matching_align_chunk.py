# This is python script for Metashape Pro. Scripts repository: https://github.com/agisoft-llc/metashape-scripts

import Metashape
from PySide2 import QtGui, QtCore, QtWidgets

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

        self.setWindowTitle("MATCHING + ALIGN PHOTOS , BY CMG")
        self.resize(300, 150)

        self.label_accuracy = QtWidgets.QLabel('Accuracy : ')
        self.matchBox = QtWidgets.QComboBox()
        self.matchBox.resize(60, 23)

        for element in MATCHING_QUALITY.keys():
            self.matchBox.addItem(element)

        self.generic_label = QtWidgets.QLabel('Generic Preselection')
        self.genericPreselection = QtWidgets.QCheckBox()
        self.genericPreselection.setChecked(True)

        self.reference_label = QtWidgets.QLabel('Reference Preselection')
        self.referencePreselection = QtWidgets.QCheckBox()
        self.referencePreselection.setChecked(True)

        self.source_label = QtWidgets.QLabel(': Source')

        self.chkSave = QtWidgets.QCheckBox("Autosave")
        self.chkSave.setToolTip("Autosaves the project after Matching Photos")

        self.btnQuit = QtWidgets.QPushButton("Cancel")
        self.btnQuit.setFixedSize(85, 23)

        self.btnP1 = QtWidgets.QPushButton("OK")
        self.btnP1.setFixedSize(85, 23)

        layout = QtWidgets.QGridLayout()  # creating layout

        layout.addWidget(self.label_accuracy, 1, 1,
                         QtCore.Qt.AlignTop)
        layout.addWidget(self.matchBox, 1, 3, QtCore.Qt.AlignTop)

        layout.addWidget(self.generic_label, 2, 1, QtCore.Qt.AlignTop)
        layout.addWidget(self.genericPreselection,
                         2, 2, QtCore.Qt.AlignTop)
        layout.addWidget(self.reference_label, 3, 1, QtCore.Qt.AlignTop)
        layout.addWidget(self.referencePreselection,
                         3, 2, QtCore.Qt.AlignTop)
        layout.addWidget(self.source_label, 3, 3, QtCore.Qt.AlignTop)

        # layout.addWidget(self.matchBox, 1, 3, QtCore.Qt.AlignTop)
        # layout.addWidget(self.generic_label, 1, 6, QtCore.Qt.AlignTop)
        # layout.addWidget(self.denseBox, 1, 2, QtCore.Qt.AlignTop)

        # layout.addWidget(self.chkSave, 4, 2)
        layout.addWidget(self.btnP1, 4, 3)
        layout.addWidget(self.btnQuit, 4, 4)

        # layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(layout)

        def proc_match(): return self.matchingChunk()

        QtCore.QObject.connect(
            self.btnP1, QtCore.SIGNAL("clicked()"), proc_match)
        QtCore.QObject.connect(self.btnQuit, QtCore.SIGNAL(
            "clicked()"), self, QtCore.SLOT("reject()"))

        self.exec()

    def matchingChunk(self):

        print("Script started...")

        generic_preselect = self.genericPreselection.isChecked()
        reference_preselect = self.referencePreselection.isChecked()

        autosave = self.chkSave.isChecked()

        quality = MATCHING_QUALITY[self.matchBox.currentText()]

        print(generic_preselect)
        print(reference_preselect)
        print(quality)

        app = Metashape.app
        doc = app.document

        chunk = doc.chunk

        chunk.resetRegion()
        self.close()
        if(app.cpu_enable == True):
            app.cpu_enable = False

        for index, item in enumerate(chunk.cameras):

            chunk.cameras[index].transform = None
            # chunk.cameras[index].selected = True

        chunk.matchPhotos(downscale=quality, generic_preselection=generic_preselect,
                          reference_preselection=reference_preselect)

        doc.save()

        for index, item in enumerate(chunk.cameras):
            chunk.cameras[index].selected = True
        #   for c in chunk.cameras:
        #     i = c.key
        #     chunk.cameras[i].selected = True

        chunk.alignCameras(chunk.cameras, min_image=2, adaptive_fitting=False,
                           reset_alignment=False, subdivide_task=True)
        chunk.resetRegion()
        doc.save()

        print("Script finished!")
        return True


def match_and_align():
    global doc
    doc = Metashape.app.document

    app = QtWidgets.QApplication.instance()
    parent = app.activeWindow()

    dlg = SplitDlg(parent)


label = "Custom menu/Matching and Align Photos"
Metashape.app.addMenuItem(label, match_and_align)
print("To execute this script press {}".format(label))
