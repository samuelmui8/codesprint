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

## Note
Interactive view is currently only available on local environment.
You can clone this repository and run the following command to run the app locally.
```
streamlit run app.py
```
## Reference

* [Optimizing three-dimensional bin packing through simulation](https://github.com/jerry800416/3dbinpacking/blob/master/reference/OPTIMIZING%20THREE-DIMENSIONAL%20BIN%20PACKING%20THROUGH%20SIMULATION.pdf)
* https://github.com/enzoruiz/3dbinpacking
* https://github.com/nmingotti/3dbinpacking
* https://github.com/jerry800416/3D-bin-packing

