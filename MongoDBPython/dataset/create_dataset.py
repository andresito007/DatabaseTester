import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append('shared/')
import variables as myVars

def Main():
    dataframe = pd.read_csv(r"data/0_000.csv")
    data = np.array(dataframe[myVars.NAMES[0]])
    data = (data - np.min(data)) / (np.max(data) - np.min(data))
    time = np.arange(0, data.shape[0])

    dataSetX = np.zeros(shape=(myVars.BATCH_SIZE, myVars.LENGTH))
    dataSetY = np.zeros(shape=(myVars.BATCH_SIZE, myVars.PREDICTION_HORIZON))

    plt.plot(data)    
    plt.xlabel("Time")
    plt.ylabel("Position")
    plt.grid(True)
    plt.savefig(r'info/position.png')
    plt.show()

    maxNumBatches = int(data.shape[0] / myVars.OFFSET)
    Xraw = np.zeros(shape=(maxNumBatches, myVars.LENGTH))
    Traw = np.zeros(shape=(maxNumBatches, myVars.LENGTH))
    counter = 0
    for i in range(maxNumBatches):
        Xraw[i, :] = data[0+i*myVars.OFFSET:myVars.LENGTH+i*myVars.OFFSET]
        Traw[i, :] = time[0+i*myVars.OFFSET:myVars.LENGTH+i*myVars.OFFSET]

        counter += myVars.OFFSET
        if(data.shape[0] - counter <  myVars.LENGTH):
            break

    for i in range(myVars.BATCH_SIZE):
        dataSetX[i, :] = data[0+i*myVars.OFFSET:myVars.LENGTH+i*myVars.OFFSET]
        dataSetY[i, :] = data[myVars.LENGTH+i*myVars.OFFSET:myVars.LENGTH+myVars.PREDICTION_HORIZON+i*myVars.OFFSET]

    dataSetX = dataSetX.reshape(myVars.BATCH_SIZE, myVars.LENGTH, 1)
    dataSetY = dataSetY.reshape(myVars.BATCH_SIZE, myVars.PREDICTION_HORIZON, 1)

    Xtrain, Ytrain = dataSetX[:(int)(0.6*myVars.BATCH_SIZE),:], dataSetY[:(int)(0.6*myVars.BATCH_SIZE),:]
    Xvalid, Yvalid = dataSetX[(int)(0.6*myVars.BATCH_SIZE):(int)(0.8*myVars.BATCH_SIZE),:], dataSetY[(int)(0.6*myVars.BATCH_SIZE):(int)(0.8*myVars.BATCH_SIZE),:]
    Xtest, Ytest = dataSetX[(int)(0.8*myVars.BATCH_SIZE):,:], dataSetY[(int)(0.8*myVars.BATCH_SIZE):,:]   

    np.savetxt(r'dataset/xraw.csv', Xraw)
    np.savetxt(r'dataset/traw.csv', Traw)
    np.savetxt(r'dataset/xtrain.csv', Xtrain[:,:,0])
    np.savetxt(r'dataset/ytrain.csv', Ytrain[:,:,0])
    np.savetxt(r'dataset/xvalid.csv', Xvalid[:,:,0])
    np.savetxt(r'dataset/yvalid.csv', Yvalid[:,:,0])
    np.savetxt(r'dataset/xtest.csv', Xtest[:,:,0])
    np.savetxt(r'dataset/ytest.csv', Ytest[:,:,0])

Main()