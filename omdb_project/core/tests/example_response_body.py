body = b'{"Search":[{"Title":"A Bird of the Air","Year":"2011","imdbID":"tt0448022","Type":"movie","Poster":"https://m.media-amazon.com/images/M/MV5BMTMzODYwMzYzNl5BMl5BanBnXkFtZTcwNjc4OTg2Nw@@._V1_SX300.jpg"},{"Title":"Pretty Bird","Year":"2008","imdbID":"tt1058743","Type":"movie","Poster":"https://m.media-amazon.com/images/M/MV5BMzkyODYzMDA2MV5BMl5BanBnXkFtZTgwMTA2NjcwMzE@._V1_SX300.jpg"},{"Title":"The Early Bird","Year":"1965","imdbID":"tt0059143","Type":"movie","Poster":"https://m.media-amazon.com/images/M/MV5BODU0YWFkNGYtMWViNy00Njc1LTg1NWItODA0NDFlZDBjMmE4XkEyXkFqcGdeQXVyMjIyNjE2NA@@._V1_SX300.jpg"},{"Title":"Man Is Not a Bird","Year":"1965","imdbID":"tt0059063","Type":"movie","Poster":"https://m.media-amazon.com/images/M/MV5BZGVlMDNiN2UtOWEzNC00NmE0LWE4ZTktNGU4M2IwYjcwZmEyXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg"},{"Title":"The Blue Bird","Year":"1976","imdbID":"tt0074225","Type":"movie","Poster":"https://m.media-amazon.com/images/M/MV5BOTU0MDM3NDk0NV5BMl5BanBnXkFtZTcwNTI0MTQyMQ@@._V1_SX300.jpg"},{"Title":"Bird of Paradise","Year":"1932","imdbID":"tt0022689","Type":"movie","Poster":"https://m.media-amazon.com/images/M/MV5BMTAzOTg4NDUyNDdeQTJeQWpwZ15BbWU4MDc5NDk3NjIx._V1_SX300.jpg"},{"Title":"Flu Bird Horror","Year":"2008","imdbID":"tt1282045","Type":"movie","Poster":"https://m.media-amazon.com/images/M/MV5BMTkzNTYxNjY5N15BMl5BanBnXkFtZTcwODQ1NTY5MQ@@._V1_SX300.jpg"},{"Title":"Fatal Contact: Bird Flu in America","Year":"2006","imdbID":"tt0800026","Type":"movie","Poster":"https://m.media-amazon.com/images/M/MV5BMTU1MTM0OTQ1NV5BMl5BanBnXkFtZTcwNzUyMDczMQ@@._V1_SX300.jpg"},{"Title":"Liz and the Blue Bird","Year":"2018","imdbID":"tt7089878","Type":"movie","Poster":"https://m.media-amazon.com/images/M/MV5BOTBjMjIyNmYtZGZiZi00ZGMzLTliZWUtYzU1MGM4OTFkZGMxXkEyXkFqcGdeQXVyMTk2MDc1MjQ@._V1_SX300.jpg"},{"Title":"The Painted Bird","Year":"2019","imdbID":"tt1667354","Type":"movie","Poster":"https://m.media-amazon.com/images/M/MV5BYjQ5YTkxNzEtZGM0Zi00YmNlLTljM2QtMjNmMmM1YzdjZWYzXkEyXkFqcGdeQXVyMjg2NTQ2NQ@@._V1_SX300.jpg"}],"totalResults":"716","Response":"True"}'

query_response_pairs = {
    'http://www.omdbapi.com/?s=test_title&apikey=test_api_key': b'{"Search":[{"Title":"Banana Boy","Year":"2003","imdbID":"tt0431644","Type":"movie","Poster":"N/A"},{"Title":"Banana Boy","Year":"2016","imdbID":"tt5252614","Type":"movie","Poster":"https://m.media-amazon.com/images/M/MV5BMTkwMzU0MDE1OF5BMl5BanBnXkFtZTgwMjU3NTU1NzE@._V1_SX300.jpg"}],"totalResults":"2","Response":"True"}',
    'http://www.omdbapi.com/?i=tt0431644&apikey=test_api_key': b'{"Title":"Banana Boy","Year":"2003","Rated":"N/A","Released":"17 Oct 2004","Runtime":"7 min","Genre":"Short","Director":"Samuel Chow","Writer":"N/A","Actors":"N/A","Plot":"A young gay asian canadian man reflects on the issues surrounding his ethnicity and his gender preference","Language":"English","Country":"Canada","Awards":"N/A","Poster":"N/A","Ratings":[],"Metascore":"N/A","imdbRating":"N/A","imdbVotes":"N/A","imdbID":"tt0431644","Type":"movie","DVD":"N/A","BoxOffice":"N/A","Production":"N/A","Website":"N/A","Response":"True"}',
    'http://www.omdbapi.com/?i=tt5252614&apikey=test_api_key': b'{"Title":"Banana Boy","Year":"2016","Rated":"N/A","Released":"01 Jan 2016","Runtime":"22 min","Genre":"Short, Drama","Director":"Steven Woodburn","Writer":"Steven Woodburn","Actors":"William Oakley, Steve Le Marquand, Eddie Baroo, Maya Stange","Plot":"N/A","Language":"English","Country":"Australia","Awards":"N/A","Poster":"https://m.media-amazon.com/images/M/MV5BMTkwMzU0MDE1OF5BMl5BanBnXkFtZTgwMjU3NTU1NzE@._V1_SX300.jpg","Ratings":[],"Metascore":"N/A","imdbRating":"N/A","imdbVotes":"N/A","imdbID":"tt5252614","Type":"movie","DVD":"N/A","BoxOffice":"N/A","Production":"N/A","Website":"N/A","Response":"True"}',
}

search_without_genre = [{'Title': 'Banana Boy', 'Year': '2003', 'imdbID': 'tt0431644', 'Type': 'movie', 'Poster': 'N/A',
                         'Genre': ['Short']},
                        {'Title': 'Banana Boy', 'Year': '2016', 'imdbID': 'tt5252614', 'Type': 'movie',
                         'Poster': 'https://m.media-amazon.com/images/M/MV5BMTkwMzU0MDE1OF5BMl5BanBnXkFtZTgwMjU3NTU1NzE@._V1_SX300.jpg',
                         'Genre': ['Short', 'Drama']}]

search_with_genre_drama = [{'Title': 'Banana Boy', 'Year': '2016', 'imdbID': 'tt5252614', 'Type': 'movie',
                            'Poster': 'https://m.media-amazon.com/images/M/MV5BMTkwMzU0MDE1OF5BMl5BanBnXkFtZTgwMjU3NTU1NzE@._V1_SX300.jpg',
                            'Genre': ['Short', 'Drama']}]
