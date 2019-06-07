set.seed(1231239)

# create an unusual regression problem
# note that these variables will already have the proper scaling
x<-runif(2500)
z<-runif(2500)

# the relationship between y and the independent variables
# is complex and non-linear
y<-sin(3*pi*x)+cos(3*pi*z)+rnorm(1000, mean=0, sd=0.25)
plot(y~x)
plot(y~z)
dat<-data.frame(x,z,y)

# estimate a neural network with one hidden layer of 4 nodes

library(neuralnet)
nn<-neuralnet(y~x+z, data=dat, hidden=10, stepmax=9e05, threshold=0.02, lifesign="full")
plot(nn)

# do the predictions of the neural network look good?
x.test<-seq(from=0, to=1, by=0.01)
y.fit<-compute(nn, covariate=matrix(c(x.test, rep(0.5, length(x.test))), nrow=length(x.test), ncol=2))$net.result
plot(y~x, data=dat)
lines(y.fit~x.test, type="l", col="red", lwd=2)
