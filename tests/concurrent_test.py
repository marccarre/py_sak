from unittest2 import TestCase, main
from py_sak.concurrent import concurrent_class_factory


class Incrementer(object):
    def increment(self, x):
        ''' Increment and return the provided value. '''
        return x + 1

class ConcurrentTest(TestCase):
    def test_concurrent_increment(self):
        ConcurrentIncrementer = concurrent_class_factory('ConcurrentIncrementer', Incrementer)
        concurrent_inc = ConcurrentIncrementer()
        self.assertEqual(concurrent_inc.increment([1, 2, 3, 4, 5]), [2, 3, 4, 5, 6])
