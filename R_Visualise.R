#  Loading Libraries
library(latticeExtra)
library(ggplot2)

# Reading in data
data <- read.csv("mycsv.csv")
data <- na.omit(data)
data$instance <- factor(data$instance)
attach(data)
write.csv(data, file = "final.csv")
data2 <- read.csv("final.csv")


# Plotting CPU Usage for 4 instances
ggplot(data2, aes(x=time, y=value, group=Instance.Type)) +
  geom_line(aes(color=Instance.Type))+
  geom_point(aes(color=Instance.Type)) +
  scale_x_continuous(breaks = round(seq(min(data2$time), max(data2$time), by = 1),1)) +
  labs(x = "Time index, 10 sec Aggregation", y= "CPU Usage %")

# Creating Matrix of Instances details
instance.list <- matrix(
  c(24.67,14.94,14.94,97.49,15.26,15.4,199.58,14.97,14.98,388.76,14.62,14.58), nrow = 3)
colnames(instance.list) <- c("1vCPU-3.75GB", "4vCPU-15GB", "8vCPU-30GB", "16vCPU-60GB")
row.names(instance.list) <- c("Price", "NN_Round1", "NN_Round2")

# Using the matrix, plotting the instance details and comparisions
p<- barplot(instance.list, col=colors()[c(45,55,77)],  border="white", font.axis=2,
        legend=rownames(instance.list), beside= T,xlab="Instance Types", font.lab=2,
        main = "Comparison of Instances", args.legend = list(x='topleft',inset=c(-0.001,-0.11),xpd = TRUE))
text(p,0, instance.list, cex = 1, pos = 3)


