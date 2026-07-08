import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------
# Page Configuration
# ---------------------------------
st.set_page_config(
    page_title="MovieLens Analytics Dashboard",
    page_icon="🎬",
    layout="wide"
)

# ---------------------------------
# Load Data
# ---------------------------------
movies = pd.read_csv("ml-latest-small/movies.csv")
ratings = pd.read_csv("ml-latest-small/ratings.csv")

# ---------------------------------
# Sidebar
# ---------------------------------
st.sidebar.title("🎬 MovieLens Dashboard")

st.sidebar.success("Data Analytics Capstone Project")

st.sidebar.markdown("---")

st.sidebar.markdown("""
### 👨‍💻 Developer
**Confidence Kwao**

### 🛠 Tools
- Python
- Streamlit
- Pandas
- Plotly

### 📂 Dataset
MovieLens Latest Small
""")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Top Movies",
        "Top Rated Movies",
        "Genres",
        "Users",
        "Movie Search",
        "Ratings Distribution",
        "Release Year Analysis",
        "Manager Recommendations"
    ]
)
# ---------------------------------
# Overview Page
# ---------------------------------
if page == "Overview":

    st.title("🎬 MovieLens Analytics Dashboard")

    st.markdown("""
    ### Netflix-Style Movie Analytics

    Analyze movie ratings, user engagement, genre popularity,
    and release trends using the MovieLens Latest Small dataset.
    """)

    st.divider()

    # KPIs
    total_movies = len(movies)
    total_ratings = len(ratings)
    total_users = ratings["userId"].nunique()
    average_rating = ratings["rating"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🎥 Movies", f"{total_movies:,}")
    col2.metric("⭐ Ratings", f"{total_ratings:,}")
    col3.metric("👥 Users", f"{total_users:,}")
    col4.metric("🌟 Average Rating", f"{average_rating:.2f}")

    st.divider()

    st.subheader("⭐ Ratings Distribution")

    fig = px.histogram(
        ratings,
        x="rating",
        nbins=10,
        title="Distribution of Ratings"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("🎬 Movies Dataset")
        st.dataframe(movies.head(10), use_container_width=True)

    with right:
        st.subheader("⭐ Ratings Dataset")
        st.dataframe(ratings.head(10), use_container_width=True)

    st.divider()

    st.subheader("💡 Project Objective")

    st.info("""
This dashboard helps analyze:

- Movie ratings
- User engagement
- Genre popularity
- Release trends

The insights can help streaming platforms improve recommendations and understand audience preferences.
""")
    # ---------------------------------
# Top Movies Page
# ---------------------------------
elif page == "Top Movies":

    st.title("⭐ Top Movies by Average Rating")

    movie_stats = (
        ratings.groupby("movieId")
        .agg(
            Average_Rating=("rating", "mean"),
            Number_of_Ratings=("rating", "count")
        )
        .reset_index()
    )

    movie_stats = movie_stats.merge(
        movies,
        on="movieId"
    )

    minimum_votes = st.slider(
        "Minimum Number of Ratings",
        min_value=1,
        max_value=200,
        value=20
    )

    filtered = movie_stats[
        movie_stats["Number_of_Ratings"] >= minimum_votes
    ]

    filtered = filtered.sort_values(
        "Average_Rating",
        ascending=False
    )

    st.dataframe(
        filtered[
            ["title", "Average_Rating", "Number_of_Ratings"]
        ].head(20),
        use_container_width=True
    )


# ---------------------------------
# Top Rated Movies Page
# ---------------------------------
elif page == "Top Rated Movies":

    st.title("🏆 Top 10 Most Rated Movies")

    movie_stats = (
        ratings.groupby("movieId")
        .agg(
            Average_Rating=("rating", "mean"),
            Number_of_Ratings=("rating", "count")
        )
        .reset_index()
    )

    movie_stats = movie_stats.merge(
        movies,
        on="movieId"
    )

    most_rated = movie_stats.sort_values(
        "Number_of_Ratings",
        ascending=False
    ).head(10)

    fig = px.bar(
        most_rated,
        x="Number_of_Ratings",
        y="title",
        orientation="h",
        title="Top 10 Most Rated Movies"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        most_rated[
            ["title", "Average_Rating", "Number_of_Ratings"]
        ],
        use_container_width=True
    )

    csv = most_rated.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Top Rated Movies",
        data=csv,
        file_name="top_rated_movies.csv",
        mime="text/csv"
    )
    # ---------------------------------
# Genres Page
# ---------------------------------
elif page == "Genres":

    st.title("🎭 Genre Analysis")

    genre_counts = (
        movies["genres"]
        .str.split("|")
        .explode()
        .value_counts()
        .reset_index()
    )

    genre_counts.columns = ["Genre", "Movies"]

    fig = px.bar(
        genre_counts,
        x="Genre",
        y="Movies",
        title="Number of Movies by Genre"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    selected_genre = st.selectbox(
        "Select a Genre",
        sorted(genre_counts["Genre"])
    )

    filtered_movies = movies[
        movies["genres"].str.contains(
            selected_genre,
            case=False,
            na=False
        )
    ]

    st.write(f"Movies found: **{len(filtered_movies)}**")

    st.dataframe(
        filtered_movies[["title", "genres"]],
        use_container_width=True
    )


# ---------------------------------
# Users Page
# ---------------------------------
elif page == "Users":

    st.title("👥 User Analytics")

    active_users = (
        ratings["userId"]
        .value_counts()
        .head(20)
        .reset_index()
    )

    active_users.columns = ["User ID", "Ratings Given"]

    fig = px.bar(
        active_users,
        x="User ID",
        y="Ratings Given",
        title="Top 20 Most Active Users"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(active_users, use_container_width=True)


# ---------------------------------
# Movie Search
# ---------------------------------
elif page == "Movie Search":

    st.title("🔍 Movie Search")

    search = st.text_input("Search by movie title")

    if search:

        results = movies[
            movies["title"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

        st.success(f"{len(results)} movie(s) found.")

        st.dataframe(
            results,
            use_container_width=True
        )

        csv = results.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Download Search Results",
            csv,
            "movie_search.csv",
            "text/csv"
        )
        # ---------------------------------
# Ratings Distribution
# ---------------------------------
elif page == "Ratings Distribution":

    st.title("⭐ Ratings Distribution")

    fig = px.histogram(
        ratings,
        x="rating",
        nbins=10,
        title="Distribution of Movie Ratings"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.write("This chart shows how users rate movies across the MovieLens dataset.")


# ---------------------------------
# Release Year Analysis
# ---------------------------------
elif page == "Release Year Analysis":

    st.title("📅 Release Year Analysis")

    movies_year = movies.copy()

    movies_year["Year"] = movies_year["title"].str.extract(r"\((\d{4})\)")

    movies_year = movies_year.dropna(subset=["Year"])

    movies_year["Year"] = movies_year["Year"].astype(int)

    yearly_movies = (
        movies_year.groupby("Year")
        .size()
        .reset_index(name="Movies Released")
    )

    fig = px.line(
        yearly_movies,
        x="Year",
        y="Movies Released",
        markers=True,
        title="Movies Released by Year"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(yearly_movies, use_container_width=True)


# ---------------------------------
# Manager Recommendations
# ---------------------------------
elif page == "Manager Recommendations":

    st.title("💼 Manager Recommendations")

    st.success("""
### Recommendation 1
Promote movies with both high ratings and a large number of user ratings.
These titles have demonstrated strong audience engagement and satisfaction.
""")

    st.info("""
### Recommendation 2
Drama, Comedy, and Action are among the most represented genres.
These genres should continue to be prioritized when acquiring content.
""")

    st.warning("""
### Recommendation 3
Movies with very few ratings should be recommended more often to users.
Increasing their visibility can improve catalog discovery.
""")

    st.error("""
### Recommendation 4
Monitor user rating activity regularly to identify changing viewer preferences.
""")

    st.divider()

    st.subheader("Executive Summary")

    st.write("""
The MovieLens dashboard provides valuable insights into movie popularity,
user engagement, genre distribution, and release trends.

These insights can help streaming services improve recommendation systems,
content acquisition strategies, and user engagement.
""")
    st.markdown("---")

st.caption(
    "🎬 MovieLens Analytics Dashboard | Built with Streamlit, Pandas & Plotly | Data Analytics Capstone Project"
)