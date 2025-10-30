import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class FuzzyTemperature:
    def __init__(self):
        self.x_min = 0
        self.x_max = 40
        self.x = np.linspace(self.x_min, self.x_max, 1000)
        self.x0 = 22  # фиксированная точка
        
    # прохладная
    def mu_A1(self, x):
        if x <= 15:
            return 1.0
        elif 15 < x < 25:
            return (25 - x) / 10
        else:
            return 0.0
    
    # Нормальная
    def mu_A2(self, x):
        if x <= 20:
            return 0.0
        elif 20 < x < 25:
            return (x - 20) / 5
        elif 25 <= x <= 30:
            return 1.0
        elif 30 < x < 35:
            return (35 - x) / 5
        else:
            return 0.0
    
    # Довольно жарко
    def mu_A3(self, x):
        if x <= 30:
            return 0.0
        elif 30 < x < 40:
            return (x - 30) / 10
        else:
            return 1.0
    
    # Операции
    def complement(self, mu):
        return 1 - mu
    
    def t_min(self, mu1, mu2):
        return min(mu1, mu2)
    
    def t_prod(self, mu1, mu2):
        return mu1 * mu2
    
    def t_max(self, mu1, mu2):
        return max(mu1, mu2)
    
    def t_lukasiewicz(self, mu1, mu2):
        return max(0, mu1 + mu2 - 1)
    
    def s_max(self, mu1, mu2):
        return max(mu1, mu2)
    
    def s_sum(self, mu1, mu2):
        return min(1, mu1 + mu2)
    
    def s_min(self, mu1, mu2):
        return min(1, mu1 + mu2 - mu1 * mu2)
    
    def s_lukasiewicz(self, mu1, mu2):
        return min(1, mu1 + mu2)
    
    # Лингвистические модификации
    def concentration(self, mu):
        return mu ** 2  # "очень"
    
    def dilation(self, mu):
        return mu ** 0.5  # "довольно"

