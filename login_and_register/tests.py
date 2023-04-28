from django.test import TestCase, Client

# Create your tests here.


class TestAuth(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login(self):
        # request.session['username'] = None
        response = self.client.post('/', {'email': 'hi@yahoo.com', 'password': 'rohnikhilt2002',
                                          })
        print(response.status_code)
        self.assertEqual(response.status_code, 401)

    def test_login1(self):
        response = self.client.post(
            '/', {'email': 'maharth@gmail.com', 'password': 'maharth'})
        self.assertEqual(response.status_code, 200)

    def test_login2(self):
        response = self.client.post(
            '/', {'email': 'hello@gmail.com', 'password': 'hello'})
        self.assertEqual(response.status_code, 200)

    def test_login3(self):
        response = self.client.post(
            '/', {'email': 'pinak@gmail.com', 'password': 'pinak'})
        self.assertEqual(response.status_code, 401)
