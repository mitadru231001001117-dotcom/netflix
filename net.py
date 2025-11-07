import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

sns.set(style="whitegrid")

# ---------------------------
# Streamlit Page Config
# ---------------------------
st.set_page_config(
    page_title="Netflix EDA Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.title("📊 Netflix EDA Dashboard")
st.markdown("""
Explore Netflix dataset with visualizations and see the Python code for each.
""")

# ---------------------------
# Sidebar Navigation
# ---------------------------
st.sidebar.title("Navigation")
options = [
    "Dataset Preview", "Data Cleaning", "Missing Data Heatmap",
    "Movies vs TV Shows", "Titles Added Per Year",
    "Top 10 Genres", "Top 10 Countries", 
    "Ratings Distribution",
    "Movie Duration Distribution", "TV Show Season Counts",
    "Top 10 Actors", "Top 10 Directors", "Correlation Heatmap",
    "Global Distribution (Map)"
]
choice = st.sidebar.radio("Select Visualization", options)


# ---------------------------
# Load Dataset
# ---------------------------
df = pd.read_csv("netflix_titles_nov_2019.csv")

# ---------------------------
# Data Cleaning
# ---------------------------
df['cast'] = df['cast'].fillna('Unknown')
df['director'] = df['director'].fillna('Unknown')
df['country'] = df['country'].fillna('Unknown')
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year
df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
df['duration_num'] = df['duration'].str.extract(r'(\d+)').astype(float)

# ---------------------------
# Helper function to show matplotlib plots with code
# ---------------------------
def show_plot(fig_code, fig):
    st.pyplot(fig)
    with st.expander("Show Python Code"):
        st.code(fig_code, language='python')

# ---------------------------
# 1. Dataset Preview
# ---------------------------
if choice == "Dataset Preview":
    st.dataframe(df.head())

# ---------------------------
# 2. Data Cleaning Info
# ---------------------------
elif choice == "Data Cleaning":
    st.write("**Data Cleaning Applied:**")
    st.markdown("""
    - Fill missing `cast`, `director`, `country` with 'Unknown'  
    - Convert `date_added` to datetime  
    - Extract `year_added` from `date_added`  
    - Convert `release_year` to numeric  
    - Extract numeric duration from `duration` column
    """)

# ---------------------------
# 3. Missing Data Heatmap
# ---------------------------
elif choice == "Missing Data Heatmap":
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(df.isnull(), cbar=False, yticklabels=False, cmap='coolwarm', ax=ax)
    fig_code = """
plt.figure(figsize=(10, 5))
sns.heatmap(df.isnull(), cbar=False, yticklabels=False, cmap='coolwarm')
plt.title("Missing Data Heatmap")
plt.show()
"""
    show_plot(fig_code, fig)

# ---------------------------
# 4. Movies vs TV Shows
# ---------------------------
elif choice == "Movies vs TV Shows":
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(x='type', data=df, hue='type', palette='Set2', ax=ax)
    if ax.get_legend() is not None:
        ax.get_legend().remove()
    fig_code = """
plt.figure(figsize=(6, 4))
sns.countplot(x='type', data=df, hue='type', palette='Set2', legend=False)
plt.title("Movies vs TV Shows on Netflix")
plt.show()
"""
    show_plot(fig_code, fig)

# ---------------------------
# 5. Titles Added per Year
# ---------------------------
elif choice == "Titles Added Per Year":
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.countplot(x='year_added', data=df, order=sorted(df['year_added'].dropna().unique()), ax=ax)
    ax.set_xlabel("Year Added")
    ax.set_ylabel("Number of Titles")
    fig_code = """
plt.figure(figsize=(10, 5))
sns.countplot(x='year_added', data=df, order=sorted(df['year_added'].dropna().unique()))
plt.title("Titles Added Per Year")
plt.xlabel("Year Added")
plt.ylabel("Number of Titles")
plt.show()
"""
    show_plot(fig_code, fig)

# ---------------------------
# 6. Top 10 Genres
# ---------------------------
elif choice == "Top 10 Genres":
    genres = df['listed_in'].dropna().str.split(',').explode().str.strip().value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=genres.values, y=genres.index, palette='magma', ax=ax)
    ax.set_xlabel("Number of Titles")
    fig_code = """
genres = df['listed_in'].dropna().str.split(',').explode().str.strip().value_counts().head(10)
plt.figure(figsize=(10, 5))
sns.barplot(x=genres.values, y=genres.index, palette='magma')
plt.title("Top 10 Genres on Netflix")
plt.xlabel("Number of Titles")
plt.show()
"""
    show_plot(fig_code, fig)

# ---------------------------
# 7. Top 10 Countries
# ---------------------------
elif choice == "Top 10 Countries":
    countries = df['country'].dropna().str.split(',').explode().str.strip().value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=countries.values, y=countries.index, palette='crest', ax=ax)
    ax.set_xlabel("Number of Titles")
    fig_code = """
countries = df['country'].dropna().str.split(',').explode().str.strip().value_counts().head(10)
plt.figure(figsize=(10, 5))
sns.barplot(x=countries.values, y=countries.index, palette='crest')
plt.title("Top 10 Countries on Netflix")
plt.xlabel("Number of Titles")
plt.show()
"""
    show_plot(fig_code, fig)

