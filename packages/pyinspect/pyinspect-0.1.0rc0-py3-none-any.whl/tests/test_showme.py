import pyinspect as pi
from rich.console import Console  # to test with a class


def test_showme():
    # try with a function that works
    if not pi.showme(pi.showme):
        raise ValueError("pi.showme failed to print a funciton")

    # try with a class
    if not pi.showme(Console):
        raise ValueError("pi.showme failed to print a class")

    # try with a class' method
    if not pi.showme(Console.print):
        raise ValueError("pi.showme failed to print a class method")


class Test:
    a = 1  # a couple variables
    _private = "this is private !!"

    def hi(
        self,
    ):  # define a function
        """
        Say HI!
        """
        print("Hello world")


def test_showme_custom_class():
    t = Test()

    pi.showme(t)
    pi.showme(Test)
    pi.showme(t.a)
    pi.showme(Test.a)
    pi.showme(t.hi)
    pi.showme(Test.hi)


def test_caught_exception():
    # showme should not accept builtins and variables
    if pi.showme("a string"):  # showme returns False for bad inputs
        raise ValueError("pi.showme should not acccept variables")

    if pi.showme(sum):
        raise ValueError("pi.showme should not acccept builtins")
