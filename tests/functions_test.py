from unittest2 import TestCase, main
from py_sak.functions import try_catch


class FunctionsTest(TestCase):
    def test_try_catch_no_args(self):
        self.assertEquals(try_catch(lambda: 1337), 1337)

    def test_try_catch_one_arg(self):
        self.assertEquals(try_catch(lambda x: x+1337, [1]), 1338)

    def test_try_catch_two_args(self):
        self.assertEquals(try_catch(lambda x,y: x+y+1337, [1, 1]), 1339)

    def test_try_catch_exception(self):
        error = RuntimeError(42)
        def throws():
            raise error
        self.assertEquals(try_catch(throws), error)
