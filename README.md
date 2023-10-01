PSA Codesprint EZPack
====
https://github.com/teoks0199/codesprint

## Introduction

EZPack is a web application designed to optimize cargo container packing. Using a 3D Bin Packing Algorithm:
It generates 3D models illustrating the most efficient way to load shipments into containers.
Includes an interactive view of the 3D model.
Lists items that are fitted/not fitted, and what containers they are in.
EZPack streamlines cargo loading, reduces costs, and maximizes container space utilization.

## How to use
Go to: https://codesprint-ezpack.streamlit.app/

Upload csv file indicating container and item information.

You can use the test csv files in the 'testvals' folder.

csv file format:
```
<number of containers>,,,
<container length>,<container width>,<container height>,<container weight limit>
<number of items>,,,
<item length>,<item width>,<item height>,<item weight>
```
Example: 2 containers, 16 items
```
2,,,
6,10,6,50
5,10,5,50
16,,,
5,4,1,1
1,2,4,1
1,2,3,1
1,2,2,1
1,2,3,1
1,2,4,1
1,2,2,1
1,2,4,1
1,2,3,1
1,2,2,1
5,4,1,1
1,1,4,1
1,2,1,1
1,2,1,1
1,1,4,1
5,4,2,51
```

## Note
Interactive view is currently only available on local environment.
You can clone this repository and run the following command to run the app locally.
```
streamlit run app.py
```

## Video Demo:
https://youtu.be/wADoxMlGi3s
## Reference

* [Optimizing three-dimensional bin packing through simulation](https://github.com/jerry800416/3dbinpacking/blob/master/reference/OPTIMIZING%20THREE-DIMENSIONAL%20BIN%20PACKING%20THROUGH%20SIMULATION.pdf)
* https://github.com/enzoruiz/3dbinpacking
* https://github.com/nmingotti/3dbinpacking
* https://github.com/jerry800416/3D-bin-packing

