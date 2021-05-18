from decorators import greetings, is_palindrome, format_output, add_class_method, add_instance_method
import pytest

#2.1
@greetings
def name_surname():
    return "jan nowak"

assert name_surname() == "Hello Jan Nowak"


#2.2
@is_palindrome
def sentence():
    return "Łapał za kran, a kanarka złapał."

assert sentence() == "Łapał za kran, a kanarka złapał. - is palindrome"


#2.3

@format_output("first_name__last_name", "city")
def first_func():
    return {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "city": "Warsaw"
    }


@format_output("first_name", "age")
def second_func():
    return {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "city": "Warsaw"
    }

assert first_func() == {"first_name__last_name": "Jan Kowalski", "city": "Warsaw"}
with pytest.raises(ValueError):
    second_func()


#2.4
class A:
    pass

@add_class_method(A)
def foo():
    return "Hello!"

@add_instance_method(A)
def bar():
    return "Hello again!"

assert A.foo() == "Hello!"
assert A().bar() == "Hello again!"