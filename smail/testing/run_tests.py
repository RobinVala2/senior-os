import unittest
from test_imap_connection import TestImapConnection
from test_send_mail import TestSendEmail
from test_json_file import TestLoadJsonFile

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestImapConnection))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSendEmail))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestLoadJsonFile))
    return test_suite

if __name__ == '__main__':
    # Run the Test Suite
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
