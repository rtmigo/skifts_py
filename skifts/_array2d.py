import numpy as np


class Array2D:
    @staticmethod
    def sort_by_first_row(matrix: np.ndarray) -> np.ndarray:
        return matrix[:, matrix[0, :].argsort()]

    @staticmethod
    def reverse_rows(matrix: np.ndarray) -> np.ndarray:
        return matrix[:, ::-1]

    @staticmethod
    def keep_columns_with_nonzero_first_row(matrix: np.ndarray) -> np.ndarray:
        matrix = matrix[:, np.nonzero(matrix[0])]
        matrix = matrix.reshape(2, matrix[0].shape[1])
        return matrix
