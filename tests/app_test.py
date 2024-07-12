import pytest
from src.app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client



def test_get_main(client):
    response = client.get('/')
    
    assert response.status_code == 200
    assert response.data.decode('utf-8') == '<h1>Home</h1>'


def test_get_authors(client):
    response = client.get('/author')
    
    assert response.status_code == 200
    authors_list = response.get_json()
    assert len(authors_list) == 11
    
    assert authors_list[0]['id'] == 1
    assert authors_list[0]['name'] == "JK Rowling"
    assert authors_list[0]['email'] == "jkrwling@hotmail.com"
    assert authors_list[0]['age'] == 56
    
def test_get_genres(client):
    response = client.get('/genre')
    
    assert response.status_code == 200
    genres_list = response.get_json()
    assert len(genres_list) == 7
    
    assert genres_list[2]['id'] == 3
    assert genres_list[2]['name'] == "Mystery"
    
    assert genres_list[1]['id'] == 2
    assert genres_list[1]['name'] == "Horror"

def test_get_editorials(client):
    response = client.get('/editorial')
    
    assert response.status_code == 200
    editorials_list = response.get_json()
    assert len(editorials_list) == 7
    
    assert editorials_list[0]['id'] == 1
    assert editorials_list[0]['name'] == "dibu"
    assert editorials_list[0]['location'] == "GUATEMALA"
    assert editorials_list[0]['phone'] == "123231"
    
    assert editorials_list[1]['id'] == 2
    assert editorials_list[1]['name'] == "HarperCollins"
    assert editorials_list[1]['location'] == "New York"
    assert editorials_list[1]['phone'] == "212-555-5678"
