import pandas as pd
from pandas import Series,DataFrame
df=pd.read_csv('train.csv')
df.head()
df.info()

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import Series,DataFrame


titanic_df = pd.read_csv('train.csv')


titanic_df.head()


import seaborn as sns
%matplotlib inline
# check gender
sns.factorplot('Sex',data=titanic_df)

sns.factorplot('Pclass',data=titanic_df,hue='Sex')

# function to sort through the sex 
def male_female_child(passenger):
   
    age,sex = passenger

    if age < 16:
        return 'child'
    else:
        return sex
    

# define a new column called 'person'
titanic_df['person'] = titanic_df[['Age','Sex']].apply(male_female_child,axis=1)
#check out the first ten rows
titanic_df[0:10]

#  histogram using pandas
titanic_df['Age'].hist(bins=70)
# quick overall comparison of male,female,child
titanic_df['person'].value_counts()

fig = sns.FacetGrid(titanic_df, hue="Sex",aspect=4)


fig.map(sns.kdeplot,'Age',shade= True)

oldest = titanic_df['Age'].max()

# no one can be negative years old set the x lower limit at 0
fig.set(xlim=(0,oldest))

#add a legend
fig.add_legend()

fig = sns.FacetGrid(titanic_df, hue="person",aspect=4)
fig.map(sns.kdeplot,'Age',shade= True)
oldest = titanic_df['Age'].max()
fig.set(xlim=(0,oldest))
fig.add_legend()
# drop the NaN values and create a new object, 
deck = titanic_df['Cabin'].dropna()
levels = []

# Loop to grab first letter
for level in deck:
    levels.append(level[0])    

# Reset DataFrame 
cabin_df = DataFrame(levels)
cabin_df.columns = ['Cabin']
sns.factorplot('Cabin',data=cabin_df,palette='winter_d')
# Redefine cabin_df as everything but where the row was equal to 'T'
cabin_df = cabin_df[cabin_df.Cabin != 'T']
#Replot
sns.factorplot('Cabin',data=cabin_df,palette='summer')
# Now we can make a quick factorplot to check out the results, note the x_order argument, used to deal with NaN values
sns.factorplot('Embarked',data=titanic_df,hue='Pclass',x_order=['C','Q','S'])
# Let's start by adding a new column to define alone

# We'll add the parent/child column with the sibsp column
titanic_df['Alone'] =  titanic_df.Parch + titanic_df.SibSp
titanic_df['Alone']
# Look for >0 or ==0 to set alone status
titanic_df['Alone'].loc[titanic_df['Alone'] >0] = 'With Family'
titanic_df['Alone'].loc[titanic_df['Alone'] == 0] = 'Alone'


titanic_df.head()
# Now let's get a simple visualization!
sns.factorplot('Alone',data=titanic_df,palette='Blues')
# a new column for legibility purposes through mapping 
titanic_df["Survivor"] = titanic_df.Survived.map({0: "no", 1: "yes"})

#  quick overall view of survied vs died. 
sns.factorplot('Survivor',data=titanic_df,palette='Set1')
sns.factorplot('Pclass','Survived',data=titanic_df)
sns.factorplot('Pclass','Survived',hue='person',data=titanic_df)
