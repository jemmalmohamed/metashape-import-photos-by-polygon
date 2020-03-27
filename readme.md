**Version 0.0.1**

# Python script for Metashape pro

This script are supported to be used in Metashape Pro v1.6.x
# Functionality

Automatically load photos by choosen polygon 



# Technologies
- python 3.5
# Installation & Requirements 



Install modules shapely , pillow and pyshp by CMD as administrator:


```bash
cd "C:\Program Files\Agisoft\Metashape Pro\python"
```

```bash
python -m pip install pillow
```

```bash
python -m pip install pyshp
```

Install compatible shapely verion to your system https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely

For version Metashape 1.6.x & windows x64 use version Shapely-1.6.4.post2-cp35-cp35m-win_amd64.whl

```bash
python -m pip install "path to\Shapely-1.6.4.post2-cp35-cp35m-win_amd64.whl"
```

# How to use

- Select a polygon format shapefile in EPSG::26191 "Maroc Lambert zone I "
- Select the images folder (the script check the subfolders)

