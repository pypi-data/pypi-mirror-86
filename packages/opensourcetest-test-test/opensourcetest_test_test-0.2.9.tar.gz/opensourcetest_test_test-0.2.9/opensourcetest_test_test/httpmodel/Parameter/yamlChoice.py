#!/user/bin/env python
# -*- coding: utf-8 -*-
from opensourcetest_test_test.builtin.autoParamInjection import AutoInjection
import inspect


class Login(AutoInjection):
    def __init__(self):
        super(Login, self).__init__(self.__class__.__name__)


if __name__ == '__main__':
    login = Login()
    print(inspect.getfile(login.__class__))
