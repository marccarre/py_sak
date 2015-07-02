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

class Exponentiator(object):
    def __init__(self, factor, exponent):
        self._factor   = factor
        self._exponent = exponent
    def exponentiate(self, x):
        return self._factor * (x ** self._exponent)
ConcurrentExponentiator = concurrent_class_factory('ConcurrentExponentiator', Exponentiator)

class ChaosMonkey(object):
    def throws(self, x):
        raise RuntimeError(x)
ConcurrentChaosMonkey = concurrent_class_factory('ConcurrentChaosMonkey', ChaosMonkey)


class ConcurrentTest(TestCase):
    def test_concurrent_increment(self):        
        concurrent_obj = ConcurrentIncrementer()
        self.assertEqual(concurrent_obj.increment([1, 2, 3, 4, 5]), [2, 3, 4, 5, 6])

    def test_concurrent_multiply(self):
        concurrent_obj = ConcurrentMultiplier(factory_args=[2])
        self.assertEqual(concurrent_obj.multiply([1, 2, 3, 4, 5]), [2, 4, 6, 8, 10])

    def test_concurrent_exponentiate(self):
        concurrent_obj = ConcurrentExponentiator(factory_args=[3, 2])
        self.assertEqual(concurrent_obj.exponentiate([1, 2, 3, 4, 5]), [3, 12, 27, 48, 75])

    def test_concurrent_throws_with_exception_handling(self):
        concurrent_obj = ConcurrentChaosMonkey()
        self.assertEqual([str(x) for x in concurrent_obj.throws([1, 2, 3, 4, 5])], ['1', '2', '3', '4', '5'])

    def test_concurrent_throws_without_exception_handling(self):
        concurrent_obj = ConcurrentChaosMonkey(raise_exceptions=True)
        with self.assertRaises(RuntimeError) as cm:
            concurrent_obj.throws([1, 2, 3, 4, 5])
        self.assertEqual(str(cm.exception), '1')

    def test_docstring_is_preserved_when_possible(self):
        concurrent_inc = ConcurrentIncrementer()
        self.assertEqual(concurrent_inc.increment.__doc__, ' Increment and return the provided value. ')
        concurrent_multiplier = ConcurrentMultiplier(factory_args=[2])
        self.assertEqual(concurrent_multiplier.multiply.__doc__, None)

    def test_private_methods_are_not_wrapped(self):
        concurrent_multiplier = ConcurrentMultiplier(factory_args=[2])
        self.assertTrue(hasattr(concurrent_multiplier, 'multiply'))
        self.assertFalse(hasattr(concurrent_multiplier, '_do_multiply'))
