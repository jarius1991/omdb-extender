from unittest.mock import Mock, patch

from django.test import SimpleTestCase, TestCase

from core import omdb


class TestOmdbApi(SimpleTestCase):
    def setUp(self):
        self.api = omdb.Omdb_API()
        self.api.OMDB_API_KEY = 'test_api_key'

    def test_page_number(self):
        """Test that _page_count return proper number of pages of query"""
        response_1 = {'totalResults': 111}
        page_count_1 = 12
        response_2 = {'totalResults': 200}
        page_count_2 = 20

        self.assertEqual(self.api._page_count(response_1), page_count_1)
        self.assertEqual(self.api._page_count(response_2), page_count_2)

    @patch('core.omdb.request')
    def test_run_query(self, request_mock):
        """Test that _run_query use proper url for provided params and return expected data"""
        import json
        from .example_response_body import body
        params = {'apikey': 'test_api_key',
                  'param_1': 3}
        url = "http://www.omdbapi.com/?apikey=test_api_key&param_1=3"
        request_mock.urlopen.return_value.read.return_value = body

        response = self.api._run_query(params)

        self.assertEqual(response, json.loads(body))
        request_mock.urlopen.assert_called_once_with(url)

    @patch('core.omdb.request')
    def test_get_movies_list_one_page(self, request_mock):
        """Check if get movies list return full list of movies"""
        first_page = ['a'] * 3
        read_mock = Mock(side_effect=(b'{"Search":["a","a","a"],"totalResults":"3"}',))
        request_mock.urlopen.return_value.read = read_mock

        movies_list = self.api._get_movies_list('test_title')

        self.assertEqual(movies_list, first_page)

    @patch('core.omdb.request')
    def test_get_movies_list_few_pages(self, request_mock):
        """Check if get movies list return full list of movies"""
        first_page = ['a'] * 10
        second_page = ['b'] * 2
        read_mock = Mock(side_effect=(b'{"Search":["a","a","a","a","a","a","a","a","a","a"],"totalResults":"12"}',
                                      b'{"Search":["b","b"],"totalResults":"12"}'))
        request_mock.urlopen.return_value.read = read_mock

        movies_list = self.api._get_movies_list('test_title')

        self.assertEqual(movies_list, first_page + second_page)

    def test_filter_movies_by_genre(self):
        movies_list = [{'Genre': ['Comedy', 'Horror'], "Title": "Bird"},
                       {'Genre': ['Thriller'], "Title": "Snake"},
                       {'Genre': ['Comedy'], "Title": "Cat"}]
        expected_filtered_list_1 = [{'Genre': ['Comedy', 'Horror'], "Title": "Bird"},
                                    {'Genre': ['Comedy'], "Title": "Cat"}]
        expected_filtered_list_2 = []

        filtered_list_1 = self.api._filter_movies_by_genre(movies_list, 'Comedy')
        filtered_list_2 = self.api._filter_movies_by_genre(movies_list, 'Biography')

        self.assertEqual(filtered_list_1, expected_filtered_list_1)
        self.assertEqual(filtered_list_2, expected_filtered_list_2)

    def test_add_genre_to_movies(self):
        movies = [{'Title': 'Title1', 'imdbID': 'Id1'},
                  {'Title': 'Title2', 'imdbID': 'Id2'}]
        genres_for_movies = {'Id1': ['Comedy', 'Musical'],
                             'Id2': ['Horror']}
        with patch.object(self.api, '_get_movie_genre') as mock_get:
            mock_get.side_effect = lambda movie_id: genres_for_movies[movie_id]

            self.api._add_genre_data_to_movies(movies)

        self.assertEqual(movies[0]['Genre'], ['Comedy', 'Musical'])
        self.assertEqual(movies[1]['Genre'], ['Horror'])

    def test_get_movie_genre(self):
        with patch.object(self.api, '_run_query') as mock_query:
            mock_query.return_value = {'Genre': 'Comedy, Horror'}
            genres_1 = self.api._get_movie_genre('1')
            mock_query.assert_called_with({'i': '1', 'apikey': 'test_api_key'})
            self.assertEqual(genres_1, ['Comedy', 'Horror'])

            mock_query.return_value = {'Genre': 'Music'}
            genres_2 = self.api._get_movie_genre('2')
            mock_query.assert_called_with({'i': '2', 'apikey': 'test_api_key'})
            self.assertEqual(genres_2, ['Music'])

    @patch('core.omdb.request.urlopen')
    def test_search_movies_without_genre(self, mock_urlopen):
        from .example_response_body import query_response_pairs, search_without_genre, search_with_genre_drama
        # Set what read() should return, it depend on url value passed to urlopen method
        mock_urlopen.side_effect = lambda url: Mock(**{'read.return_value': query_response_pairs[url]})

        movies_1 = self.api.search_movies('test_title')
        self.assertEqual(movies_1, search_without_genre)

        movies_2 = self.api.search_movies('test_title', genre='Drama')
        self.assertEqual(movies_2, search_with_genre_drama)
