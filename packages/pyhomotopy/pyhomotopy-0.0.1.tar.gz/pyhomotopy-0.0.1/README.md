pyHAM

Python module to apply Homotopy Analysis Method to nonlinear equations.

Current version supports the solution of nonlinear algebraic equations and boundary value problems of Ordinary Differential Equations (ODEs).
Main Classes of API

HamSolver HamBcs HamResult

See the examples in file hamExtTests.py. There are two examples.

    To solve nonlinear algebraic equation exp(-x**2)cos(4x)
    To solve the ODE BVP : y' - 1/x2 + y/x + y2 = 0, y(1) = -1

