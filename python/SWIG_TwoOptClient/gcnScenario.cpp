// Note : inclure dans le makefile ou le compilateur pyFunctions.cpp et le path de python3.5-conf
// exemple: g++ -std=c++11 gcnScenario.cpp pyFunctions.cpp -o gcnScenario $(/usr/bin/python3.5-config --ldflags)


#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <python3.5/Python.h>
#include "pyFunctions.h"

using namespace std;

int main()
{
  Py_Initialize(); //ouverture flux python

  //Definir chemin de swig
  char const *swig_dir = "/home/safran/Documents/hybrid_2OPT_simu/hybrid_2OPT_simu/python/SWIG_TwoOptClient/";

  //MAJ du graphe. Decommenter pour mettre le graphe à jour
  //updateGraph(swig_dir);

  //MAJ du GCN. Decommenter pour entrainer le GCN sur le graphe mis à jour.
  //const char* training_hours = "24";
  //trainCaller(swig_dir, training_hours);



  //mission
  // Les noeuds commencent à 1
  string start = "2";
  string end = "16";
  string mandatory = "14,1,11,4,15,10,8";

  vector<string> results = gcnApplicationCaller(swig_dir, start, end, mandatory);
  string sol_path = results[0];
  double cost = stod(results[1]);
  string mand_order = results[2];

  cout << "\n PATH:" << sol_path << endl;
  cout << "\n COST:" << cost << endl;
  cout << "\n ORDER:" << mand_order << endl;

  Py_Finalize(); //fermeture flux python

  return 0;
}
