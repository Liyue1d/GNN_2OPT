# GNN_2OPT

Computes approximate solutions in a graph to problems instances I = (s,d,M) where: s is the start node, d the end node and M the list of mandatory nodes to visit at least once.

Requirements:SWIG (need to setup config files for numpy so C++ knows where to look for required files), numpy, networkx, scipy, tensorflow, cuda

Installation instructions:

1) Install Cuda
Export to Path and Environment variables
See guide : https://docs.nvidia.com/cuda/archive/10.0/

2) Install Pip for python 3: sudo apt-get install python3-pip

3) Install tensorflow GPU: pip3 install tensorflow-gpu
If any problems, install older versions of tensorflow-gpu.
Tested successfully with tensorflow-gpu 1.4.0

3) Install cuDNN v7.6.2 (July 22, 2019), for CUDA 10.0(create Nvidia account):
https://developer.nvidia.com/rdp/cudnn-download
(Install Runtime, developer, code samples for Ubuntu version)

4) Install Numpy : pip3 install numpy

5) Install Scipy: sudo apt-get install python3-scip

6) Install Networkx: pip3 install networkx

7) Install SWIG: sudo apt-get install swig

8) Go to hybrid_2OPT_simu/hybrid_2OPT_simu/python/SWIG_TwoOptClient and edit swig_compile.sh:
- If needed, correct the following address to python3.5 package: /usr/include/python3.5/
- If needed, correct the following address to numpy: /usr/lib/python3/dist-packages/numpy/core/include/

9) Run sudo ./swig_compile.sh

10) When calling this program from C++ (use c++11),  include in C++ source code the header "pyFunctions.h". Include in the makefile pyFunctions.cpp and the path to python3.5-config:
example: g++ -std=c++11 gcnScenario.cpp pyFunctions.cpp -o gcnScenario $(/usr/bin/python3.5-config --ldflags)

Three C++ functions can be used (example in gcnScenario.cpp):

- UpdateGraph: Needs to be run after the graph file GRAPH.xml (in XML format) is updated in python/input

- TrainCaller: Trains the GCN on the current graph

- gcnApplicationCaller: Solves a problem (s,d,M): start/destination/mandatory and returns the result



