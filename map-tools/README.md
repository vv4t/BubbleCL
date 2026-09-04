# Map Tools

Script used to generate a `Map_XXXX.txt` file for dynamic map loading.

Copy an Aottg2 map script into the folder such as `akina.txt`.

Then in the python script, change the map name to the file and run `python compress.py`.

It will generate an `output.txt` which you can rename and put in PersistentData.

Map loading on the CL side is in `class MapLoaderLogic`.