# ---------------------------
# 8. Ratings Distribution
# ---------------------------
elif choice == "Ratings Distribution":
    ratings = df['rating'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=ratings.values, y=ratings.index, palette='viridis', ax=ax)
    ax.set_xlabel("Number of Titles")
    fig_code = """
ratings = df['rating'].value_counts().head(10)
plt.figure(figsize=(10, 5))
sns.barplot(x=ratings.values, y=ratings.index, palette='viridis')
plt.title("Ratings Distribution on Netflix")
plt.xlabel("Number of Titles")
plt.show()
"""
    show_plot(fig_code, fig)

# ---------------------------
# 9. Movie Duration Distribution
# ---------------------------
elif choice == "Movie Duration Distribution":
    movie_durations = df[df['type'] == 'Movie']['duration_num'].dropna()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(movie_durations, bins=30, kde=True, color='red', ax=ax)
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Count")
    fig_code = """
plt.figure(figsize=(8, 5))
movie_durations = df[df['type'] == 'Movie']['duration_num'].dropna()
sns.histplot(movie_durations, bins=30, kde=True, color='red')
plt.title("Distribution of Movie Durations (Minutes)")
plt.xlabel("Duration (minutes)")
plt.ylabel("Count")
plt.show()
"""
    show_plot(fig_code, fig)

# ---------------------------
# 10. TV Show Season Counts
# ---------------------------
elif choice == "TV Show Season Counts":
    tv_seasons = df[df['type'] == 'TV Show']['duration_num'].dropna()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(x=tv_seasons, ax=ax)
    ax.set_xlabel("Seasons")
    ax.set_ylabel("Count")
    fig_code = """
tv_seasons = df[df['type'] == 'TV Show']['duration_num'].dropna()
plt.figure(figsize=(8, 5))
sns.countplot(x=tv_seasons)
plt.title("Number of Seasons in TV Shows")
plt.xlabel("Seasons")
plt.ylabel("Count")
plt.show()
"""
    show_plot(fig_code, fig)

# ---------------------------
# 11. Top 10 Actors
# ---------------------------
elif choice == "Top 10 Actors":
    actors = df['cast'].dropna().str.split(',').explode().str.strip().value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=actors.values, y=actors.index, palette='rocket', ax=ax)
    ax.set_xlabel("Number of Appearances")
    fig_code = """
actors = df['cast'].dropna().str.split(',').explode().str.strip().value_counts().head(10)
plt.figure(figsize=(10, 5))
sns.barplot(x=actors.values, y=actors.index, palette='rocket')
plt.title("Top 10 Actors on Netflix")
plt.xlabel("Number of Appearances")
plt.show()
"""
    show_plot(fig_code, fig)

# ---------------------------
# 12. Top 10 Directors
# ---------------------------
elif choice == "Top 10 Directors":
    directors = df['director'].dropna().str.split(',').explode().str.strip().value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=directors.values, y=directors.index, palette='flare', ax=ax)
    ax.set_xlabel("Number of Titles Directed")
    fig_code = """
directors = df['director'].dropna().str.split(',').explode().str.strip().value_counts().head(10)
plt.figure(figsize=(10, 5))
sns.barplot(x=directors.values, y=directors.index, palette='flare')
plt.title("Top 10 Directors on Netflix")
plt.xlabel("Number of Titles Directed")
plt.show()
"""
    show_plot(fig_code, fig)

# ---------------------------
# 13. Correlation Heatmap
# ---------------------------
elif choice == "Correlation Heatmap":
    fig, ax = plt.subplots(figsize=(6, 4))
    corr = df[['release_year', 'year_added', 'duration_num']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    fig_code = """
plt.figure(figsize=(6, 4))
corr = df[['release_year', 'year_added', 'duration_num']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.show()
"""
    show_plot(fig_code, fig)

# ---------------------------
# 14. Global Distribution Map
# ---------------------------
elif choice == "Global Distribution (Map)":
    country_df = df.copy()
    country_df['country'] = country_df['country'].str.split(',').str[0].str.strip()
    country_count = country_df.groupby(['country', 'type']).size().reset_index(name='count')
    country_count = country_count[country_count['country'] != 'Unknown']

    fig = px.choropleth(
        country_count,
        locations='country',
        locationmode='country names',
        color='count',
        hover_name='country',
        animation_frame='type',
        color_continuous_scale='Reds',
        title='Global Distribution of Movies and TV Shows on Netflix'
    )
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig)

    fig_code = """
country_df = df.copy()
country_df['country'] = country_df['country'].str.split(',').str[0].str.strip()
country_count = country_df.groupby(['country', 'type']).size().reset_index(name='count')
country_count = country_count[country_count['country'] != 'Unknown']

fig = px.choropleth(
    country_count,
    locations='country',
    locationmode='country names',
    color='count',
    hover_name='country',
    animation_frame='type',
    color_continuous_scale='Reds',
    title='Global Distribution of Movies and TV Shows on Netflix'
)
fig.update_layout(title_x=0.5)
fig.show()
"""
    st.expander("Show Python Code").code(fig_code, language='python')

