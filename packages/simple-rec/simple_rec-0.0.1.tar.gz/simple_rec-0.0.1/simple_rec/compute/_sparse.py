from typing import List, Union
import numpy as np


def _binary_search(query, keys):

    raise NotImplementedError()


class _CoordinateList:
    """Base class for _SparseMatrix

    """

    def __init__(self,
                 row_index: List[int] = [],
                 col_index: List[int]= [],
                 values: List[float] = []):

        self.__row_index = row_index
        self.__col_index = col_index
        self.__values = values


    @property
    def row_index(self):
        """Getter for row_index.

        """
        return self.__row_index

    @property
    def col_index(self):
        """Getter for col_index.

        """
        return self.__col_index

    @property
    def values(self):
        """Getter for values.

        """
        return self.__values

    @property
    def length(self):
        """Getter for length.

        """
        return len(self.values)

    def _insert(self,
                index: int,
                i: int,
                j: int,
                v: float):
        """Inserts an entry at index.

        """
        self.__row_index.insert(index, i)
        self.__col_index.insert(index, j)
        self.__values.insert(index, v)

    def _remove(self,
                index: int):
        """Deletes an entry at index.

        """
        del(self.__row_index[index])
        del(self.__col_index[index])
        del(self.__values[index])


class _SparseMatrix(_CoordinateList):
    # TODO: docstrings, efficient queries (binary search), _get, _add, _del

    def __init__(self,
                 row_index: List[int] = [],
                 col_index: List[int] = [],
                 values: List[float] = []):

        # sort by row_index, col_index and values
        zipped = list(zip(row_index, col_index, values))
        zipped.sort()
        row_index, col_index, values = zip(*zipped)

        # pass sorted as lists to super
        super(_SparseMatrix, self).__init__(list(row_index),
                                            list(col_index),
                                            list(values))

    def _get(self, i: int, j: int):
        """Returns entry at i, j.

        """
        raise NotImplementedError()


    def _row(self, i: int):
        """Returns the i-th row as a tuple (columns, values).

        """
        return (
            [col for col, row in zip(self.col_index, self.row_index) if row == i],
            [val for val, row in zip(self.values, self.row_index) if row == i]
        )

    def _col(self, j: int):
        """Returns the j-th column as a tuple (rows, values).

        """
        return (
            [row for row, col in zip(self.row_index, self.col_index) if col == j],
            [val for val, col in zip(self.values, self.col_index) if col == j]
        )

    def _add(self, i: int, j: int, v: float):
        """Adds the entry v at i, j.

        """
        raise NotImplementedError()

    def _del(self, i: int, j: int):
        """Deletes the entry at i, j.

        """
        raise NotImplementedError()


class _SparseDecomposeMixin:
    # TODO: docstrings

    U: np.ndarray
    V: np.ndarray
    _lambda: float
    k: int


    def _row_step(self):
        """

        """
        mse = 0.
        for i, u in enumerate(self.U):
            
            cols, vals = self._row(i)
            vals = np.array(vals)

            scatter = self._lambda * np.eye(self.k)
            scatter = scatter + \
                sum([np.outer(self.V[j], self.V[j]) for j in cols])

            linear = (self.V[cols] * vals[:, None]).sum(0)

            assert scatter.shape == (self.k, self.k)
            assert linear.shape == (self.k, )

            self.U[i] = np.linalg.inv(scatter).dot(linear).squeeze()
            mse += np.power(self.V[cols].dot(self.U[i]) - vals, 2).mean()
        
        return mse / len(self.U)

    def _col_step(self):
        """

        """
        mse = 0.
        for j, v in enumerate(self.V):
            
            rows, vals = self._col(j)
            vals = np.array(vals)

            scatter = self._lambda * np.eye(self.k)
            scatter = scatter + \
                sum([np.outer(self.U[i], self.U[i]) for i in rows])

            linear = (self.U[rows] * vals[:, None]).sum(0)

            assert scatter.shape == (self.k, self.k)
            assert linear.shape == (self.k, )

            self.V[j] = np.linalg.inv(scatter).dot(linear).squeeze()
            mse += np.power(self.U[rows].dot(self.V[j]) - vals, 2).mean()
        
        return mse / len(self.V)

    def _decompose(self,
                   n_rows: int,
                   n_cols: int,
                   k: int = 16,
                   _lambda: float = 1e-3,
                   min_iter: int = 5,
                   max_iter: int = 10,
                   eps: float = 1e-5):
        """

        """

        self.U = np.random.randn(n_rows, k)
        self.V = np.random.randn(n_cols, k)
        self._lambda = _lambda
        self.k = k

        mse = []
        for _ in range(max_iter):
            # decompose matrix in two steps
            mse.append(0.5 * self._row_step() + 0.5 * self._col_step())
            # check when to stop
            if len(mse) < min_iter:
                continue
            if len(mse) > max_iter - 1:
                break
            if mse[-1] < eps:
                break
    
        return mse[-1]
