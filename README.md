# Problem Framing

Processing power has been always one of the biggest concerns in every type of computation. Specifically, in statistical modelling and big data, when it requires intensive computation methods, processing power becomes vital.
Sometimes we use statistical modelling in order to interpret the result and might not care about predictions, however, we require the result to be available as soon as possible, like when we use simple GLM models. In other occasions we might not care about the interpretability as algorithm is a black-box and does not let us to have ability of interpretability, but we care about predictions for large data such as various random forest methods, XGBoost etc or even more complicated algorithms such as Neural Networks, which provide overly complicated algorithm that requires very intensive computational power when runs against big data.
For the purpose of this practical we are simulating set of data as well as real life dataset (wind farms dataset) to construct and fit a neural network model and then gauge the completion time and percentage of CPU engagement on four different google compute engine instances.
After all, we compare CPU usage time and the percentage of each CPU has been used to perform the task along with the monthly price of each instance on the google cloud platform.
This process helps the user to decide what kind hardware specification a desired instance needs to have in order to run this particular type of modelling.

# Prototyping

In order to run this experiment, container-based applications such as Docker and Google Cloud platform have been used. Firstly, a base image has been deployed locally and modified according to the requirements of this experiment in order to provide a unique container for the purpose of this experiment.
R and Python compilers have been installed on Debian GNU/Linux 9 (stretch) (n1-standard-
1) and then a R code which simulates a dataset and runs a Neural Network on that dataset copied on the container. The R code, simulates, 2500 point for two variables x and z and then using x and y we create a complicated nonlinear relationship on variable y and then we try to fit a neural network with y, function of x and y (y ~ x + z). It also computes predictions and provides required plots in pdf formats for clear conclusion on the model and predictions.
 
The modified Docker container that has been prepared locally, then pushed into Docker hub in a private repository and from there it can be deployed anywhere in order to benefit container-based applications advantages such as google cloud platform.
In the google cloud platform we decided to deploy 4 different instances as below along with estimated monthly price for each of them:

![table1](https://user-images.githubusercontent.com/32543461/59111475-04e88800-8939-11e9-9c96-9f5566183391.JPG)

Since, in compute engine there is constrain on number of CPU per region, Instance-4 has been deployed on a different region. However, from individual testing it is very unlikely that it affects the outcome of this experiment.
Using the provided Docker images in Docker Hub for this experiment, instance-1 has been deployed, however, in order to ease this process and have a quicker procedure. Image of instance-1 has been taken in google cloud platform and instances 2,3 and 4 have been deployed using the instance-1’s image. This way we could mitigate some of the docker push image overhead. This helps especially when deploying instances through Python scripts directly (future work section).
After preparing all the instances, the provided R code that fits a neural network has been run on every instance. As benchmark every “step” (first column) of fitting the model
 
observed, as we can see in the below figure. We can see that how early each instance has reached step 7000 mark.

![7000 Mark](https://user-images.githubusercontent.com/32543461/59111544-1cc00c00-8939-11e9-919e-97bb896f0f02.jpg)

Since the logs are being loaded from the bottom as model fitting gets completed, the higher the red arrow the earlier that instance has reached the 7000 mark. It is interesting that instance number two is much slower than instance-1 even though it has higher configuration.
Finally, we can obtain the completion time up on end of the model fitting which can be seen in the below table for each instance, when we ran the experiments twice:

![table2](https://user-images.githubusercontent.com/32543461/59111602-3e20f800-8939-11e9-83e8-614912aadbdd.JPG)

Right after running the experiments, a Python code which has been developed locally on a local machine run and collects CPU metrics from each google cloud instance.
 
However, Python code must authenticate first in order to access the GCP, which had been achieved by deploying a Jason file locally that holds the credentials and private key details from GCP.
The code, collects and stores all the reading metric data and after classifying them for each instance into a NumPy array, it stores them in a text file and from there we call another function to store the information in a CSV format. This way the other R code which has been developed to visualize the result can use the metrics data in CSV for comparison and provide insight about the collected metrics.

# Evaluation

For evaluation and visualize the collected data, R code reads in all the collected data from the provided CSV fie and uses ggplot2 library to visualize the data.
In the below figure we can see performance of each instance for two rounds of experiments:

![image](https://user-images.githubusercontent.com/32543461/59111658-5abd3000-8939-11e9-9730-007b21633d88.png)

In this figure we can see, first round of experiment on the left side and second round of experiment on the right side of the down time between time index of 9 to 13. It be clearly seen that instane-1 with 1 CPU has used all its capacity in order to perform the model fitting, while instance 2 is just using 25 percent of CPU capacity for both experiments and instance 3 and 4 are using much lower capacity in order to perform our experiment. It means that instances 2,3 and 4 can allocate CPU time to other tasks while instance-1 does not seem to be able to any other tasks comfortably while running the required task.


Eventually, collecting all the metrics and estimated monthly prices and previous analysis we use a bar chart in order to have overall comparison among these evaluated instances using the same R code.


![image](https://user-images.githubusercontent.com/32543461/59111679-66a8f200-8939-11e9-9872-717b297a92a3.png)

As can be seen in the above figure, for every instance the completion time of task in both rounds are almost the same which is almost the same even among different instance with just maybe maximum one-minute difference. For sure, instance number four has done the better job, but depending on the situation we need to know if it worth the cost.
In conclusion, for the current analysis, it might not be very reasonable to invest 388.76 USD for running a task that finishes only one minute earlier compare to an instance which costs
 
only 24.67 USD per month. However, depending on the situation, we should for sure consider CPU engagement time (figure 2). Since cheaper instance (instance-1) has used 100% of the CPU capacity in order to run the experiment while other instances did not feel the pressure as much and they are able to easily run other tasks along with our experiment.

# Future Work

As a future work this experiment can be all automated and using Python or R script, we can deploy, list and delete instances directly from our Python code and run our benchmark on every instance and pull the metrics and visualize the result.

