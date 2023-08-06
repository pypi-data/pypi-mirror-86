import sys
import os
import unittest

from client_part.client_packages.client import ClientTransport

sys.path.append(os.path.join(os.getcwd(), '../..'))


class TestClass(unittest.TestCase):

    def test_client_data(self):
        ip = 1
        port = 8888
        test = ClientTransport.connection_init(self, ip, port)
        test[TIME] = 1.1
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1,
                                USER: {ACCOUNT_NAME: 'Guest'}})

    def test_check_200(self):
        server_address = "127.0.0.1"
        message = {RESPONSE: 200}
        self.assertEqual(ClientTransport.process_answer(message),
                         f'200 : успешное соединение с сервером {server_address}')

    def test_check_400(self):
        self.assertEqual(ClientTransport.process_answer({RESPONSE: 400, ERROR:
            'Bad Request'}), '400 : Bad Request')

    def test_no_response(self):
        self.assertRaises(ValueError, ClientTransport.process_answer,
                          {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()

