import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn 
import streamlit as slt
df = pd.read_csv("D:/python/unified fourth project/European_Bank.csv")
print(df.head())
print(df.info())
print(df.describe())
print(df.shape)

for i in df.columns:
    if df[i].isnull().sum() > 0:
        print(i, "is null")
    else:
        print(i, "is not null")
   
print("HasCrCard:", df['HasCrCard'].unique())
print("IsActiveMember:", df['IsActiveMember'].unique())
print("Exited (Target):", df['Exited'].unique())

df.drop(columns=["Surname","CustomerId"], inplace=True)

df['Gender']= df["Gender"].map({"Male":1, "Female":0})

df = pd.get_dummies(df, columns=['Geography'])

# Final check
print(df.head())


# customer segmentation design
# age sagmentation
df["Age_Group"] = pd.cut(df["Age"], bins=[0, 30, 45, 60, 100], labels=["<30", "30-45", "46-60", "60+"])

# credit score segmentation
df["Credit_Group"] = pd.cut(df["CreditScore"], bins=[0, 500, 700, 850], labels=["Low", "Medium", "High"])

# tenure segmentation
df["Tenure_Group"] = pd.cut(df["Tenure"], bins=[-1, 3, 7, 10], labels=['New', 'Mid-term', 'Long-term'])

# balance segmentation
df["Balance_Group"] = pd.cut(df["Balance"], bins=[-1, 1, 100000, df['Balance'].max()],labels=['Zero-balance', 'Low-balance', 'High-balance'])

print(df[['Age_Group','Credit_Group','Tenure_Group','Balance_Group']].head())



#churn distribution analysis
# overall churn rate
churn_rate = df['Exited'].mean()
print(f"Overall Churn Rate: {churn_rate:.2%}")

# churn rate by age group
age_churn = df.groupby('Age_Group')['Exited'].mean()
print(f"Churn Rate by Age Group:\n{age_churn}")

# churn rate by region
geo_churn = df.groupby('Geography_Germany')['Exited'].mean()
print(f"Churn Rate by Region:\n{geo_churn}")

# total churn count
churn_count = df['Exited'].value_counts()
print(f"Total Churn Count:\n{churn_count}")

# compare churned vs retained customers
churned = df[df['Exited'] == 1]
retained = df[df['Exited'] == 0]

print("Avg Balance - Churned:", churned['Balance'].mean())
print("Avg Balance - Retained:", retained['Balance'].mean())



# comarative demographic analysis
# gender-based churn analysis
gender_churn = df.groupby('Gender')['Exited'].mean()
print(f"Churn Rate by Gender:\n{gender_churn}")

# churn rate by region and age group
geo_age = df.groupby(['Geography_Germany', 'Age_Group'])['Exited'].mean().unstack()
print(f"Churn Rate by Region and Age Group:\n{geo_age}")

# financial stability and churn
print(f"Churn Rate by Credit Score Group:\n{df.groupby('Credit_Group')['Exited'].mean()}")
print(f"Churn Rate by Balance Group:\n{df.groupby('Balance_Group')['Exited'].mean()}")



# High-Value Customer Churn Analysis
# high balance churn
high_balance = df[df['Balance_Group'] == 'High-balance']
print("High Balance Churn Rate:", high_balance['Exited'].mean())

#  salary vs balance churn analysis
print(f"Financial Characteristics by Churn Status:\n{df[['EstimatedSalary', 'Balance', 'Exited']].groupby('Exited').mean()}")

# Revenue risk
revenue_risk = churned['Balance'].sum()
print(f"Total Balance Lost Due to Churn: {revenue_risk}")

df.drop('Age',axis=1,inplace=True)
df.to_csv("D:/python/unified fourth project/European_Bank_Cleaned.csv", index=False)

