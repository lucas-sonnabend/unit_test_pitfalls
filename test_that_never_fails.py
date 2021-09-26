import requests
import json

import requests_mock

URL = "https://swapi-graphql.netlify.app/.netlify/functions/index"
QUERY='''
query getFilm($id: ID) {
  film(id: $id) {
    title
    id
    episodeID
    releaseDate
  }
}
'''

def get_film(id: str):
    data = {"query": QUERY, "variables": json.dumps({"id": id})}
    response = requests.post(URL, data=data)
    return response.json()["data"]["film"]
    

def test_get_film_returns_successfully():
    example_response = {
        "data": {
            "film": {
            "title": "a New Test",
            "id": "testId",
            "episodeID": 4
            }
        }
    }
    with requests_mock.Mocker() as m:
        m.post(URL, json=example_response)
        result = get_film("foo")
        assert result == {
            "title": "a New Test",
            "id": "testId",
            "episodeID": 4
        }

# print(get_film("ZmlsbXM6MQ=="))