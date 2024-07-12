import unittest
from src.app import app

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def test_get_main(self):
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), '<h1>Home</h1>')

    def test_get_authors(self):
        response = self.client.get('/author')
        
        self.assertEqual(response.status_code, 200)
        authors_list = response.get_json()
        self.assertEqual(len(authors_list), 11)
        
        self.assertEqual(authors_list[0]['id'], 1)
        self.assertEqual(authors_list[0]['name'], "JK Rowling")
        self.assertEqual(authors_list[0]['email'], "jkrwling@hotmail.com")
        self.assertEqual(authors_list[0]['age'], 56)
    
    def test_get_genres(self):
        response = self.client.get('/genre')
        
        self.assertEqual(response.status_code, 200)
        genres_list = response.get_json()
        self.assertEqual(len(genres_list), 7)
        
        self.assertEqual(genres_list[2]['id'], 3)
        self.assertEqual(genres_list[2]['name'], "Mystery")
        
        self.assertEqual(genres_list[1]['id'], 2)
        self.assertEqual(genres_list[1]['name'], "Horror")

    def test_get_editorials(self):
        response = self.client.get('/editorial')
        
        self.assertEqual(response.status_code, 200)
        editorials_list = response.get_json()
        self.assertEqual(len(editorials_list), 7)
        
        self.assertEqual(editorials_list[0]['id'], 1)
        self.assertEqual(editorials_list[0]['name'], "dibu")
        self.assertEqual(editorials_list[0]['location'], "GUATEMALA")
        self.assertEqual(editorials_list[0]['phone'], "123231")
        
        self.assertEqual(editorials_list[1]['id'], 2)
        self.assertEqual(editorials_list[1]['name'], "HarperCollins")
        self.assertEqual(editorials_list[1]['location'], "New York")
        self.assertEqual(editorials_list[1]['phone'], "212-555-5678")

if __name__ == '__main__':
    unittest.main()
