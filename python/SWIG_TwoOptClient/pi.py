#Fichier de définition de l'utilisation recursive du GCN pour la
#phase d'utilisation

import socket
import tensorflow as tf
import numpy as np
import sys
import pickle
import h5py
import csv

# Hyperparameters
exec(open("./../model_params/params.py").read())

# Graph definition
exec(open("./defineGraph.py").read())
sess = tf.InteractiveSession(config=tf.ConfigProto(allow_soft_placement=True))
saver = tf.train.Saver()

#Restore variables
try:
    saver.restore(sess, "../save/tuned_graph_net.ckpt")
    print("\n Successfully loaded GCN weights")
except:
    print("\n GCN save files not found. Using random GCN weights")
    sess.run(tf.global_variables_initializer())

#separation index between x and y
separationInd = number_of_features_per_node * number_of_nodes

#Prend en entrée une instance, le nombre de noeud du graphe n,
# et le nombre d'attributs par noeuds m et retourne le vecteur correspondant
def instanceToArray(instance, n, m):
    start = instance[0]
    end = instance[1]
    mand = instance[2]
    ia = np.zeros(n*m)
    ia[start*m] = 1
    ia[end*m+1] = 1
    for manNode in mand:
        ia[manNode*m+2]=1
    return ia

#Prend en entrée une instance et retourne une liste ordonnée par le GCN
#des points oblogatoires
def pi(instance):

    start = instance[0]
    end = instance[1]
    mand = instance[2]

    if len(mand) <= 1:
        return mand

    order =[]

    while len(mand) > 0:
        if len(mand) == 1:
            order.append(mand[0])
            start = mand[0]
            mand = []
            instance[0] = start
            instance[2] = mand
        else:
            array = instanceToArray(instance, number_of_nodes, number_of_features_per_node)
            [prob] = sess.run(prob0, feed_dict = {x0: [array], dropout_prob: 1, is_training: False})
            #print("\n mand bef")
            #print(mand)
            #print(prob)
            mandatory_probs = prob[mand]
            nextNode = mand[np.argmax(mandatory_probs)]
            order.append(nextNode)
            start = nextNode
            mand.remove(nextNode)
            #print("\n mand af")
            #print(mand)
            instance[0] = start
            instance[2] = mand

    return order;
