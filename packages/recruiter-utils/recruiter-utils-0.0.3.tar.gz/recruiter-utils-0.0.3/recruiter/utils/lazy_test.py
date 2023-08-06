from . import lazy


def test_lazy():
    lazy_class = LazyClass()
    assert lazy_class.some_value == 100


class LazyClass:
    @lazy.Lazy
    def some_value(self):
        return 100
