# Uber_Fare_Pricing

DataSet : https://www.kaggle.com/nivednambiar/uber-fare-pricing-predictor/data

Goal: Analysis of fare price for UBER customers based on different featurs.

Problem Statement:
The dataset contains information about passengers trips using UBER cars. Here we have information about their trip date and time alongside the atitude and longitude of pickup and dropoff points and number of passengers. The aim of the project is to use a regression model to predict the fare price for a trip.


Content Attributes:

key - a unique identifier for each trip
fare_amount - the cost of each trip in usd
pickup_datetime - date and time when the meter was engaged
passenger_count - the number of passengers in the vehicle (driver entered value)
pickup_longitude - the longitude where the meter was engaged
pickup_latitude - the latitude where the meter was engaged
dropoff_longitude - the longitude where the meter was disengaged
dropoff_latitude - the latitude where the meter was disengaged

Model deployment as a web service on local machine
To test the model deployment as a web service - open 2 separate terminal sessions into your machine (where all this code resides) and activate the virtual environment

From one terminal session run the following command to host the prediction model as a web service.

waitress-serve --listen 127.0.0.1:5000 predict:predict
From other terminal session from the cloned project directory, execute the following command to make a request to this web service:

python predict.py
The result would be like this: 

![Capture](https://user-images.githubusercontent.com/62038461/150739695-de58bcc5-6da6-4f55-ae82-02747a350691.PNG)


Deploy model as a web service to Docker container
You can deploy the trained model as a web service running inside a docker container on your local machine.

Pre-requisites: You should have Docker installed and running on the machine where you want to perform model deployment to docker. Run the below commands to check whether docker service is running and then to see if any docker containers are running.

systemctl status docker docker ps -a Following are the steps to do this:

Clone this repo (if you have not done this already. If done then skip this step) Change to the directory that has the model file, python script (predict.py) for the web service and other required files cd mlzoomcamp-third-project/app-deploy Build docker image named Uber_Fare_Pricing docker build -t "Uber_Fare_Pricing" . Check docker image available. Output of below command should show the image with name Uber_Fare_Pricing docker images Create a docker container from the image. The model prediction script as a web service will then be running inside this container. Below command will create and run a docker container named Uber_Fare_Pricing (--name Uber_Fare_Pricing) running as a daemon i.e. non-interactive mode (-d), mapping the port 5000 on host to port 5000 on container (-p 5000:5000 first port is host port, second is container port. If you want to map different port on host just change the first number), from image Uber_Fare_Pricing. The container will be deleted if stopped or when you shutdown your machine (--rm).

docker run --rm --name predict -d -p 5000:5000 Uber_Fare_Pricing

Check whether docker container running. Below command should show the container in Running state and not Exited.

docker ps -a

Test sending some sample customer data to the web service and see the results. For this you can use the predict.py script provided as part of this repo, which has some sample customer entries and can make a request to the Web app service. Ensure you have activated the virtual environment as explained in 4. Virtual environment and package dependencies. Check whether you are already in the project directory which you cloned from git. If not change to that directory.

python predict.py
