import unittest
import json
import score_server


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        score_server.app.config['TESTING'] = True
        self.app = score_server.app.test_client()
        self.headers = {'content-type': 'application/json'}

    def test_ping_alive(self):
        response = self.app.post('/ping')
        self.assertEqual(response.status_code, 200)

    def test_ping_message(self):
        response = self.app.post('/ping')
        self.assertEqual(response.get_data(), "I'm alive")

    def test_no_body(self):
        response = self.app.post('/')
        self.assertEqual(response.status_code, 400)

    def test_no_route(self):
        response = self.app.post('/nowhere')
        self.assertEqual(response.status_code, 404)

    def test_body_but_invalid_data_no_list(self):
        bad_data = {'hello': 999}
        response = self.app.post('/', data=json.dumps(bad_data),
                                 headers=self.headers)
        self.assertEqual(response.status_code, 400)
        message = 'Request not valid, Json data is not a list'
        self.assertEqual(response.get_data(), message)

    def test_body_but_invalid_data_not_dicts(self):
        bad_data = [5, 6]
        response = self.app.post('/', data=json.dumps(bad_data),
                                 headers=self.headers)
        self.assertEqual(response.status_code, 400)
        message = 'Request not valid, Some list elements are not dictionaries'
        self.assertEqual(response.get_data(), message)

    def test_body_but_invalid_data_not_valid_dicts(self):
        bad_data = [{'hello': 8}, {'there': 99}]
        response = self.app.post('/', data=json.dumps(bad_data),
                                 headers=self.headers)
        self.assertEqual(response.status_code, 400)
        message = 'Request not valid, Some list elements missing ' \
                  'required fields'
        self.assertEqual(response.get_data(), message)

    def test_body_but_invalid_data_amounts_not_numbers(self):
        bad_data = [{'first_name': 'Dave',
                     'last_name': 'Johnston',
                     'address_num': 42,
                     'street': 'Main St',
                     'city': 'Boston',
                     'state': 'MA',
                     'amount': 'a string not a number'}]

        response = self.app.post('/', data=json.dumps(bad_data),
                                 headers=self.headers)
        self.assertEqual(response.status_code, 400)
        message = 'Request not valid, Some list elements amount ' \
                  'values are not numeric'
        self.assertEqual(response.get_data(), message)

    def test_valid_data(self):
        good_data = [{'first_name': 'Dave',
                      'last_name': 'Johnston',
                      'address_num': '42',
                      'street': 'Main St',
                      'city': 'Boston',
                      'state': 'MA',
                      'amount': '120'}]

        response = self.app.post('/', data=json.dumps(good_data),
                                 headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.get_data()
        self.assertTrue(isinstance(data, str))
        data_dict = json.loads(data)
        self.assertTrue(isinstance(data_dict, dict))
        self.assertTrue('recovered_millions' in data_dict)
        self.assertTrue('best_possible_recovered_millions' in data_dict)
        self.assertTrue('percent_recovered' in data_dict)
        self.assertEqual(data_dict['percent_recovered'], 0.0)
