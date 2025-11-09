#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')

sns.set(style='whitegrid')


# In[60]:


df = pd.read_csv("netflix_titles.csv")

df.head()


# In[61]:


df.info()
df.isnull().sum()


# In[62]:


df['director'].fillna('Not Available', inplace=True)
df['cast'].fillna('Not Available', inplace=True)
df['country'].fillna('Unknown', inplace=True)
df['rating'].fillna('Not Rated', inplace=True)
df['date_added'].fillna('Unknown', inplace=True)


# In[63]:


plt.figure(figsize=(6,4))
sns.countplot(x='type', data=df)
plt.title("Movies vs TV Shows on Netflix")
plt.xlabel("Type of Content")
plt.ylabel("Count")
plt.show()


# In[64]:


df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

df['year_added'] = df['date_added'].dt.year

type_year = df.groupby(['year_added', 'type']).size().unstack().fillna(0)

type_year.plot(kind='bar', figsize=(12,6), stacked=False, color=['#FF6F61', '#6B5B95'])
plt.title('Movies vs TV Shows Added Each Year')
plt.xlabel('Year Added')
plt.ylabel('Number of Titles')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()


# In[65]:


plt.figure(figsize=(10,5))
df['country'].value_counts().head(10).plot(kind='bar', color='orange')
plt.title('Top 10 Countries Producing Netflix Content')
plt.xlabel('Country')
plt.ylabel('Number of Titles')
plt.show()


# In[66]:


content_trend = df['year_added'].value_counts().sort_index()

plt.figure(figsize=(10,5))
plt.plot(content_trend.index, content_trend.values, marker='o', color='purple')
plt.title('Trend of Content Added to Netflix Over the Years')
plt.xlabel('Year Added')
plt.ylabel('Number of Titles Added')
plt.grid(True)
plt.show()




# In[67]:


plt.figure(figsize=(8,5))
sns.countplot(y='rating', data=df, order=df['rating'].value_counts().index)
plt.title('Distribution of Ratings')
plt.xlabel('Count')
plt.ylabel('Rating')
plt.show()


# In[68]:


ratings = df['rating'].value_counts().head(8)

plt.figure(figsize=(7,7))
plt.pie(ratings, labels=ratings.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
plt.title("Top Ratings Distribution on Netflix")
plt.show()


# In[69]:


from collections import Counter

genres = df['listed_in'].dropna().apply(lambda x: x.split(', '))
genre_list = [g for sublist in genres for g in sublist]
genre_counts = pd.Series(genre_list).value_counts().head(10)

plt.figure(figsize=(8,5))
genre_counts.plot(kind='barh', color='red')
plt.title('Top 10 Genres on Netflix')
plt.xlabel('Count')
plt.ylabel('Genre')
plt.show()


# In[70]:


top_directors = df[df['director'] != 'Not Available']['director'].value_counts().head(10)

plt.figure(figsize=(8,5))
sns.barplot(x=top_directors.values, y=top_directors.index, palette='cool')
plt.title('Top 10 Directors on Netflix')
plt.xlabel('Number of Titles')
plt.ylabel('Director')
plt.show()


# In[71]:


print("Insights:")
print("• Netflix has more Movies than TV Shows. ")
print("• Netflix has consistently added more Movies than TV Shows every year.")
print("• The USA and India dominate content production.")
print("• The number of titles increased rapidly after 2015.")
print("• Most shows are rated TV-MA or TV-14.")
print("• Top genres include Dramas, Comedies, and International content.")
print("• The list of top 10 directors is also shown")


# In[ ]:




