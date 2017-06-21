# test_solutions.py
"""Volume 1B: Testing.
<Name>
<Class>
<Date>
"""

import solutions as soln
import pytest

# Problem 1: Test the addition and fibonacci functions from solutions.py
def test_addition():
    assert soln.addition(1, 3) == 4

def test_smallest_factor():
    assert soln.smallest_factor(1) == 1
    assert soln.smallest_factor(4) == 2
    assert soln.smallest_factor(3) == 3

# Problem 2: Test the operator function from solutions.py
def test_operator():
    with pytest.raises(Exception) as excinfo:
        soln.operator(2, 4, 6)
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "Oper should be a string"
    with pytest.raises(Exception) as excinfo:
        soln.operator(2, 4, "*+")
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "Oper should be one character"
    assert soln.operator(2, 4, "+") == 6
    with pytest.raises(Exception) as excinfo:
        soln.operator(2, 0, "/")
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "You can't divide by zero!"
    assert soln.operator(2, 4, "/") == 0.5
    assert soln.operator(2, 4, "-") == - 2
    assert soln.operator(2, 4, "*") == 8
    with pytest.raises(Exception) as excinfo:
        soln.operator(2, 4, "$")
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "Oper can only be: '+', '/', '-', or '*'"
    

# Problem 3: Finish testing the complex number class
@pytest.fixture
def set_up_complex_nums():
    number_1 = soln.ComplexNumber(1, 2)
    number_2 = soln.ComplexNumber(5, 5)
    number_3 = soln.ComplexNumber(2, 9)
    return number_1, number_2, number_3

def test_complex_addition(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1 + number_2 == soln.ComplexNumber(6, 7)
    assert number_1 + number_3 == soln.ComplexNumber(3, 11)
    assert number_2 + number_3 == soln.ComplexNumber(7, 14)
    assert number_3 + number_3 == soln.ComplexNumber(4, 18)

def test_complex_multiplication(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1 * number_2 == soln.ComplexNumber(-5, 15)
    assert number_1 * number_3 == soln.ComplexNumber(-16, 13)
    assert number_2 * number_3 == soln.ComplexNumber(-35, 55)
    assert number_3 * number_3 == soln.ComplexNumber(-77, 36)

def test_conjugate(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1.conjugate() == soln.ComplexNumber(1, -2)
    assert number_2.conjugate() == soln.ComplexNumber(5, -5)
    assert number_3.conjugate() == soln.ComplexNumber(2, -9)

def test_norm(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1.norm() == 5 ** 0.5
    assert number_2.norm() == 50 ** 0.5
    assert number_3.norm() == 85 ** 0.5

def test_complex_subtraction(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1 - number_2 == soln.ComplexNumber(-4, -3)
    assert number_1 - number_3 == soln.ComplexNumber(-1, -7)
    assert number_2 - number_3 == soln.ComplexNumber(3, -4)
    assert number_3 - number_3 == soln.ComplexNumber(0, 0)

def test_complex_division(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    with pytest.raises(Exception) as excinfo:
        number_1 / soln.ComplexNumber(0, 0)
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "Cannot divide by zero"
    assert number_1 / number_2 == soln.ComplexNumber(0.3, 0.1)
    assert number_3 / number_3 == soln.ComplexNumber(1, 0)   
    
def test_str(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert str(number_1) == "1+2i"
    

    
# Problem 4: Write test cases for the Set game.