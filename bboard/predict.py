import numpy as np
import pandas as pd
import uuid
import os
import datetime
import time
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense, Dropout
from sklearn.preprocessing import StandardScaler

OUT_DIR = '../../data'


def convert_dates_to_epoch_format(start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    start_date, end_date = list(map(
        (
            lambda x: int(
                time.mktime(x.replace(microsecond=0, second=0,
                                      tzinfo=None, hour=23, minute=59).timetuple()))
        ),
        [start_date, end_date]))
    return start_date, end_date


def generate_filename(file_extension):
    return str(uuid.uuid4()) + '.' + file_extension


def get_forecast(period1, period2, ticker='AAPL', interval='1d'):  # запись в файл
    generated_fn = generate_filename('csv')
    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)
    fullname = os.path.join(OUT_DIR, generated_fn)

    period1, period2 = convert_dates_to_epoch_format(period1, period2)

    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
    df = pd.read_csv(query_string)
    df.to_csv(fullname, index=False)
    print(df)
    return generated_fn

    # return df


def get_forecast1(period1, period2, ticker='AAPL', interval='1d'):
    generated_fn = generate_filename('csv')
    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)
    fullname = os.path.join(OUT_DIR, generated_fn)

    period1, period2 = convert_dates_to_epoch_format(period1, period2)

    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
    df = pd.read_csv(query_string)
    df.to_csv(fullname, index=False)
    return df


# start_d = '2021-10-14'
# end_d = '2022-05-07'


def calculate(
        data_file,
        batch_size=15,
        epochs=100,
        end_date=datetime.datetime.now().strftime("%Y-%m-%d")
):
    #     df = pd.read_csv(os.path.join(OUT_DIR, data_file))
    df = data_file
    train_dates = pd.to_datetime(df['Date'])
    cols = list(df)[1:6]
    df_for_training = df[cols].astype(float)
    scaler = StandardScaler()
    scaler = scaler.fit(df_for_training)
    df_for_training_scaled = scaler.transform(df_for_training)

    trainX = []
    trainY = []

    n_future = 5  # Number of days we want to predict into the future
    n_past = 10  # Number of past days we want to use to predict the future

    for i in range(n_past, len(df_for_training_scaled) - n_future + 1):
        trainX.append(df_for_training_scaled[i - n_past:i, 0:df_for_training.shape[1]])
        trainY.append(df_for_training_scaled[i:i + n_future, 4])
    trainX, trainY = np.array(trainX), np.array(trainY)

    model = Sequential()
    model.add(LSTM(64, activation='tanh', input_shape=(trainX.shape[1], trainX.shape[2]), return_sequences=True))
    model.add(LSTM(32, activation='tanh', return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(trainY.shape[1]))

    model.compile(optimizer='adam', loss='mse')
    model.summary()

    model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, validation_split=0.1, verbose=1)

    n_future = 5  # Redefining n_future to extend prediction dates beyond original n_future dates...
    forecast_period_dates = pd.date_range(list(train_dates)[-1], periods=n_future, freq='1d').tolist()

    forecast = model.predict(trainX[-n_past:])
    forecast_copies = np.repeat(forecast, df_for_training.shape[1], axis=-1)
    forecast_copies = np.array([np.array_split(row, 5) for row in forecast_copies])
    scaler.inverse_transform(forecast_copies[0])
    y_pred_future = scaler.inverse_transform(forecast_copies[0])[:, 4]
    forecast_dates = []
    for time_i in forecast_period_dates:
        forecast_dates.append(time_i.date())
    df_forecast = pd.DataFrame({'Date': np.array(forecast_dates), 'Adj Close': y_pred_future})
    print(df_forecast)
    return df_forecast


def predict(start_d, end_d, name):
    generated_filename = get_forecast(start_d, end_d, name)
    df = pd.read_csv(os.path.join(OUT_DIR, generated_filename))
    df_forecast = calculate(df)
    df_forecast['Date'] = df_forecast['Date'].apply(lambda x: x.strftime("%Y-%m-%d"))
    l = []
    for row in df_forecast.values:
        row_dict = {'price': row[1], 'date': row[0]}
        print(row_dict)
        l.append(row_dict)
    return l