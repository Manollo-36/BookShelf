import os
import unittest
import json

from sqlalchemy import null
from flaskr import create_app
from models import setup_db, Book


class BookTestCase(unittest.TestCase):    
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        #self.app = create_app()
        #self.client = self.app.test_client
        self.database_name = 'bookshelf_test'
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'Emmanuel', 'Manos', 'localhost:5432', self.database_name
        )
        
        self.app = create_app(self.database_path)
        #Binds the test file to app_context 
        self.cxt = self.app.app_context()
        self.cxt.push()     
           
        self.client = self.app.test_client
        print(f"database_path:{self.database_path}")
        #setup_db(self.app, self.database_path)

        self.new_book = {"title": "Anansi Boys", "author": "Neil Gaiman", "rating": 5}
        self.new_book2 = {"title": "Mobby Dick","author": "Herman Melville","rating":6}

    def tearDown(self):
        """Executed after reach test"""
        pass

    # def test_get_paginated_books(self):
    #     res = self.client().get("/books")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["total_books"])
    #     self.assertTrue(len(data["books"]))

    # def test_404_sent_requesting_beyond_valid_page(self):
    #     res = self.client().get("/books?page=1000", json={"rating": 1})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "resource not found")

    # def test_update_book_rating(self):
    #      res = self.client().patch("/books/5", json={"rating": 1})
    #      print(f'Update_json: {self.client().patch("/books/5", json={"rating": 1})}')
    #      data = json.loads(res.data)
    #      print(f'Update_data:{res.data}')
    #      book = Book.query.filter(Book.id == 5).one_or_none()
    #      print(f'book:{book}')   
    #      self.assertEqual(res.status_code, 200)
    #      self.assertEqual(data["success"], True)
    #      self.assertEqual(book.format()["rating"], 1)

    # def test_400_for_failed_update(self):
    #      res = self.client().patch("/books/5",json={"rating": ''})
    #      #print(f'Update_json_failed: {self.client().patch("/books/0",json={"rating": 1})}')
    #      data = json.loads(res.data)
    #      print(f'Update_data_failed:{res.data}')
    #      self.assertEqual(res.status_code, 400)
    #      self.assertEqual(data["success"], False)
    #      self.assertEqual(data["message"], "bad request")

    def test_create_new_book(self):
        res = self.client().post("/books", json=self.new_book2)
        print(f'JSONData: {self.client().post("/books", json=self.new_book2)}')
        
        data = json.loads(res.data)
        print(f'data:{data}')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["books"]))

    # def test_405_if_book_creation_not_allowed(self):
    #     res = self.client().post("/books/45", json=self.new_book)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 405)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "method not allowed")

    #Delete a different book in each attempt
    # def test_delete_book(self):
    #     res = self.client().delete("/books/2")
    #     data = json.loads(res.data)

    #     book = Book.query.filter(Book.id == 2).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["deleted"], 2)
    #     self.assertTrue(data["total_books"])
    #     self.assertTrue(len(data["books"]))
    #     self.assertEqual(book, None)

    # def test_422_if_book_does_not_exist(self):
    #     res = self.client().delete("/books/1000")
    #     data = json.loads(res.data)
    #     print(f'Delete Failed:{data}')
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "unprocessable")

    def test_get_book_search_with_results(self):
            res = self.client().post('/books', json={'search':'Mobby'})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data["success"], True)
            self.assertTrue(data["total_books"])
            self.assertTrue(len(data['books']),4) 
            print (f'search_data: {data}')

    # def test_get_book_search_without_results(self):
    #         res = self.client().post('/books', json={'search':'Mobdy'})
    #         data = json.loads(res.data)
    #         print (f'search_data2: {data}')
    #         self.assertEqual(res.status_code, 200)
    #         self.assertEqual(data["success"], True)
    #         self.assertEqual(data["total_books"], 0)
    #         self.assertEqual(len(data["books"]),0)
            
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()