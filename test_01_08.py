# Copyright (C) 2018 GuQiangJs.
# Licensed under https://www.gnu.org/licenses/gpl-3.0.html <see LICENSE file>

import unittest

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo

import test_helper


class MyTestCase(test_helper.MyTestBase):
    def test_run(self):
        Xguess = 2.0
        min_result = spo.minimize(MyTestCase.f, Xguess, method='SLSQP', options={'disp': True})
        print('Minima found at:')
        print('X={X}, Y={Y}'.format(X=min_result.x, Y=min_result.fun))

        Xplot = np.linspace(0.5, 2.5, 21)
        Yplot = MyTestCase.f(Xplot)
        plt.plot(Xplot, Yplot)
        plt.plot(min_result.x, min_result.fun, 'ro')
        plt.title('Minima of an objective function')
        plt.show()

    def f(X):
        Y = (X - 1.5) ** 2 + 0.5
        print('X={X}, Y={Y}'.format(X=X, Y=Y))
        return Y


if __name__ == '__main__':
    unittest.main()
