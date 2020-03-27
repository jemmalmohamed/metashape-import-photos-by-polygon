# Python script for Metashape pro

This script are supported to be used in Metashape Pro v1.6.x
# Functionality

Automatically load photos by choosen polygon 

**Version 0.0.1**

# Technologies
- python 3.5
# Installation & Requirements 

in python folder in metashape install folder 

install modules by CMD as administrator:

```bash
cd "C:\Program Files\Agisoft\Metashape Pro\python"
```

```bash
python -m pip install pillow
```

```bash
python -m pip install pyshp
```

install compatible shapely verion to your system whl https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely
For version Metashape 1.6.x & windows x64 use version Shapely-1.6.4.post2-cp35-cp35m-win_amd64.whl

```bash
python -m pip install "path to\Shapely-1.6.4.post2-cp35-cp35m-win_amd64.whl"
```

#utilisation

 - Créer un polygone format un SHP en lambert zone 1 préférable avec un buffer de quelques mètres.
 - Excuser le script.
 - Sélectionner le polygone SHP 
 - Sélectionner le dossier des photos par exemple le dossier "DAR" , le script va chercher aussi les sous dossier.
 # pour 61000 photos va prendre 10 a 12 min de recherche .

 o rad 3liya wach khdam wela la 
  