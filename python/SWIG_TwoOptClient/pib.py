#Fichier de définition de l'utilisation recursive du GCN pour la
#phase d'apprentissage, et autre fonctions utiles


#Separation index between x and y
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



#Function to compute loss for test set
def test_loss(sess, batch_size, x_test, y_test):
    test_size = x_test.shape[0]
    test_loss = 0
    test_right = 0
    count = 0
    while count < test_size:
        if count + batch_size < test_size + 1:
            xSet = x_test[count:(count+batch_size)]
            ySet = y_test[count:(count+batch_size)]
            batch_loss, batch_right = sess.run([total_loss0, total_right], feed_dict={
                x0: xSet, y0: ySet, dropout_prob: 1.0, is_training: False})
            test_loss = test_loss + batch_loss
            test_right = test_right + batch_right
        else:
            xSet = x_test[count:]
            ySet = y_test[count:]
            batch_loss, batch_right = sess.run([total_loss0, total_right], feed_dict={
                x0: xSet, y0: ySet, dropout_prob: 1.0, is_training: False})
            test_loss = test_loss + batch_loss
            test_right = test_right + batch_right
        count = count + batch_size


    avg_loss = test_loss / test_size
    accuracy = test_right / test_size

    summary = tf.Summary(value=[tf.Summary.Value(tag="loss", simple_value=avg_loss), tf.Summary.Value(tag="accuracy", simple_value=accuracy)])
    return [avg_loss, accuracy, summary]

def batchGen():
    number_of_features_per_node = 3
    x_size = number_of_nodes * number_of_features_per_node
    y_size = number_of_nodes
    c = 0
    vect = []
    i = random.randint(0,number_of_nodes-1)
    j = random.randint(0,number_of_nodes-1)
    possible_mandatories = [x for x in range(number_of_nodes) if x != i and x != j]
    length = len(possible_mandatories)
    num = random.randint(1,length)
    current_choices = list(possible_mandatories)
    mandatories = []
    for m in range(num):
        mn = random.choice(current_choices)
        mandatories.append(mn)
        current_choices.remove(mn)
    instance = [i, j, mandatories]
    nv = instance.copy()
    nv[2] = instance[2].copy()

    print("\n Instance mand length  %s"%len(instance[2]))
    gcn_order = pi(nv)
    order_inst = instance.copy()
    order_inst[2] = gcn_order.copy()
    random.shuffle(instance[2])

    results = twoOptCompute(A,instance)
    order_results = twoOptCompute(A,order_inst)


    if results[1] < order_results[1]:
    	r = results
    else:
        r = order_results
    sol_order = r[2]
    start = instance[0]
    end = instance[1]
    mand = instance[2].copy()
    for s in sol_order:
        new = [start, end, mand]
        array = instanceToArray(new, number_of_nodes, number_of_features_per_node)
        label = np.zeros(number_of_nodes)
        label[s] = 1
        vect.append(np.concatenate((array, label)))
        start = s
        mand.remove(s)

    return vect    
