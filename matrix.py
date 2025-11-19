import time
import random

def matrix_multiplication(A, B):
    """Умножение матриц O(n³) - полиномиальная сложность"""
    comparisons = 0
    start_time = time.time()
    
    n = len(A)
    # Создаем результирующую матрицу заполненную нулями
    C = [[0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                comparisons += 1
                C[i][j] += A[i][k] * B[k][j]
    
    time_taken = time.time() - start_time
    return C, comparisons, time_taken

def generate_matrix(size):
    """Генерация случайной матрицы"""
    return [[random.randint(1, 10) for _ in range(size)] for _ in range(size)]