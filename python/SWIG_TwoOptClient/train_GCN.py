import tensorflow as tf
import numpy as np
import pickle
import sys
import h5py
import os
import sys
sys.path.insert(0, 'src/')
from TwoOptClient import twoOptCompute
import numpy as np
import random
import time


training_hours = float(sys.argv[1])




# Hyperparameters
exec(open("./../model_params/params.py").read())

os.environ["CUDA_VISIBLE_DEVICES"]= str(GPU_in_use)
A = data.get('adj')
shortest_costs = data.get('shortest_costs')


# Definition du graphe de calcul
exec(open("./defineGraph.py").read())
sess = tf.InteractiveSession(config=tf.ConfigProto(allow_soft_placement=True))

#Initialiasation des variables et module de sauvegarde
sess.run(tf.global_variables_initializer())
saver = tf.train.Saver()

#Chargement de fonctions nécéssaires
exec(open("./pib.py").read())

#Separation index x y
separationInd = number_of_features_per_node * number_of_nodes

#Initialisation des compteurs

#Nombre de batch update
i = 0
#nombre de periodes
periods = 0
#Dernier cycle d'amelio
last_test_improvement = 0
#meilleur score sur le test
best_test_score = sys.float_info.max
#index courant sur le dataset
ind = 0

#Entrainement du modèle

#Fenetre d'apprentissage
window = []
start = time.time()

while float(time.time() - start) < training_hours * 3600:
    print(time.time() - start)
    print(training_hours * 3600)

    #Generation de nouvelles donnees
    if i % (number_of_nodes * new_data_insert_frequency) == 0:
        window = window + batchGen()
        while(len(window) > sizeOfWindow):
            window.pop(0)

#Entrainement du GCN


    if (len(window) > batch_size):

        current_batch = np.array(random.sample(window, batch_size))
        xSet = current_batch[:,0:separationInd]
        ySet = current_batch[:,separationInd:]
        sess.run(train_step_single, feed_dict = {x0: xSet, y0: ySet,
        dropout_prob: drop_probability, is_training: True})



    else:

        current_batch = np.array(window)
        xSet = current_batch[:,0:separationInd]
        ySet = current_batch[:,separationInd:]
        sess.run(train_step_single, feed_dict = {x0: xSet, y0: ySet,
        dropout_prob: drop_probability, is_training: True})


    if i % 100 == 0:
        train_batch_avg_loss, train_accuracy, train_summary = sess.run([average_loss0, accuracy, merged], feed_dict={
            x0: xSet, y0: ySet, dropout_prob: 1.0, is_training: False})


        print("\n window size: %d"%len(window))

        if len(window) > sizeOfWindow - 10:
            train_writer.add_summary(train_summary, i)


        save_path = saver.save(sess, "../save/tuned_graph_net.ckpt")
        print("Model saved in path: %s" % save_path)




        print('step %d, training accuracy %g' % (i, train_accuracy))
        print('step %d, training batch avg loss %f' % (i, train_batch_avg_loss))


    #update counters
    i += 1

sess.close()
tf.reset_default_graph()