#include "pyFunctions.h"
#ifdef _pyFunctions_H


void updateGraph(char const *swig_dir){

  chdir (swig_dir);
  FILE* file;
  int argc;
  wchar_t * argv[1];
  argc = 1;
  argv[0] = Py_DecodeLocale("graph_to_pickle.py", NULL);
  Py_SetProgramName(argv[0]);
  //Py_Initialize();
  PySys_SetArgv(argc, argv);
  file = fopen("graph_to_pickle.py","r");
  PyRun_SimpleFile(file, "graph_to_pickle.py");
  //Py_Finalize();
}

void trainCaller(char const *swig_dir, const char* training_hours){
  chdir (swig_dir);
  FILE* file;
  int argc;
  wchar_t * argv[2];
  argc = 2;
  argv[0] = Py_DecodeLocale("train_GCN.py", NULL);
  argv[1] = Py_DecodeLocale(training_hours, NULL);
  Py_SetProgramName(argv[0]);
  //Py_Initialize();
  PySys_SetArgv(argc, argv);
  file = fopen("train_GCN.py","r");
  PyRun_SimpleFile(file, "train_GCN.py");
  //Py_Finalize();
}


vector<string> gcnApplicationCaller(char const *swig_dir, string start, string end, string mandatory){
  vector<string> results(3);
  chdir (swig_dir);
  //recalibrage des noeuds à 0 pour le programme python
  string start_rec = std::to_string(std::stoi(start)-1);
  string end_rec = std::to_string(std::stoi(end)-1);
  string mandatory_rec ("");
  std::string s = mandatory;
  std::string delimiter = ",";
  size_t pos = 0;
  std::string token;
  while ((pos = s.find(delimiter)) != std::string::npos) {
      token = s.substr(0, pos);
      mandatory_rec += std::to_string(std::stoi(token)-1);
      mandatory_rec += ",";
      s.erase(0, pos + delimiter.length());
  }
  mandatory_rec += std::to_string(std::stoi(s)-1);
  const char * start_rec_ch = start_rec.c_str();
  const char * end_rec_ch = end_rec.c_str();
  const char * mandatory_rec_ch = mandatory_rec.c_str();

// Appel au programme python
  FILE* file;
  int argc;
  wchar_t * argv[4];
  argc = 4;
  argv[0] = Py_DecodeLocale("chain_single_example.py", NULL);
  argv[1] = Py_DecodeLocale(start_rec_ch, NULL);
  argv[2] = Py_DecodeLocale(end_rec_ch, NULL);
  argv[3] = Py_DecodeLocale(mandatory_rec_ch, NULL);
  Py_SetProgramName(argv[0]);
  //Py_Initialize();
  PySys_SetArgv(argc, argv);
  file = fopen("chain_single_example.py","r");
  PyRun_SimpleFile(file, "chain_single_example.py");
  //Py_Finalize();

  string sol_path;
  string cost;
  string mand_order;
  ifstream myfile ("results.txt");
  if (myfile.is_open())
  {
    getline (myfile,sol_path);
    getline (myfile,cost);
    getline (myfile,mand_order);
    myfile.close();
    string sol_path_rec ("");
    s = sol_path;
    delimiter = ",";
    pos = 0;
    while ((pos = s.find(delimiter)) != std::string::npos) {
        token = s.substr(0, pos);
        sol_path_rec += std::to_string(std::stoi(token)+1);
        sol_path_rec += ",";
        s.erase(0, pos + delimiter.length());
    }
    sol_path_rec += std::to_string(std::stoi(s)+1);
    string mand_order_rec ("");
    s = mand_order;
    delimiter = ",";
    pos = 0;
    while ((pos = s.find(delimiter)) != std::string::npos) {
        token = s.substr(0, pos);
        mand_order_rec += std::to_string(std::stoi(token)+1);
        mand_order_rec += ",";
        s.erase(0, pos + delimiter.length());
    }
    mand_order_rec += std::to_string(std::stoi(s)+1);

    sol_path = sol_path_rec;
    mand_order = mand_order_rec;
  }
  else cout << "Unable to open file";

  results[0] = sol_path;
  results[1] = cost;
  results[2] = mand_order;
  return results;
}



#endif
