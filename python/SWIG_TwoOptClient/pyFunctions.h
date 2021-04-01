#ifndef _pyFunctions_H
#define _pyFunctions_H
#include <iostream>
#include <stdio.h>
#include <python3.5/Python.h>
#include <string>
#include <stdlib.h>
#include <unistd.h>
#include <fstream>
#include <vector>
using namespace std;

void updateGraph(char const *swig_dir);
void trainCaller(char const *swig_dir, const char* training_hours);
vector<string> gcnApplicationCaller(char const *swig_dir, string start, string end, string mandatory);


#endif
