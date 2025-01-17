import numpy as np


from benchopt import BaseSolver


class Solver(BaseSolver):
    '''
    Alternating Proximal gradient
    '''
    name = "apg"

    # any parameter defined here is accessible as a class attribute
    parameters = {
        'n_inner_iter': [1, 5]
    }

    def set_objective(self, X, rank, fac_init):
        # The arguments of this function are the results of the
        # `to_dict` method of the objective.
        # They are customizable.
        self.X = X
        self.rank = rank
        self.fac_init = fac_init  # None if not initialized beforehand

    def run(self, n_iter):
        m, n = self.X.shape
        rank = self.rank
        n_inner_iter = self.n_inner_iter

        if not self.fac_init:
            # Random init if init is not provided
            self.fac = [np.random.rand(m, rank), np.random.rand(rank, n)]
        else:
            self.fac = [np.copy(self.fac_init[i]) for i in range(2)]

        for _ in range(n_iter):
            HHt = np.dot(self.fac[1], self.fac[1].T)
            XHt = np.dot(self.X, self.fac[1].T)
            Lw = np.linalg.norm(HHt)  # upper bound of Lw
            # W update
            for inner in range(n_inner_iter):
                self.fac[0] = np.maximum(
                    self.fac[0] - (np.dot(self.fac[0], HHt) - XHt) / Lw, 0)

            # H update
            WtW = np.dot(self.fac[0].T, self.fac[0])
            WtX = np.dot(self.fac[0].T, self.X)
            Lh = np.linalg.norm(WtW)  # upper bound for Lh
            # H update
            for inner in range(n_inner_iter):
                self.fac[1] = np.maximum(
                    self.fac[1] - (np.dot(WtW, self.fac[1]) - WtX) / Lh, 0)

    def get_result(self):
        # The outputs of this function are the arguments of the
        # `compute` method of the objective.
        # They are customizable.
        return self.fac
