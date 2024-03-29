# -*- coding: utf-8 -*-
"""Clustering.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15eSX2-pdh14rnG-FTBrrVf4SY8bAi_Sm
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from yellowbrick.cluster import KElbowVisualizer
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from kmodes.kprototypes import KPrototypes
from sklearn.cluster import KMeans

# Import the dataset and Removing the customer id column from the dataset as it provides no useful data, no split for k-means
dataset = pd.read_csv("marketing_campaign.csv")
dataset.head()

n_row,n_col = dataset.shape
print("The number of rows in dataset are {0} and the number of columns are {1} ".format(n_row,n_col))

# Information on dataset before removing unnecessary columns

dataset.info()
dataset.describe(include='all')

# The columns for Z_CostContact and Z_Revenue provide no useful information for my analysis, therefore I remove them.
dataset.drop(columns=["ID", "Z_CostContact", "Z_Revenue"], inplace=True, errors='ignore')


# information on dataset after removing unnecessary columns
dataset.info()

# Having a mix data type, Dt_Customer is data type object
# Education and Martial_Status are categorical features
# Income has missing values

# Exploring the categorical features
print(dataset["Marital_Status"].value_counts())

# Exploring the categorical features
print(dataset["Marital_Status"].value_counts())
print(dataset["Education"].value_counts())

# Feature Engineering
dataset["Marital_Status"].replace({"Alone":"Single","Absurd":"Single", "YOLO":"Single"},inplace=True)

# Replace data of birth with age

dataset["Year_Birth"] = 2022-dataset["Year_Birth"]
dataset.rename(columns={"Year_Birth":"Age"},inplace = True)
dataset.head()

# total Spending on all items
dataset["Total_Spent"] = dataset["MntWines"]+dataset["MntFruits"]+dataset["MntMeatProducts"]+dataset["MntFishProducts"]+dataset["MntSweetProducts"]+dataset["MntGoldProds"]

# Creating a new feature showing the number of days of customer engagement
dataset["Dt_Customer"] = pd.to_datetime(dataset.Dt_Customer)
newest_customer = dataset["Dt_Customer"].max()
dataset["newest_customer"] = newest_customer
dataset["days_engaged"]=(dataset["newest_customer"] - dataset["Dt_Customer"]).dt.days
print(dataset["days_engaged"])
dataset.drop(columns=["Dt_Customer","newest_customer"],inplace=True)
dataset.describe()

# Data Cleaning process in order to target NaN values
dataset.isna().sum
dataset.dropna(inplace = True)

# Checking on the relevant features
plt.figure()
cols_to_plot = ["Income","Age","Total_Spent"]
sns.pairplot(dataset[cols_to_plot], diag_kind = "kde", diag_kws = {"color":"g"}, plot_kws={"color":"y"})
plt.show()

# dropping the outliers
dataset = dataset[dataset["Age"]<100]
dataset = dataset[(dataset["Income"]<600000)]

# Number of samples after cleaning
print(len(dataset))

# Show casing the correlation among the features
numeric_dataset = dataset.select_dtypes(include=['int64', 'float64'])
plt.figure(figsize = (16,9))
sns.heatmap(dataset.corr(),cmap="viridis",annot = True)
plt.title("Correlation matrix")
plt.show()

# encoding ordinal features using OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler, MinMaxScaler
education_order = ["Basic","2n Cycle","Graduation","Master","PhD"]
oe = OrdinalEncoder(categories = [education_order], dtype = int)
education_oe = oe.fit_transform(dataset[["Education"]])
dataset_enc = dataset.assign(Education_encode=education_oe)
print(dataset_enc.shape)
print(dataset_enc[["Education","Education_encode"]])

ohe = OneHotEncoder(dtype="int")
Marital_ohe = ohe.fit_transform(dataset[["Marital_Status"]])
Marital_ohe = pd.DataFrame(data=Marital_ohe.toarray(),columns=ohe.get_feature_names_out(["Marital_Status"]), index=dataset.index,)
dataset_enc = pd.concat([dataset_enc,Marital_ohe],axis=1)
dataset_enc.drop(columns=["Marital_Status","Education"],inplace=True)
dataset_enc.info()


binary_columns = ["Marital_Status_Divorced","Marital_Status_Married","Marital_Status_Single","Marital_Status_Together","AcceptedCmp3","AcceptedCmp4","AcceptedCmp5","AcceptedCmp1","AcceptedCmp2","Complain","Response"]
dataset_to_scaler = dataset_enc.drop(columns = binary_columns)
scaler = StandardScaler().fit_transform(dataset_to_scaler)
scaled_dataset = pd.DataFrame(scaler,columns = dataset_to_scaler.columns)
binary_series = dataset_enc[binary_columns]
scaled_dataset = pd.concat([scaled_dataset,binary_series],axis=1)
scaled_dataset.isna().sum()
scaled_dataset = scaled_dataset.fillna(0)

# Dimensionality Reduction with PCA
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
pca = PCA(n_components = 3)
pca.fit(scaled_dataset)
PCA_dataset = pd.DataFrame(pca.transform(scaled_dataset),columns =(["feature1","feature2","feature3"]))

# Plotting
plt.figure(figsize=(10,8))
plt.axes(projection="3d").scatter(PCA_dataset["feature1"],PCA_dataset["feature2"],PCA_dataset["feature3"])
plt.axes(projection="3d").scatter(PCA_dataset["feature1"],PCA_dataset["feature2"],PCA_dataset["feature3"])
plt.title("A 3D Projection of Data In Reduced Dimension")
plt.show()


# Clustering
from yellowbrick.cluster import KElbowVisualizer
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
Elbow_M = KElbowVisualizer(KMeans(),k=(2,11))
Elbow_M.fit(PCA_dataset)
Elbow_M.show()

# Using elbow curve to find the optimum number of clusters
# The Agglomerative Clustering model

AC = AgglomerativeClustering(n_clusters=4)
yhat_AC = AC.fit_predict(PCA_dataset)
PCA_dataset["Clusters"] = yhat_AC
scaled_dataset["Clusters"] = yhat_AC

# Plotting Clusters
fig = plt.figure(figsize=(10,8))
plt.axes(projection="3d").scatter(PCA_dataset["feature1"],PCA_dataset["feature2"],PCA_dataset["feature3"])
plt.title("The Clusters by Agglomerative Model")

sns.scatterplot(data = scaled_dataset,x=scaled_dataset["Total_Spent"], y = scaled_dataset["Income"], hue = scaled_dataset["Clusters"])
plt.title("Cluster's Profile Based on Income and Total Spending")

# Clustering using K-Means Model

kmeans = KMeans(n_clusters = 4, init = "k-means++", random_state = 50)
# fit model and predict clusters
labels = kmeans.fit_predict(PCA_dataset)
PCA_dataset["Clusters"] = labels
# Adding the Clusters feature to the original dataframe
scaled_dataset["Clusters"] = labels

# plotting the clusters
fig = plt.fig(figsize=(10,8))
ax = plt.subplot(111,projection="3d",label = "bla")
ax.scatter(PCA_dataset["feature1"],PCA_dataset["feature2"],PCA_dataset["feature3"], s = 40, c = PCA_dataset["Clusters"])
ax.set_title("Clustering by K-Means model")
plt.show()