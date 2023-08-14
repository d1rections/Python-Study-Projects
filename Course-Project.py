import requests_with_caching
import json

def get_movies_from_tastedive(inp_str):
    baseurl = 'https://tastedive.com/api/similar'
    params_diction = {}
    params_diction['q'] = inp_str
    params_diction['type'] = 'movies'
    params_diction['limit'] = 5
    tastedive_resp = requests_with_caching.get(baseurl, params = params_diction)
    json_result = tastedive_resp.json()
    return json_result


def extract_movie_titles(result):
    movie_titles = []
    movie_info_lst = result['Similar']['Results']
    for word in movie_info_lst:
        movie_titles.append(word['Name'])
    return movie_titles


def get_related_titles(lst_of_movies):
    sequence_of_movies = []
    for a_movie in lst_of_movies:
        json_loop_result = get_movies_from_tastedive(a_movie)
        movie_loop_titles = extract_movie_titles(json_loop_result)
        for title in movie_loop_titles:
            if title not in sequence_of_movies:
                sequence_of_movies.append(title)
    return sequence_of_movies


def get_movie_data(desired_movie):
    baseurl = 'http://www.omdbapi.com/'
    params_diction2 = {}
    params_diction2['t'] = desired_movie
    params_diction2['r'] = 'json'
    omdb_resp = requests_with_caching.get(baseurl, params = params_diction2)
    json_omdb_result = omdb_resp.json()
    return json_omdb_result


def get_movie_rating(json_omdb_result):
    rating = 0
    rating_info = json_omdb_result['Ratings']
    for d in rating_info:
        if d['Source'] == 'Rotten Tomatoes':
            rating = d['Value']
    string_rating = str(rating)
    normal_rating = string_rating.strip('%')
    return int(normal_rating)


def get_sorted_recommendations(lst_of_movie_titles):
    related_titles = get_related_titles(lst_of_movie_titles)
    rating_dict = {}
    for title in related_titles:
        title_rating = get_movie_rating(get_movie_data(title))
        rating_dict[title] = title_rating
    return [movie_name[0] for movie_name in
        sorted(rating_dict.items(), key=lambda item: (item[1], item[0]), reverse=True)]
