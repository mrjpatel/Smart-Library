from library.admin_dashboard.flask_main import app
import unittest
import json


class FlaskRouteTest(unittest.TestCase):
    """
    Class FlaskRouteTest test all the routing
    of all webpages
    """
    def setUp(self):
        self.app = app.test_client()

    # Tests Add book Flask API
    def test_addBooks(self):
        response = self.app.post(
            '/addBook',
            data=json.dumps({
                'title': "Test Book",
                'author': "Book Author",
                'publishedDate': "2019-05-05"
            }),
            content_type='application/json')
        assert response.status == '200 OK'

    # Tests Remove book Flask API
    def test_updateBooks(self):
        response = self.app.put(
            '/updateBook/21',
            data=json.dumps({
                'title': "New Book",
                'author': "New Author",
                'publishedDate': "2019-06-05"
            }),
            content_type='application/json')
        assert response.status == '200 OK'

    # Tests Admin Login Request Status
    def test_adminLoginRequest(self):
        response = self.app.post(
            '/adminLogin')
        assert response.status == '302 FOUND'

    # Test route for removing invalid books
    def test_removeInvalidBook(self):
        rv = self.app.post('/removeBook/0')
        assert rv.status == '405 METHOD NOT ALLOWED'

    # Test route for updating invalid books
    def test_updateInvalidBook(self):
        rv = self.app.post('/updateBook/0')
        assert rv.status == '405 METHOD NOT ALLOWED'

    # Test route status for Books
    def test_getAllBooks(self):
        rv = self.app.get('/books')
        assert rv.status == '200 OK'

    # Test route status for login page
    def test_renderLogin(self):
        rv = self.app.get('/login')
        assert rv.status == '200 OK'

    # Test route status for dashboard page
    def test_renderDashboard(self):
        rv = self.app.get('/dashboard')
        assert rv.status == '302 FOUND'

    # Test route status for Logout page
    def test_renderLogout(self):
        rv = self.app.get('/logout')
        assert rv.status == '302 FOUND'

    # Test route status for Add Book page
    def test_renderAddBook(self):
        rv = self.app.get('/book/add')
        assert rv.status == '302 FOUND'

    # Test route status for Remove Book page
    def test_renderRemoveBook(self):
        rv = self.app.get('/book/remove')
        assert rv.status == '302 FOUND'

    # Test route status for Update Book page
    def test_renderUpdateBook(self):
        rv = self.app.get('/book/update')
        assert rv.status == '302 FOUND'
