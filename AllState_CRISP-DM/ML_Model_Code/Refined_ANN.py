# Get packages
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import StratifiedKFold

def set_up():
    '''Sets up the data for the model'''
    
    # Load in data
    data = pd.read_csv("AllState_clean_data.csv")
    
    # Grab only final purchase
    data = data[data['record_type'] == 1]
    
    # Get important columns
    data = data.iloc[:,[3,5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25]]
    
    # Make car_value_number an integer
    data['car_value_number'] = data['car_value_number'].astype('int')
    
    # Create dummy variables and remove location
    data = pd.get_dummies(data, columns = ['homeowner','married_couple','state'])
    loc = data['location']
    data.drop('location', axis = 1, inplace = True)
    
    return data, loc
    
def run_model(x,y,v):
    '''Runs the artificial neural network model'''
    
    # Set temp values
    acc_temp = []
    loss_temp = []
    f1_temp = []
    
    # Cross validation using stratified k-fold
    skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=30)
    for train_index, test_index in skf.split(x, y):
        X_train, X_test = x.iloc[train_index], x.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        
        # Standardize the data
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
        
        # Configure the model
        model = keras.Sequential()
        model.add(tf.keras.layers.Dense(64, activation = 'relu',
                                        input_shape = (X_train.shape[1],))) # Input layer
        model.add(tf.keras.layers.Dense(128, activation = 'relu')) # Hidden layer
        model.add(tf.keras.layers.Dense(v, activation = 'softmax')) # Output layer
        
        # Compile the model
        model.compile(optimizer = 'adam', loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])
        
        # Model summary
        model.summary()
        
        # Actual Learning
        model.fit(X_train, y_train, epochs = 3)
        
        # Using test data to gauge accuracy, loss and f1 score
        testLoss, testAccuracy = model.evaluate(X_test, y_test)
        acc_temp.append(testAccuracy)
        loss_temp.append(testLoss)
        pred = model.predict(X_test)
        pred_labeled = []
        for i in range(len(pred)):
            pred_labeled.append(np.argmax(pred[i]))
        print(confusion_matrix(y_test, pred_labeled))
        f1_temp.append(f1_score(y_test, pred_labeled, average = 'weighted'))
        
    return acc_temp, loss_temp, f1_temp

def print_metrics(accuracy, loss, f1):
    '''Prints the three metrics'''
    
    print(f"Accuracy: {accuracy}")
    print(f"Loss: {loss}")
    print(f"f1: {f1}")

def main():
    
    data, loc = set_up()
    
    # Set up insurance policies to select and empty lists
    policies = ['A','B','C','D','E','F','G']
    accuracy = []
    loss = []
    f1 = []
    
    # Setting up x with and without location
    x_1 = data.drop(policies, axis = 1)
    x_2 = x_1
    x_2['location'] = loc
    x_2 = pd.get_dummies(x_1, columns = ['location'])
    
    # Loop over insurance policies
    for i in policies:
    
        # Depending on insurance policy, setting x, y, and v
        if i == 'A':
            x = x_1
            y = data['A']
            v = 3
        if i == 'B':
            x = x_2
            y = data['B']
            v = 2
        if i == 'C':
            x = x_1
            y = data['C']
            y = y - 1
            v = 4
        if i == 'D':
            x = x_2
            y = data['D']
            y = y - 1
            v = 3
        if i == 'E':
            x = x_1
            y = data['E']
            v = 2
        if i == 'F':
            x = x_2
            y = data['F']
            v = 4
        if i == 'G':
            x = x_2
            y = data['G']
            y = y - 1
            v = 4
                
        acc_temp, loss_temp, f1_temp = run_model(x,y,v)
        
        # Add new results to lists
        accuracy.append(sum(acc_temp)/len(acc_temp))
        loss.append(sum(loss_temp)/len(loss_temp))
        f1.append(sum(f1_temp)/len(f1_temp))
        
    print_metrics(accuracy, loss, f1)
    
        
if __name__ == "__main__":
    main()