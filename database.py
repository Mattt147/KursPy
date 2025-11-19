"""
Простая база данных SQLite для хранения данных проекта
"""
import sqlite3
import json
from datetime import datetime
import os


class Database:
    def __init__(self, db_name="kurspy.db"):
        """Инициализация базы данных"""
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Получить соединение с БД"""
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        """Создание таблиц, если их нет"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Таблица для графов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS graphs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                vertices INTEGER NOT NULL,
                edges INTEGER NOT NULL,
                matrix TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица для матриц
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS matrices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                matrix_a TEXT NOT NULL,
                matrix_b TEXT NOT NULL,
                result TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица для результатов сортировки
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sorts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                array_size INTEGER NOT NULL,
                input_array TEXT NOT NULL,
                algorithm TEXT NOT NULL,
                sorted_array TEXT NOT NULL,
                comparisons INTEGER NOT NULL,
                time_taken REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # ========================================================================
    # РАБОТА С ГРАФАМИ
    # ========================================================================
    
    def save_graph(self, name, vertices, edges, matrix):
        """Сохранить граф"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        matrix_json = json.dumps(matrix)
        cursor.execute('''
            INSERT INTO graphs (name, vertices, edges, matrix)
            VALUES (?, ?, ?, ?)
        ''', (name, vertices, edges, matrix_json))
        
        conn.commit()
        graph_id = cursor.lastrowid
        conn.close()
        return graph_id
    
    def get_all_graphs(self):
        """Получить все графы"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, vertices, edges, matrix, created_at
            FROM graphs
            ORDER BY created_at DESC
        ''')
        
        graphs = []
        for row in cursor.fetchall():
            graphs.append({
                'id': row[0],
                'name': row[1],
                'vertices': row[2],
                'edges': row[3],
                'matrix': json.loads(row[4]),
                'created_at': row[5]
            })
        
        conn.close()
        return graphs
    
    def get_graph(self, graph_id):
        """Получить граф по ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, vertices, edges, matrix, created_at
            FROM graphs
            WHERE id = ?
        ''', (graph_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'vertices': row[2],
                'edges': row[3],
                'matrix': json.loads(row[4]),
                'created_at': row[5]
            }
        return None
    
    def delete_graph(self, graph_id):
        """Удалить граф"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM graphs WHERE id = ?', (graph_id,))
        conn.commit()
        conn.close()
    
    # ========================================================================
    # РАБОТА С МАТРИЦАМИ
    # ========================================================================
    
    def save_matrices(self, name, matrix_a, matrix_b, result=None):
        """Сохранить матрицы и результат"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        matrix_a_json = json.dumps(matrix_a)
        matrix_b_json = json.dumps(matrix_b)
        result_json = json.dumps(result) if result else None
        
        cursor.execute('''
            INSERT INTO matrices (name, matrix_a, matrix_b, result)
            VALUES (?, ?, ?, ?)
        ''', (name, matrix_a_json, matrix_b_json, result_json))
        
        conn.commit()
        matrix_id = cursor.lastrowid
        conn.close()
        return matrix_id
    
    def get_all_matrices(self):
        """Получить все сохраненные матрицы"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, matrix_a, matrix_b, result, created_at
            FROM matrices
            ORDER BY created_at DESC
        ''')
        
        matrices = []
        for row in cursor.fetchall():
            matrices.append({
                'id': row[0],
                'name': row[1],
                'matrix_a': json.loads(row[2]),
                'matrix_b': json.loads(row[3]),
                'result': json.loads(row[4]) if row[4] else None,
                'created_at': row[5]
            })
        
        conn.close()
        return matrices
    
    def get_matrices(self, matrix_id):
        """Получить матрицы по ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, matrix_a, matrix_b, result, created_at
            FROM matrices
            WHERE id = ?
        ''', (matrix_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'matrix_a': json.loads(row[2]),
                'matrix_b': json.loads(row[3]),
                'result': json.loads(row[4]) if row[4] else None,
                'created_at': row[5]
            }
        return None
    
    def delete_matrices(self, matrix_id):
        """Удалить матрицы"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM matrices WHERE id = ?', (matrix_id,))
        conn.commit()
        conn.close()
    
    # ========================================================================
    # РАБОТА С СОРТИРОВКОЙ
    # ========================================================================
    
    def save_sort_result(self, name, array_size, input_array, algorithm, 
                        sorted_array, comparisons, time_taken):
        """Сохранить результат сортировки"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        input_json = json.dumps(input_array)
        sorted_json = json.dumps(sorted_array)
        
        cursor.execute('''
            INSERT INTO sorts (name, array_size, input_array, algorithm, 
                             sorted_array, comparisons, time_taken)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, array_size, input_json, algorithm, sorted_json, 
              comparisons, time_taken))
        
        conn.commit()
        sort_id = cursor.lastrowid
        conn.close()
        return sort_id
    
    def get_all_sorts(self, algorithm=None):
        """Получить все результаты сортировки"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if algorithm:
            cursor.execute('''
                SELECT id, name, array_size, input_array, algorithm,
                       sorted_array, comparisons, time_taken, created_at
                FROM sorts
                WHERE algorithm = ?
                ORDER BY created_at DESC
            ''', (algorithm,))
        else:
            cursor.execute('''
                SELECT id, name, array_size, input_array, algorithm,
                       sorted_array, comparisons, time_taken, created_at
                FROM sorts
                ORDER BY created_at DESC
            ''')
        
        sorts = []
        for row in cursor.fetchall():
            sorts.append({
                'id': row[0],
                'name': row[1],
                'array_size': row[2],
                'input_array': json.loads(row[3]),
                'algorithm': row[4],
                'sorted_array': json.loads(row[5]),
                'comparisons': row[6],
                'time_taken': row[7],
                'created_at': row[8]
            })
        
        conn.close()
        return sorts
    
    def get_sort(self, sort_id):
        """Получить результат сортировки по ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, array_size, input_array, algorithm,
                   sorted_array, comparisons, time_taken, created_at
            FROM sorts
            WHERE id = ?
        ''', (sort_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'array_size': row[2],
                'input_array': json.loads(row[3]),
                'algorithm': row[4],
                'sorted_array': json.loads(row[5]),
                'comparisons': row[6],
                'time_taken': row[7],
                'created_at': row[8]
            }
        return None
    
    def delete_sort(self, sort_id):
        """Удалить результат сортировки"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM sorts WHERE id = ?', (sort_id,))
        conn.commit()
        conn.close()
    
    # ========================================================================
    # СТАТИСТИКА
    # ========================================================================
    
    def get_stats(self):
        """Получить статистику по БД"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Количество графов
        cursor.execute('SELECT COUNT(*) FROM graphs')
        stats['graphs_count'] = cursor.fetchone()[0]
        
        # Количество матриц
        cursor.execute('SELECT COUNT(*) FROM matrices')
        stats['matrices_count'] = cursor.fetchone()[0]
        
        # Количество результатов сортировки
        cursor.execute('SELECT COUNT(*) FROM sorts')
        stats['sorts_count'] = cursor.fetchone()[0]
        
        # Среднее время сортировки по алгоритмам
        cursor.execute('''
            SELECT algorithm, AVG(time_taken), AVG(comparisons)
            FROM sorts
            GROUP BY algorithm
        ''')
        stats['sort_stats'] = {}
        for row in cursor.fetchall():
            stats['sort_stats'][row[0]] = {
                'avg_time': row[1],
                'avg_comparisons': row[2]
            }
        
        conn.close()
        return stats
    
    def clear_all(self):
        """Очистить все таблицы"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM graphs')
        cursor.execute('DELETE FROM matrices')
        cursor.execute('DELETE FROM sorts')
        
        conn.commit()
        conn.close()


# Глобальный экземпляр БД
db = Database()

