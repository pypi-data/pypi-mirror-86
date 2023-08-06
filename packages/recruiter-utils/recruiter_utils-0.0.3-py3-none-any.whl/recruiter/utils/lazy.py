class Lazy:
    """
    class A:
        @Lazy
        def answer_to_life(self):
            return expensive_calculation

    obj = A()
    print(obj.answer_to_life) # will calculate and store
    print(obj.answer_to_life) # will just look up stored value
    """

    def __init__(self, calculate_function) -> None:
        self._calculate = calculate_function

    def __get__(self, obj, _=None):
        if obj is None:
            return self
        value = self._calculate(obj)
        setattr(obj, self._calculate.__name__, value)
        return value
