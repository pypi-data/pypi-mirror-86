# 필수 패키지를 import합니다.
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn import utils
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow as tf
from tensorflow.keras.models import Sequential
tf.random.set_seed(777) #하이퍼파라미터 튜닝을 위해 실행시 마다 변수가 같은 초기값 가지게 하기

def stock(filePath) : 

    ## 데이터 로드
    #df = pd.read_csv('YG_PLUS.csv')
    df = pd.read_csv(filePath)
    
    ## 데이터 분석
    print("head") #앞 5개 확인 
    print(df.head()) 
    
    print("info") # 정보 확인 
    print(df.info())
    
    print("describe") # 전체적인 폼 형성 
    print(df.describe())
    
    
    ## 데이터 전처리
    
    # 4 속성 이용
    df = df[['Open', 'High', 'Low', 'Close']]
    print(df)
    #df = df[::-1]
    
    # test용, train용 나눔 
    data = df.values
    print("data", len(data), data)
    train = data[:(len(data) - int(len(data)*0.2))]
    test = data[:int(len(data)*0.2)]
    #train = train[::-1]
    #test = test[::-1]
    print("test",len(test),test)
    print("train",len(train),train)
    
    # 전처리 전 데이터
    bftest = test
    bftrain = train
    
    # feature 값이 0~1 사이에 있도록 데이터 재조정
    transformer = MinMaxScaler()
    train = transformer.fit_transform(train)
    test = transformer.transform(test)
    
    sequence_length = 5
    window_length = sequence_length + 1
    
    x_train = []
    y_train = []
    
    # window만큼(?) 자른 걸 배열에 넣어서 x_train, y_train에 넣어줄 것임
    for i in range(0, len(test) - window_length + 1):
        # window = train의 i~(i+window_length-1)행(전체열)
        window = train[i:i + window_length, :]
        # x_train에 window의 마지막 행 제외한 나머지행(전체열) 더함
        x_train.append(window[:-1, :])
        # y_train에 window의 마지막 행(마지막 열) 더함
        y_train.append(window[-1, [-1]])
    x_train = np.array(x_train)
    y_train = np.array(y_train)
    
    x_test = []
    y_test = []
    for i in range(0, len(test) - window_length + 1):
        window = test[i:i + window_length, :]
        x_test.append(window[:-1, :])
        y_test.append(window[-1, [-1]])
    x_test = np.array(x_test)
    y_test = np.array(y_test)
    
    utils.shuffle(x_train, y_train)
    
    ## 모델 학습
    ## 모델 검증
    
    model = Sequential()
    # 5일 4개(시,고,저,종가)의 데이터
    model.add(LSTM(units=512, input_shape=(sequence_length, 4)))
    model.add(Dense(units=512, activation='relu'))
    model.add(Dense(units=512, activation='relu'))
    # target 1개
    model.add(Dense(units=1))
    
    model.summary()
    
    # 연속적인 값 예측하므로 손실함수 mse 사용
    # 손실함수 : 평균제곱오차, 최적화 : adam
    model.compile(loss='mean_squared_error', optimizer=Adam(lr=0.01), metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=50, validation_data=(x_test, y_test)) 
    
    
    #y_test
    #inverseList
    #y_test_inverse
    inverseList = []
    ## 모델 예측
    y_test_inverse = []
    for y in y_test:
        inverse = transformer.inverse_transform([[0, 0, 0, y[0]]])
        inverseList.append(inverse)
        y_inverse = inverse.flatten()[-1]
        y_test_inverse.append(y_inverse)
    
    y_predict = model.predict(x_test)
    y_predict_inverse = []
    for y in y_predict:
        inverse = transformer.inverse_transform([[0, 0, 0, y[0]]])
        y_inverse = inverse.flatten()[-1]
        #print(y_inverse)
        y_predict_inverse.append(y_inverse)
    
    
    import matplotlib.pyplot as plt
    #plt.plot( y_test_inverse)
    #plt.plot(y_predict_inverse)
    
    #plt.xlabel('Time Period')
    #plt.ylabel('Close')
    #plt.show()
 
    answer = np.array(y_test_inverse)
    result = np.array(y_predict_inverse)
    zero = np.zeros(answer.shape)
    difference = answer - result
    plt.plot(difference)
    plt.plot(zero)
    plt.xlabel('Time Period')
    plt.ylabel('money')
    plt.legend(['train', 'test'])
    plt.title('YG_PLUS')
    plt.show()

stock('YG_PLUS.csv')
