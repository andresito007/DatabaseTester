import sys
import numpy as np
import matplotlib.pyplot as plt

from tensorflow import keras

sys.path.append('shared/')
import variables as myVars

def Main():
    Xtest = np.loadtxt(r'dataset/xtest.csv')
    Ytest = np.loadtxt(r'dataset/ytest.csv')
    Xraw = np.loadtxt(r'dataset/xraw.csv')
    Traw = np.loadtxt(r'dataset/traw.csv')

    Xtest = Xtest.reshape(Xtest.shape[0], Xtest.shape[1], 1)
    Ytest = Ytest.reshape(Ytest.shape[0], Ytest.shape[1], 1)

    Xraw = Xraw.reshape(Xraw.shape[0], Xraw.shape[1], 1)
    Traw = Traw.reshape(Traw.shape[0], Traw.shape[1], 1)
    
    print(Xtest.shape, Ytest.shape, Xraw.shape, Traw.shape)
        
    model= keras.models.Sequential([
        keras.layers.GRU(5, return_sequences=True, use_bias=False, activation='linear', input_shape=[None, 1]), 
        keras.layers.GRU(5, return_sequences=False, use_bias=False, activation='linear'), 
        keras.layers.Dense(myVars.PREDICTION_HORIZON, activation='linear')])

    model.load_weights(r"saved_models/weights.hdf5")

    pred = model.predict(Xraw)

    for i in range(Xraw.shape[0] - 1):
        plt.plot(Traw[i, :], Xraw[i, :], 'k',  linewidth=2)
        plt.plot(Traw[i+1, :myVars.PREDICTION_HORIZON], pred[i, :], 'r', linewidth=2)

    plt.xlabel('Time')
    plt.ylabel('Function Value')
    plt.legend()
    plt.grid(True)
    plt.savefig(r'info/prediction.png')
    plt.show()

Main()