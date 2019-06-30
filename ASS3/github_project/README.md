# Comp9321ASS3
Assignment 3 of COMP9321

# clean data
Because the data include some dirty data like '?' which may influence the accuracy, we need to replace it with cleaning data.
### a) replace '?' with the number 99.
### b) the data of 'target' include the number 2,3,4, we update these number with 1.

# data normalization
We use Min-Max Normalization to normalize the data.
The formula is : x' = (x - X_min) / (X_max - X_min)
# calculate the weight of each attribute
Using decision tree to calculate the weights

# Api
Using flask and flask_restplus to create api to provide the data to the front end.




