#include "TwoOpt.h"
#ifdef _TwoOpt_H

TwoOpt::TwoOpt (){}
TwoOpt::~TwoOpt (){}

//This function takes as input
//a 2d-flattened cost matrix: cost_matrix,
//the initial number of rows of the matrix: size_0,
//the initial number of columns of the matrix: size_1,
//the row number of the desired cost: row_number,
//the column number of the desired cost: column_number,
//And returns the cost stored in the matrix at row_number and col_number: cost

double TwoOpt::getCost (const double* cost_matrix, int size_0, int size_1, int row_number, int col_number){
  double cost = cost_matrix[row_number * size_1 + col_number];
  return cost;
}


//This function takes as input
//an order for the mandatory nodes: currentOrder,
//the number of mandatory nodes: length_order,
//a 2d-flattened cost matrix: cost_matrix,
//the initial number of rows of the matrix: size_0,
//the initial number of columns of the matrix: size_1,
//the departure node in the instance: departure_node,
//the arrival node in the instance: arrival_node,
//And returns the path cost of the order currentOrder: cost

double TwoOpt::pathCost (int* currentOrder, int length_order, const double* cost_matrix, int size_0, int size_1, int departure_node, int arrival_node){

  //cost of the path to be returned, set to 0
  double cost = 0;
  // cost of the link from the departure node to the 1st node in the order currentOrder
  cost = cost + getCost (cost_matrix, size_0, size_1, departure_node, currentOrder[0]);
  // cost of the link from the last node in the order currentOrder to the arrival node
  cost = cost + getCost (cost_matrix, size_0, size_1, currentOrder[length_order-1], arrival_node);
  //cost of all the paths linking the nodes in currentOrder
  for (int i = 0; i < length_order-1; i++){
    cost = cost + getCost (cost_matrix, size_0, size_1, currentOrder[i], currentOrder[i+1]);
  }

  return cost;
}

//This function takes as input
//an order for the mandatory nodes: currentOrder,
//the number of mandatory nodes: length_order,
//the index of the node in the order from which the swapping starts: i,
//the index of the node in the order from which the swapping ends: j,
//And returns the new path that has been swapped: newPath

int* TwoOpt::pathSwap(int* currentOrder, int length_order, int i, int j){

  //create new space for the new path
  int* newPath = (int*) malloc(length_order * sizeof(int));
  //set new path to current path
  for (int k = 0; k < length_order; k++){
    newPath[k] = currentOrder[k];
  }
  //swap the new path from i to j
  while(i<j){
    int tempI = newPath[i];
    int tempJ = newPath[j];
    newPath[i] = tempJ;
    newPath[j] = tempI;
    i++;
    j--;
  }

  return newPath;
}

//This function takes as input
//an order for the mandatory nodes: order,
//the number of mandatory nodes: length_order,
//a 2d-flattened cost matrix: cost_matrix,
//the initial number of rows of the matrix: size_0,
//the initial number of columns of the matrix: size_1,
//the departure node in the instance: departure_node,
//the arrival node in the instance: arrival_node,
//a table where to store computation information: inf,
//the size of the information table: size_of_inf,
//!!!! order and inf are modified in memory, and exploited !!!!
//!!!! in python after the call to this function, no explicit return !!!!

void TwoOpt::optimize (double* order, int length_order, const double* cost_matrix, int size_0, int size_1, int departure_node, int arrival_node, double* inf, int size_of_inf, double* permutation_group, int size_of_group, double* score_value, int size_of_score) {
  //number of swap attempts
  int attempts = 0;
  //number of swaps
  int swap_cnt = 0;
  int swap_ind = 0;
  //new container for the initial order, cast to int type.
  //this container will be optimized and copied back to order
  int* order_int = (int*) malloc(length_order * sizeof(int));
  for (int i = 0; i < length_order; i++){
    order_int[i] = (int) order[i];
  }

  //improvement boolean set to true. Will break the following loop
  //if no improvement after one iteration of twoOpt
  bool improvement = true;
  //best order found so far
  double best_distance;


  //start of two opt iterations
  while(improvement){

    //start point after a swap
    start_again:
    //cost of current order
    best_distance = pathCost (order_int, length_order, cost_matrix, size_0, size_1, departure_node, arrival_node);
    if (swap_ind < size_of_score){
      score_value[swap_ind] = best_distance;
      swap_ind = swap_ind + 1;
    }
    //search of a swap that improves current order
    for (int i = 0; i < length_order - 1; i++){
      for (int j = i + 1; j < length_order; j++){
        //computation of new path from the swap of i,j
        int* newPath = pathSwap(order_int, length_order, i, j);
        attempts ++;
        //computation of cost of the new path
        double new_distance = pathCost (newPath, length_order, cost_matrix, size_0, size_1, departure_node, arrival_node);

        if (new_distance<best_distance){
          //new path better, so keep it and delete old path from memory
          if (j-i < 10){
              permutation_group[j-i-1] = permutation_group[j-i-1] + 1;
          }
          else{
              permutation_group[9] = permutation_group[9] + 1;
          }
          swap_cnt++;
          free(order_int);
          order_int = newPath;
          goto start_again;
        }
        else{
          //old path better, so keep it and delete new path from memory
          free(newPath);
        }
      }
    }
    //no swap that improved current order, so break
    improvement = false;
  }


  //copy new order to shared memory variable
  for (int i = 0; i < length_order; i++){
    order[i] = (double) order_int[i];
  }


  if ((swap_ind < size_of_score) && ((swap_ind-1) >= 0)){
    double last_score = score_value[swap_ind-1];
    while(swap_ind < size_of_score){
      score_value[swap_ind] = last_score;
      swap_ind = swap_ind + 1;
    }
  }


//shared memory variable
  inf[0] = best_distance;
  inf[1] = swap_cnt;
  inf[2] = attempts;
  return;
}

#endif
