from project import prime, perfect, square, consecutive_rearrange

def test_prime():
    assert prime(1) == False
    assert prime(2) == True
    assert prime(20) == False
    assert prime(23) == True

def test_perfect():
    assert perfect(1) == True
    assert perfect(2) == False
    assert perfect(6) == True
    assert perfect(28) == True
    assert perfect(496) == True
    assert perfect(500) == False

def test_square():
    assert square(1) == True
    assert square(16) == True
    assert square(121) == True
    assert square(2) == False

def test_consecutive_rearrange():
    assert consecutive_rearrange(123123123) == True
    assert consecutive_rearrange(12343216) == False
    assert consecutive_rearrange(1) == True
    assert consecutive_rearrange(9087) == False
