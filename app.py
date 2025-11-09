import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Streamlit page config
st.set_page_config(page_title="Netflix EDA Dashboard", layout="wide")
sns.set(style='whitegrid')

# Title
st.title("📊 Netflix Movies & TV Shows EDA Dashboard")

# Load dataset
df = pd.read_csv("netflix_titles.csv")

# Fill missing values
df['director'].fillna('Not Available', inplace=True)
df['cast'].fillna('Not Available', inplace=True)
df['country'].fillna('Unknown', inplace=True)
df['rating'].fillna('Not Rated', inplace=True)
df['date_added'].fillna('Unknown', inplace=True)

# Sidebar filters
st.sidebar.header("Filters")
content_type = st.sidebar.multiselect("Select Content Type", options=df['type'].unique(), default=df['type'].unique())
year_range = st.sidebar.slider("Select Year Range", 2000, 2025, (2000, 2025))

# Apply filters
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year
filtered_df = df[df['type'].isin(content_type) & df['year_added'].between(year_range[0], year_range[1])]

# Show raw data
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df.head(50))

# Movies vs TV Shows
st.subheader("Movies vs TV Shows")
fig, ax = plt.subplots(figsize=(6,4))
sns.countplot(x='type', data=filtered_df, ax=ax)
ax.set_xlabel("Type of Content")
ax.set_ylabel("Count")
st.pyplot(fig)

# Movies vs TV Shows Added Each Year
st.subheader("Movies vs TV Shows Added Each Year")
type_year = filtered_df.groupby(['year_added', 'type']).size().unstack().fillna(0)
fig, ax = plt.subplots(figsize=(12,6))
type_year.plot(kind='bar', stacked=False, color=['#FF6F61', '#6B5B95'], ax=ax)
ax.set_xlabel("Year Added")
ax.set_ylabel("Number of Titles")
plt.xticks(rotation=45)
st.pyplot(fig)

# Top 10 Countries
st.subheader("Top 10 Countries Producing Content")
top_countries = filtered_df['country'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(10,5))
top_countries.plot(kind='bar', color='orange', ax=ax)
ax.set_xlabel("Country")
ax.set_ylabel("Number of Titles")
st.pyplot(fig)

# Trend of content added over years
st.subheader("Content Added Trend Over the Years")
content_trend = filtered_df['year_added'].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(content_trend.index, content_trend.values, marker='o', color='purple')
ax.set_xlabel("Year Added")
ax.set_ylabel("Number of Titles Added")
ax.grid(True)
st.pyplot(fig)

# Ratings Distribution
st.subheader("Ratings Distribution")
fig, ax = plt.subplots(figsize=(8,5))
sns.countplot(y='rating', data=filtered_df, order=filtered_df['rating'].value_counts().index, ax=ax)
st.pyplot(fig)

# Top Ratings Pie Chart
st.subheader("Top Ratings Distribution")
ratings = filtered_df['rating'].value_counts().head(8)
fig, ax = plt.subplots(figsize=(7,7))
ax.pie(ratings, labels=ratings.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
st.pyplot(fig)

# Top 10 Genres
st.subheader("Top 10 Genres")
genres = filtered_df['listed_in'].dropna().apply(lambda x: x.split(', '))
genre_list = [g for sublist in genres for g in sublist]
genre_counts = pd.Series(genre_list).value_counts().head(10)
fig, ax = plt.subplots(figsize=(8,5))
genre_counts.plot(kind='barh', color='red', ax=ax)
st.pyplot(fig)

# Top 10 Directors
st.subheader("Top 10 Directors")
top_directors = filtered_df[filtered_df['director'] != 'Not Available']['director'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(x=top_directors.values, y=top_directors.index, palette='cool', ax=ax)
st.pyplot(fig)

# Insights
st.subheader("Key Insights")
st.markdown("""
- Netflix has more Movies than TV Shows.  
- Netflix consistently adds more Movies than TV Shows every year.  
- The USA and India dominate content production.  
- Number of titles increased rapidly after 2015.  
- Most shows are rated TV-MA or TV-14.  
- Top genres include Dramas, Comedies, and International content.  
- Top 10 directors are also highlighted.
""")
