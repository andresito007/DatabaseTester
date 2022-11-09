import sys
import numpy as np
import matplotlib.pyplot as plt

from tensorflow import keras
from keras.callbacks import ModelCheckpoint

sys.path.append('shared/')
import variables as myVars

def Main():
    Xtrain = np.loadtxt('dataset/xtrain.csv')
    Ytrain = np.loadtxt('dataset/ytrain.csv')
    Xvalid = np.loadtxt('dataset/xvalid.csv')
    Yvalid = np.loadtxt('dataset/yvalid.csv')

    Xtrain = Xtrain.reshape(Xtrain.shape[0], Xtrain.shape[1], 1)
    Ytrain = Ytrain.reshape(Ytrain.shape[0], Ytrain.shape[1], 1)
    Xvalid = Xvalid.reshape(Xvalid.shape[0], Xvalid.shape[1], 1)
    Yvalid = Yvalid.reshape(Yvalid.shape[0], Yvalid.shape[1], 1)

    model= keras.models.Sequential([
        keras.layers.GRU(5, return_sequences=True, use_bias=False, activation='linear', input_shape=[None, 1]), 
        keras.layers.GRU(5, return_sequences=False, use_bias=False, activation='linear'), 
        keras.layers.Dense(myVars.PREDICTION_HORIZON, activation='linear')])

    filepath = r"saved_models/weights.hdf5"
    callbacks_list = [ModelCheckpoint(filepath, monitor='val_loss', verbose=0, save_best_only=True, save_weights_only=False, mode='auto')]

    model.compile(loss="mean_squared_error", optimizer="adam", metrics=['mse'])
    model.summary()
    history = model.fit(Xtrain, Ytrain, batch_size=100, epochs=5000, validation_data=(Xvalid, Yvalid), callbacks=callbacks_list, verbose=2)
    
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(1, len(loss)+1)
    
    plt.figure()
    plt.plot(epochs, loss,'b', label='Training loss',linewidth=2)
    plt.plot(epochs, val_loss,'r', label='Validation loss',linewidth=2)
    plt.title('Training and validation losses')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.savefig(r'info/validation_and_loss.png')
    plt.show()

Main()