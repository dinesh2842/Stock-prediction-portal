from django.shortcuts import render
from .seriializers import StockzSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
from django.conf import settings
from .utils import *
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
#mean squared error measures the squares between predicted values and actual values
from sklearn.metrics import mean_squared_error , r2_score


class StockPredictionApiView(APIView):
    def post(self,request):
        serializer = StockzSerializer(data=request.data)
        if serializer.is_valid():
            ticker = serializer.validated_data['ticker']

            # Fetch the data from yfinance
            now = datetime.now()
            start = datetime(now.year-10, now.month, now.day)
            end = now
            df = yf.download(ticker, start, end)
            
            if df.empty:
                 return Response({
                    'status': 'Error',
                    'error': 'No data found for the given ticker.'
                }, status=status.HTTP_404_NOT_FOUND)
            
            df = df.reset_index()
            # Generate basic Plot
            plt.switch_backend('AGG')
            plt.figure(figsize=(12,5))
            plt.plot(df.Close,label='Closing Price')
            plt.title(f'Closing Price of {ticker}')
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.legend()

            #save the plot to a file
            plot_img_path = f'{ticker}_plog.png'
            
            plot_img = save_plot(plot_img_path)

            #100 days moving challenge
            ma100 = df.Close.rolling(100).mean()
            plt.switch_backend('AGG')
            plt.figure(figsize=(12,5))
            plt.plot(df.Close,label='Closing Price')
            plt.plot(ma100,'r',label='100 DMA')
            plt.title(f'100 days moving average of {ticker}')
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.legend()
            plot_img_path = f'{ticker}_100_dma.png'
            
            plot_100_dma = save_plot(plot_img_path)

            #200 days moving challenge
            ma200 = df.Close.rolling(200).mean()
            plt.switch_backend('AGG')
            plt.figure(figsize=(12,5))
            plt.plot(df.Close,label='Closing Price')
            plt.plot(ma100,'r',label='100 DMA')
            plt.plot(ma200,'g',label='200 DMA')

            plt.title(f'200 days moving average of{ticker}')
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.legend()
            # 100 days plot
            # plot_img_path_100 = f'{ticker}_100_dma.png'
            # plot_100_dma = save_plot(plot_img_path_100)

            # 200 days plot
            plot_img_path_200 = f'{ticker}_200_dma.png'
            plot_200_dma = save_plot(plot_img_path_200)


            # splitting data into training & Testing datasets
            data_training = pd.DataFrame(df.Close[0:int(len(df)*0.7)])
            data_testing = pd.DataFrame(df.Close[int(len(df)*0.7):int(len(df))])

            # scaling down the data between 0 and 1
            scaler = MinMaxScaler(feature_range=(0,1))  

            #Load ML model
            model = load_model('stock_prediction_model.keras')

            #prepare the test data
            past_100_days = data_training.tail(100)
            final_df = pd.concat([past_100_days,data_testing],ignore_index=True)
            input_data = scaler.fit_transform(final_df)

            x_test = []
            y_test = []
            for i in range(100,input_data.shape[0]):  # index of the rows is 0 (input_data.shape)
                x_test.append(input_data[i-100:i])
                y_test.append(input_data[i,0])
            x_test,y_test=np.array(x_test),np.array(y_test)

            #Making predictions
            y_predicted = model.predict(x_test)

            #Revert the scaled prices to original price
            y_predicted = scaler.inverse_transform(y_predicted.reshape(-1,1)).flatten() #now we want to take the scaled data and convert back it to original state 
            #-1 means automatically calculate the no. of rows based on the length of the data and the number of columns , 1 is columns , we use flatten() to convert 
            #it into 1D array
            y_test = scaler.inverse_transform(y_test.reshape(-1,1)).flatten() # confirming that both of these will be in the same shape
            

            
            #plot the final prediction

             #200 days moving challenge
           
            plt.switch_backend('AGG')
            plt.figure(figsize=(12,5))
            plt.plot(y_test,'b',label='Original Price')
            plt.plot(y_predicted,'r',label='Predicted price')


            plt.title(f'Final prediction for the{ticker}')
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.legend()
            # 100 days plot
            # plot_img_path_100 = f'{ticker}_100_dma.png'
            # plot_100_dma = save_plot(plot_img_path_100)

            # 200 days plot
            plot_img_path = f'{ticker}final_prediction.png'
            plot_prediction = save_plot(plot_img_path)

            #model evaluation
            #mse
            mse = mean_squared_error(y_test,y_predicted)

            #root mean squared error(rmse) square root od mse
            rmse = np.sqrt(mse)

            # R-squared how will model prediction values will match your actual values
            r2 = r2_score(y_test,y_predicted)


            return Response(
                {'status':'Success',
                 'plot_img':plot_img,
                 'plot_100_dma':plot_100_dma,
                'plot_200_dma':plot_200_dma,
                'plot_prediction':plot_prediction,
                'mse':mse,
                'rmse':rmse,
                'r2':r2,


                 })
        