def main():
    fuzzy = FuzzyTemperature()
    
    # 1. Графики функций принадлежности
    mu_A1_vals = [fuzzy.mu_A1(xi) for xi in fuzzy.x]
    mu_A2_vals = [fuzzy.mu_A2(xi) for xi in fuzzy.x]
    mu_A3_vals = [fuzzy.mu_A3(xi) for xi in fuzzy.x]
    
    plt.figure(figsize=(12, 6))
    plt.plot(fuzzy.x, mu_A1_vals, 'b-', label='A1: Прохладная ', linewidth=2)
    plt.plot(fuzzy.x, mu_A2_vals, 'g-', label='A2: Нормальная ', linewidth=2)
    plt.plot(fuzzy.x, mu_A3_vals, 'r-', label='A3: Довольно жарко ', linewidth=2)
    
    # Отметим точку x0
    mu_A1_x0 = fuzzy.mu_A1(fuzzy.x0)
    mu_A2_x0 = fuzzy.mu_A2(fuzzy.x0)
    mu_A3_x0 = fuzzy.mu_A3(fuzzy.x0)
    
    plt.axvline(x=fuzzy.x0, color='k', linestyle='--', alpha=0.7, label=f'x₀ = {fuzzy.x0}°C')
    plt.plot(fuzzy.x0, mu_A1_x0, 'bo', markersize=8)
    plt.plot(fuzzy.x0, mu_A2_x0, 'go', markersize=8)
    plt.plot(fuzzy.x0, mu_A3_x0, 'ro', markersize=8)
    
    plt.xlabel('Температура, °C')
    plt.ylabel('Степень принадлежности μ(x)')
    plt.title('Функции принадлежности нечетких подмножеств')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    
    # 2. Значения в точке x0
    print("ЗНАЧЕНИЯ В ТОЧКЕ x0 = 22°C:")
    print(f"μ_A1(x0) = {mu_A1_x0:.3f} (Прохладная)")
    print(f"μ_A2(x0) = {mu_A2_x0:.3f} (Нормальная)") 
    print(f"μ_A3(x0) = {mu_A3_x0:.3f} (Довольно жарко)")
    
    # 3. Свойства A2
    print("СВОЙСТВА НЕЧЕТКОГО ПОДМНОЖЕСТВА A2 (НОРМАЛЬНАЯ):")
    
    # Найдем ядро, носитель и точку перехода
    core_A2 = [x for x in fuzzy.x if abs(fuzzy.mu_A2(x) - 1.0) < 0.001]
    support_A2 = [x for x in fuzzy.x if fuzzy.mu_A2(x) > 0]
    crossover_A2 = [x for x in fuzzy.x if abs(fuzzy.mu_A2(x) - 0.5) < 0.01]
    
    print(f"Ядро (μ=1): [{core_A2[0]:.1f}, {core_A2[-1]:.1f}]°C")
    print(f"Носитель (μ>0): [{support_A2[0]:.1f}, {support_A2[-1]:.1f}]°C")
    print(f"Точка перехода (μ=0.5): {crossover_A2[0]:.1f}°C и {crossover_A2[-1]:.1f}°C\n")
    
    # 4. Лингвистические модификации A2
    print("ЛИНГВИСТИЧЕСКИЕ МОДИФИКАЦИИ A2:")
    
    mu_A2_very = fuzzy.concentration(mu_A2_x0)
    mu_A2_fairly = fuzzy.dilation(mu_A2_x0)
    
    print(f"ОЧЕНЬ нормальная (CON): μ = {mu_A2_x0:.3f}² = {mu_A2_very:.3f}")
    print(f"ДОВОЛЬНО нормальная (DIL): μ = √{mu_A2_x0:.3f} = {mu_A2_fairly:.3f}\n")
    
    # 5. Таблица операций
    print("ТАБЛИЦА ОПЕРАЦИЙ НАД НЕЧЕТКИМИ МНОЖЕСТВАМИ:")
    
    # Выполним операции для x0
    operations_data = []
    
    # Дополнение A1
    comp_A1 = fuzzy.complement(mu_A1_x0)
    operations_data.append(['Дополнение A1', f'1 - μ_A1(x)', f'1 - {mu_A1_x0:.3f}', f'{comp_A1:.3f}'])
    
    # T-нормы (пересечения)
    t_min_val = fuzzy.t_min(mu_A1_x0, mu_A2_x0)
    t_prod_val = fuzzy.t_prod(mu_A1_x0, mu_A2_x0)
    t_max_val = fuzzy.t_max(mu_A1_x0, mu_A2_x0)
    t_luk_val = fuzzy.t_lukasiewicz(mu_A1_x0, mu_A2_x0)
    
    operations_data.append(['T_min(A1,A2)', f'min(μ_A1, μ_A2)', f'min({mu_A1_x0:.3f}, {mu_A2_x0:.3f})', f'{t_min_val:.3f}'])
    operations_data.append(['T_prod(A1,A2)', f'μ_A1 × μ_A2', f'{mu_A1_x0:.3f} × {mu_A2_x0:.3f}', f'{t_prod_val:.3f}'])
    operations_data.append(['T_max(A1,A2)', f'max(μ_A1, μ_A2)', f'max({mu_A1_x0:.3f}, {mu_A2_x0:.3f})', f'{t_max_val:.3f}'])
    operations_data.append(['T_△(A1,A2)', f'max(0, μ_A1+μ_A2-1)', f'max(0, {mu_A1_x0:.3f}+{mu_A2_x0:.3f}-1)', f'{t_luk_val:.3f}'])
    
    # S-нормы (объединения)
    s_max_val = fuzzy.s_max(mu_A1_x0, mu_A2_x0)
    s_sum_val = fuzzy.s_sum(mu_A1_x0, mu_A2_x0)
    s_min_val = fuzzy.s_min(mu_A1_x0, mu_A2_x0)
    s_luk_val = fuzzy.s_lukasiewicz(mu_A1_x0, mu_A2_x0)
    
    operations_data.append(['S_max(A1,A2)', f'max(μ_A1, μ_A2)', f'max({mu_A1_x0:.3f}, {mu_A2_x0:.3f})', f'{s_max_val:.3f}'])
    operations_data.append(['S_sum(A1,A2)', f'min(1, μ_A1+μ_A2)', f'min(1, {mu_A1_x0:.3f}+{mu_A2_x0:.3f})', f'{s_sum_val:.3f}'])
    operations_data.append(['S_min(A1,A2)', f'min(1, μ_A1+μ_A2-μ_A1×μ_A2)', 
                          f'min(1, {mu_A1_x0:.3f}+{mu_A2_x0:.3f}-{mu_A1_x0:.3f}×{mu_A2_x0:.3f})', f'{s_min_val:.3f}'])
    operations_data.append(['S_△(A1,A2)', f'min(1, μ_A1+μ_A2)', f'min(1, {mu_A1_x0:.3f}+{mu_A2_x0:.3f})', f'{s_luk_val:.3f}'])
    
    # Создаем и выводим таблицу
    df_operations = pd.DataFrame(operations_data, columns=['Операция', 'Математическая запись', 'Вычисление', 'Результат'])
    print(df_operations.to_string(index=False))
    
    # 6. Дискретное представление
    print("\nДИСКРЕТНОЕ ПРЕДСТАВЛЕНИЕ НЕЧЕТКИХ ПОДМНОЖЕСТВ:")
    
    discrete_points = [0, 10, 15, 20, 22, 25, 30, 35, 40]
    
    print("A1 = {", end="")
    for i, x in enumerate(discrete_points):
        mu = fuzzy.mu_A1(x)
        if mu > 0:
            print(f" {mu:.1f}/{x}", end="")
            if i < len(discrete_points) - 1 and any(fuzzy.mu_A1(discrete_points[j]) > 0 for j in range(i+1, len(discrete_points))):
                print(" ∪", end="")
    print(" }")
    
    print("A2 = {", end="")
    for i, x in enumerate(discrete_points):
        mu = fuzzy.mu_A2(x)
        if mu > 0:
            print(f" {mu:.1f}/{x}", end="")
            if i < len(discrete_points) - 1 and any(fuzzy.mu_A2(discrete_points[j]) > 0 for j in range(i+1, len(discrete_points))):
                print(" ∪", end="")
    print(" }")
    
    print("A3 = {", end="")
    for i, x in enumerate(discrete_points):
        mu = fuzzy.mu_A3(x)
        if mu > 0:
            print(f" {mu:.1f}/{x}", end="")
            if i < len(discrete_points) - 1 and any(fuzzy.mu_A3(discrete_points[j]) > 0 for j in range(i+1, len(discrete_points))):
                print(" ∪", end="")
    print(" }")

if __name__ == "__main__":
    main()