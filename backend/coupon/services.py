# 자주 사용하는 class or def 모음
import random


def convert():
    """
        쿠폰 이름 랜덤 생성 10~15자리
    """
    encoding = []
    encoding += [chr(i) for i in range(65, 91)]
    encoding += [chr(i) for i in range(97, 123)]
    encoding += [str(i) for i in range(10)]
    random_len = random.choice(range(10, 16))
    return "".join([random.choice(encoding) for i in range(random_len)])
