from app.utils.singleton_meta import SingletonMeta


class MyClass(metaclass=SingletonMeta):
    def __init__(self, value):
        self.value = value

def test_singleton_instances_are_same():
    obj1 = MyClass(1)
    obj2 = MyClass(2)
    assert obj1 is obj2
    # The value should be from the first instantiation only
    assert obj1.value == 1
    assert obj2.value == 1

def test_singleton_multiple_classes():
    class AnotherClass(metaclass=SingletonMeta):
        def __init__(self, data):
            self.data = data

    obj_a1 = AnotherClass('a')
    obj_a2 = AnotherClass('b')
    obj_m1 = MyClass(3)

    assert obj_a1 is obj_a2
    assert obj_a1.data == 'a'
    assert obj_m1.value == 1  # MyClass instance still holds first value
