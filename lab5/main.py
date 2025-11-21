import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple

class FuzzyAirConditioner:
    def __init__(self):
        # Определение термов для температуры воздуха
        self.temp_terms = {
            'NB': {'range': (10, 20), 'peak': 15},  # очень холодная
            'NS': {'range': (15, 25), 'peak': 20},  # холодная  
            'Z': {'range': (20, 30), 'peak': 25},   # нормальная
            'PS': {'range': (25, 35), 'peak': 30},  # теплая
            'PB': {'range': (30, 40), 'peak': 35}   # очень теплая
        }
        
        # Определение термов для скорости изменения температуры
        self.speed_terms = {
            'NS': {'range': (-1, 0), 'peak': -0.5},   # отрицательная
            'Z': {'range': (-0.5, 0.5), 'peak': 0},   # нулевая
            'PS': {'range': (0, 1), 'peak': 0.5}      # положительная
        }
        
        # Определение термов для угла поворота регулятора
        self.angle_terms = {
            'NB': {'range': (-90, -60), 'peak': -75},   # очень большой влево
            'NM': {'range': (-60, -30), 'peak': -45},   # большой влево
            'NS': {'range': (-30, 0), 'peak': -15},     # небольшой влево
            'Z': {'range': (-15, 15), 'peak': 0},       # выключить
            'PS': {'range': (0, 30), 'peak': 15},       # небольшой вправо
            'PM': {'range': (30, 60), 'peak': 45},      # большой вправо
            'PB': {'range': (60, 90), 'peak': 75}       # очень большой вправо
        }
        
        # База правил 
        self.rules = [
            (1, 'PB', 'PS', 'NB'),
            (2, 'PB', 'NS', 'NS'),
            (3, 'PS', 'PS', 'NM'),
            (4, 'PS', 'NS', 'Z'),
            (5, 'NB', 'NS', 'PB'),
            (6, 'NB', 'PS', 'PS'),
            (7, 'NS', 'NS', 'PM'),
            (8, 'NS', 'PS', 'Z'),
            (9, 'PB', 'Z', 'NM'),
            (10, 'PS', 'Z', 'NS'),
            (11, 'NB', 'Z', 'PM'),
            (12, 'NS', 'Z', 'PS'),
            (13, 'Z', 'PS', 'NS'),
            (14, 'Z', 'NS', 'PS'),
            (15, 'Z', 'Z', 'Z')
        ]

    def triangular_mf(self, x: float, a: float, b: float, c: float) -> float:
        """Треугольная функция принадлежности"""
        if x <= a or x >= c:
            return 0.0
        elif a < x <= b:
            return (x - a) / (b - a)
        else:
            return (c - x) / (c - b)

    def temp_membership(self, temp: float) -> Dict[str, float]:
        """Вычисление степеней принадлежности для температуры"""
        membership = {}
        for term, params in self.temp_terms.items():
            a, c = params['range']
            b = params['peak']
            membership[term] = self.triangular_mf(temp, a, b, c)
        return membership

    def speed_membership(self, speed: float) -> Dict[str, float]:
        """Вычисление степеней принадлежности для скорости"""
        membership = {}
        for term, params in self.speed_terms.items():
            a, c = params['range']
            b = params['peak']
            membership[term] = self.triangular_mf(speed, a, b, c)
        return membership

    def angle_membership(self, angle: float) -> Dict[str, float]:
        """Вычисление степеней принадлежности для угла"""
        membership = {}
        for term, params in self.angle_terms.items():
            a, c = params['range']
            b = params['peak']
            membership[term] = self.triangular_mf(angle, a, b, c)
        return membership

    def find_active_rules(self, temp: float, speed: float) -> List[Tuple]:
        """Поиск активных правил"""
        temp_mf = self.temp_membership(temp)
        speed_mf = self.speed_membership(speed)
        
        active_rules = []
        for rule_num, temp_term, speed_term, angle_term in self.rules:
            alpha = min(temp_mf.get(temp_term, 0), speed_mf.get(speed_term, 0))
            if alpha > 0:
                active_rules.append((rule_num, temp_term, speed_term, angle_term, alpha))
        
        return active_rules

    def mamdani_inference(self, temp: float, speed: float) -> np.ndarray:
        """Алгоритм Мамдани"""
        active_rules = self.find_active_rules(temp, speed)
        angles = np.linspace(-90, 90, 181)
        result_mf = np.zeros_like(angles)
        
        print("Активные правила (Мамдани):")
        for rule_num, temp_term, speed_term, angle_term, alpha in active_rules:
            print(f"Правило {rule_num}: ЕСЛИ temp={temp_term} И speed={speed_term} ТО angle={angle_term}, a={alpha:.2f}")
            
            # Min-активизация
            angle_mf = np.array([self.angle_membership(angle)[angle_term] for angle in angles])
            activated_mf = np.minimum(alpha, angle_mf)
            result_mf = np.maximum(result_mf, activated_mf)
        
        return angles, result_mf

    def larsen_inference(self, temp: float, speed: float) -> np.ndarray:
        """Алгоритм Ларсена"""
        active_rules = self.find_active_rules(temp, speed)
        angles = np.linspace(-90, 90, 181)
        result_mf = np.zeros_like(angles)
        
        print("\nАктивные правила (Ларсен):")
        for rule_num, temp_term, speed_term, angle_term, alpha in active_rules:
            print(f"Правило {rule_num}: ЕСЛИ temp={temp_term} И speed={speed_term} ТО angle={angle_term}, a={alpha:.2f}")
            
            # Prod-активизация
            angle_mf = np.array([self.angle_membership(angle)[angle_term] for angle in angles])
            activated_mf = alpha * angle_mf
            result_mf = np.maximum(result_mf, activated_mf)
        
        return angles, result_mf

    def defuzzify_cog(self, angles: np.ndarray, mf: np.ndarray) -> float:
        """
        Дефаззификация методом центра тяжести
        COG - метод центра тяжести, в котором
        определяфется абсцисса центра тяжести
        фигуры, ограниченной графиком ФП
        """
        if np.sum(mf) == 0:
            return 0.0
        return np.sum(angles * mf) / np.sum(mf)

    def defuzzify_mom(self, angles: np.ndarray, mf: np.ndarray) -> float:
        """
        Дефаззификация методом среднего максимума
        MOM - метод центра максимума, в котором
        ФП рассматривается как функция, представляющая
        рузельтирующее мн-то средним значением,
        соответствующим максимуму ФП
        """
        max_val = np.max(mf)
        if max_val == 0:
            return 0.0
        max_indices = np.where(mf == max_val)[0]
        return np.mean(angles[max_indices])

    def plot_results(self, angles: np.ndarray, mamdani_mf: np.ndarray, 
                    larsen_mf: np.ndarray, temp: float, speed: float):
        """Построение графиков результатов"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # График для Мамдани
        ax1.plot(angles, mamdani_mf, 'b-', linewidth=2, label='Результирующая ФП')
        ax1.fill_between(angles, 0, mamdani_mf, alpha=0.3)
        ax1.set_title('Алгоритм Мамдани')
        ax1.set_xlabel('Угол поворота регулятора (°)')
        ax1.set_ylabel('Степень принадлежности')
        ax1.grid(True)
        ax1.legend()
        
        # График для Ларсена
        ax2.plot(angles, larsen_mf, 'r-', linewidth=2, label='Результирующая ФП')
        ax2.fill_between(angles, 0, larsen_mf, alpha=0.3)
        ax2.set_title('Алгоритм Ларсена')
        ax2.set_xlabel('Угол поворота регулятора (°)')
        ax2.set_ylabel('Степень принадлежности')
        ax2.grid(True)
        ax2.legend()
        
        plt.tight_layout()
        plt.show()

class SugenoFuzzySystem:
    def __init__(self):
        # Функции для термов (линейные функции)
        self.rules = [
            {'A': 'среднее', 'B': 'среднее', 'f': lambda x, y: 2 + x + 2*y},
            {'A': 'малое', 'B': 'высокое', 'f': lambda x, y: 2 + 2*x + 3*y}
        ]
    
    def membership_A1(self, x: float) -> float:
        """Функция принадлежности для A1 """
        if 2 <= x <= 4:
            return (x - 2) / 2
        elif 4 < x <= 6:
            return (6 - x) / 2
        else:
            return 0.0
    
    def membership_A2(self, x: float) -> float:
        """Функция принадлежности для A2 """
        if 0 <= x <= 2:
            return x / 2
        elif 2 < x <= 4:
            return (4 - x) / 2
        else:
            return 0.0
    
    def membership_B1(self, y: float) -> float:
        """Функция принадлежности для B1 """
        if 2 <= y <= 4:
            return (y - 2) / 2
        elif 4 < y <= 6:
            return (6 - y) / 2
        else:
            return 0.0
    
    def membership_B2(self, y: float) -> float:
        """Функция принадлежности для B2 """
        if 4 <= y <= 8:
            return (y - 4) / 4
        elif 8 < y <= 12:
            return (12 - y) / 4
        else:
            return 0.0
    
    def sugeno_inference(self, x: float, y: float) -> float:
        """Алгоритм Такаги-Сугено"""
        print(f"\nАлгоритм Такаги-Сугено:")
        print(f"Входные значения: x={x}, y={y}")
        
        # Вычисление степеней принадлежности
        w1 = min(self.membership_A1(x), self.membership_B1(y))
        w2 = min(self.membership_A2(x), self.membership_B2(y))
        
        print(f"Степени истинности: w1={w1:.3f}, w2={w2:.3f}")
        
        # Вычисление значений функций
        z1 = self.rules[0]['f'](x, y)
        z2 = self.rules[1]['f'](x, y)
        
        print(f"Значения функций: z1={z1:.3f}, z2={z2:.3f}")
        
        # Дефаззификация
        if w1 + w2 == 0:
            return 0.0
        
        result = (w1 * z1 + w2 * z2) / (w1 + w2)
        print(f"Результат: z = ({w1:.3f}*{z1:.3f} + {w2:.3f}*{z2:.3f}) / ({w1:.3f} + {w2:.3f}) = {result:.3f}")
        
        return result

def main():    
    temp = 26.0      # x1
    speed = -0.4     # x2
    
    print(f"Температура воздуха: {temp}°C")
    print(f"Скорость изменения температуры: {speed}°C/мин")
    
    # Задание 1: Алгоритмы Мамдани и Ларсена
    fuzzy_system = FuzzyAirConditioner()
    
    # Мамдани
    angles, mamdani_mf = fuzzy_system.mamdani_inference(temp, speed)
    cog_mamdani = fuzzy_system.defuzzify_cog(angles, mamdani_mf)
    mom_mamdani = fuzzy_system.defuzzify_mom(angles, mamdani_mf)
    
    print(f"\nРезультаты Мамдани:")
    print(f"COG: {cog_mamdani:.2f}°")
    print(f"MOM: {mom_mamdani:.2f}°")
    
    # Ларсен
    angles, larsen_mf = fuzzy_system.larsen_inference(temp, speed)
    cog_larsen = fuzzy_system.defuzzify_cog(angles, larsen_mf)
    mom_larsen = fuzzy_system.defuzzify_mom(angles, larsen_mf)
    
    print(f"\nРезультаты Ларсена:")
    print(f"COG: {cog_larsen:.2f}°")
    print(f"MOM: {mom_larsen:.2f}°")
    
    # Построение графиков
    fuzzy_system.plot_results(angles, mamdani_mf, larsen_mf, temp, speed)
    
    # Таблица результатов
    print("Таблица результатов\n")
    print(f"{'Алгоритм':<15} {'COG':<10} {'MOM':<10}")
    print(f"{'Мамдани':<15} {cog_mamdani:<10.2f} {mom_mamdani:<10.2f}")
    print(f"{'Ларсен':<15} {cog_larsen:<10.2f} {mom_larsen:<10.2f}")
    
    # Задание 2: Алгоритм Такаги-Сугено
    print("\nТагаки-Сугено\n")
    
    sugeno_system = SugenoFuzzySystem()

    x = 3.2
    y = 5.5
    
    result_sugeno = sugeno_system.sugeno_inference(x, y)
    print(f"\nФинальный результат Такаги-Сугено: {result_sugeno:.3f}")
    

if __name__ == "__main__":
    main()