# Movie Recommendation System

This project is a Django-based movie recommendation system that leverages data scraping, database management, vectorization, similarity calculation, and recommendation generation to deliver personalized movie suggestions. The system is designed to enhance user experience by providing tailored movie recommendations based on individual preferences.

## Features

- **Data Collection**: Uses TMDB's API to collect comprehensive movie data, including titles, genres, descriptions, posters, release dates, and popularity scores.
- **Database Management**: Organizes the collected data into a structured database for efficient storage and retrieval.
- **Text Preprocessing**: Cleans and standardizes movie descriptions by removing HTML tags, punctuation, special characters, and stopwords, followed by tokenization and normalization.
- **Vectorization**: Converts textual descriptions into numerical vectors using TF-IDF (Term Frequency-Inverse Document Frequency), capturing the essence of each movie's content.
- **Similarity Calculation**: Computes cosine similarity between movies to measure how closely related they are based on content.
- **Recommendation Generation**: Provides personalized movie recommendations based on user input, such as preferences, input movie, or browsing history.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/movie-recommendation-system.git
   cd movie-recommendation-system
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: `env\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up TMDB API Key**
   - Sign up for a TMDB API key from [TMDB](https://www.themoviedb.org/).
   - Create a `.env` file in the project root and add your API key:
     ```
     TMDB_API_KEY=your_tmdb_api_key
     ```

5. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   - Open your web browser and navigate to `http://localhost:8000`.
  
## Results

![Picture1](https://github.com/user-attachments/assets/707484eb-6fbd-4960-8567-95ea40f64aba)

![Picture2](https://github.com/user-attachments/assets/a6b8b691-4fcf-4623-b741-75ced7c2d7c5)

![Picture3](https://github.com/user-attachments/assets/46d8aced-de01-4bb7-baeb-b909051d01c8)

![Picture4](https://github.com/user-attachments/assets/c1de9acb-62ca-4c77-a2e5-72627cb589c1)

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your proposed changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact Nirakar Jena at [Gmail](mailto:jenashubham60@gmail.com).
