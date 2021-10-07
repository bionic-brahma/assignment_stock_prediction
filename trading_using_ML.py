###################################################
import threading
import pandas as pd
import pandas_datareader.data as web
import datetime
from sklearn import linear_model
from time import sleep
import joblib
##################################################


# this class is to give colors to the print statements
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# This function will give the price after the delay of sleep_time units of seconds
def getprice(label="WIPRO.NS", sleep_time=1):
    # Pause for sleep_time number of seconds
    sleep(sleep_time)
    # Using yahoo finance to get the stock market live data
    quote = web.get_quote_yahoo(label)
    price = quote["price"].values[0]
    current_time = datetime.datetime.now()
    return tuple([price, current_time])


# This function trains the model using the input data(dataframe)
def train(input):
    print("\nModel updating...", end=" ")
    # We take last column of the features as target and rest are taken as attributes
    featureMat = input.iloc[:, : len(input.columns) - 1]
    label = input[input.columns[-1]]
    # Here we are using linear regression model
    model = linear_model.LinearRegression()
    model.fit(featureMat, label)
    # Model is being written on the hard drive
    joblib.dump(model, "modelLR.pkl")
    print("[Completed]")


##########################  Training over  ################################

# Increase the values of these variables to get improved results
# but if you will increase them then you have to wait for
#
#               (number_of_features X training_record_criteran) X steep_time units seconds
#
# for first training

number_of_features = 5  # This indicates how many columns the dataframe will have.
training_record_criterian = 5  # This decides how frequently the model will update [5 new features -> retrain the model]
number_of_predictions = 3  # Tells how many prediction in series you want
##################################################################################

data = pd.DataFrame(columns=range(number_of_features))  # creating an empty dataframe

predict_input = list()

while 1:

    feature = list()  # stores the features for a single record for dataframe

    for i in range(number_of_features):

        price = getprice()[0]
        feature.append(price)
        predict_input.append(price)

        try:  # this will throw exception in two cases:
            # 1> model is not yet trained and saved
            # 2> model prediction is not working.

            first_predict = True  # flag for detecting the first prediction in predicted series
            model = joblib.load("modelLR.pkl")  # trying to open the saved model (can throw exception)
            print("")
            inputlist = predict_input.copy()  # copying the list to make the prediction if model is ready
            #   printing latest 3 prices
            for feature_value in inputlist[-(3):]:
                print(f"{bcolors.WARNING} --> ", int(feature_value * 100) / 100, end=" ")
            #   taking the latest price
            price = getprice(sleep_time=0)[0]
            #   Starting the predictions
            for i in range(number_of_predictions):
                pre_price = model.predict([inputlist[-(number_of_features - 1):]])
                #   printing the predicted values one by one in the series
                print(f"{bcolors.OKBLUE} --> ", int(pre_price[0] * 100) / 100, end=" ")
                #   This block will only run for the first prediction in series
                if first_predict:
                    # When prediction tells about increase in price
                    if pre_price[0] - inputlist[-1] > 0:
                        print(f"{bcolors.OKGREEN}  \u2191", end="")
                        #   Calculating the % of increase the program predicts and printing.
                        print(f"{bcolors.BOLD}[", int((pre_price[0] - price) * 1000000 / price) / 10000, "%] ", end=" ")
                        print(f"{bcolors.OKCYAN} Actual: ", price, end="")
                    # When prediction says that no change will happen
                    elif pre_price[0] - inputlist[-1] == 0:
                        print(f"{bcolors.HEADER} \u2022", end="")
                        print(f"{bcolors.BOLD}[", int((pre_price[0] - price) * 1000000 / price) / 10000, "%] ", end=" ")
                        print(f"{bcolors.OKCYAN} Actual: ", price, end="")
                    # When prediction is about decrease in price
                    else:
                        print(f"{bcolors.FAIL}  \u2193", end="")
                        print(f"{bcolors.BOLD}[", int(-(pre_price[0] - price) * 1000000 / price) / 10000, "%] ",
                              end=" ")
                        print(f"{bcolors.OKCYAN} Actual: ", price, end="")
                    # Next statement talk about what happened actually
                    if price - inputlist[-1] > 0:
                        print(f"{bcolors.OKGREEN}  \u2191", end=" ")
                    elif price - inputlist[-1] == 0:
                        print(f"{bcolors.HEADER} \u2022", end="")
                    else:
                        print(f"{bcolors.FAIL}  \u2193", end=" ")

                    first_predict = False


                #   pushing the predicted price in the back of the input array..
                #   it will be used in predicting next element in the series
                inputlist.append(pre_price[0])
        except:

            print("Please Wait while the model is getting ready...")
    #   Adding the feature in the dataframe
    data.loc[len(data.index)] = feature
    #   If number of elements present in the dataframe is multiple of training record criterian, the retraining
    if len(data.index) % training_record_criterian == 0:
        # print(data)
        #   training in separate thread
        trainer = threading.Thread(target=train, args=(data,))
        trainer.start()
        trainer.join()
