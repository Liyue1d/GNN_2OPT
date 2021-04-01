#Numero du CPU/GPU à utiliser
GPU_in_use = 0
#Type de machine
device = 'gpu'

# Hyperparameters - ne pas modifier
batch_norm_decay = 0.9
batch_size = 32
drop_probability = 0.9

#Si Test set disponible, arret sans ameliorations
early_stop = 50000

#Vitesse de gradient
learning_rate = 1e-4

#Taille fenetre apprentissage
sizeOfWindow = 50000

#Nombre d'iterations d'apprentissage
number_of_iterations = 10000000000
#Nombre de mise à jour par gradient avant génération nouvelles données
new_data_insert_frequency = 10

# Chargement graph data
with open('../model_utils/data.pickle', 'rb') as f:
    data = pickle.load(f)

# Stockage graph data en variables
adj_matrix = tf.constant(data.get('adj'), dtype = tf.float32)
sym_norm = tf.constant(data.get('prod_matrix'), dtype = tf.float32)
number_of_nodes = data.get('number_of_nodes')
number_of_features_per_node = 3


x_size = number_of_nodes * number_of_features_per_node
y_size = number_of_nodes

# GCN architecture - commence par 3 obligatoirement
#Diminuer le nombre de 10 pour une meilleure stabilité
#(si la perte de diminue pas)
#Achitecture conseillee: graph_layers = [3,10,10,10]
graph_layers = [3,10,10,10]
