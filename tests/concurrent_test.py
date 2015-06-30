from unittest2 import TestCase, main
from py_sak.concurrent import concurrent_class_factory


class Incrementer(object):
    def increment(self, x):
        ''' Increment and return the provided value. '''
        return x + 1

ConcurrentIncrementer = concurrent_class_factory('ConcurrentIncrementer', Incrementer)


class Multiplier(object):
    def __init__(self, factor):
        self._factor = factor
    def multiply(self, x):
        return self._do_multiply(x)
    def _do_multiply(self, x):
        return self._factor * x

ConcurrentMultiplier = concurrent_class_factory('ConcurrentMultiplier', Multiplier)


class ConcurrentTest(TestCase):
    def test_concurrent_increment(self):        
        concurrent_inc = ConcurrentIncrementer()
        self.assertEqual(concurrent_inc.increment([1, 2, 3, 4, 5]), [2, 3, 4, 5, 6])

    def test_concurrent_multiply(self):
        concurrent_multiplier = ConcurrentMultiplier(factory_args=[2])
        self.assertEqual(concurrent_multiplier.multiply([1, 2, 3, 4, 5]), [2, 4, 6, 8, 10])

    def test_docstring_is_preserved_when_possible(self):
        concurrent_inc = ConcurrentIncrementer()
        self.assertEqual(concurrent_inc.increment.__doc__, ' Increment and return the provided value. ')
        concurrent_multiplier = ConcurrentMultiplier(factory_args=[2])
        self.assertEqual(concurrent_multiplier.multiply.__doc__, None)

    def test_private_methods_are_not_wrapped(self):
        concurrent_multiplier = ConcurrentMultiplier(factory_args=[2])
        self.assertTrue(hasattr(concurrent_multiplier, 'multiply'))
        self.assertFalse(hasattr(concurrent_multiplier, '_do_multiply'))
