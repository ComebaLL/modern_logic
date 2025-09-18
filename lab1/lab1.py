import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
import json
import os
import numpy as np
import tkinter as tk
from tkinter import filedialog

class SemanticNetworkApp:
    def __init__(self):
        self.G = nx.DiGraph()
        self.fig, self.ax = plt.subplots(figsize=(14, 10))
        plt.subplots_adjust(bottom=0.25, top=0.95)
        
        self.selected_node = None
        self.current_filename = None
        self.setup_ui()
        self.draw_network()
        
    def setup_ui(self):
        # Текстовые поля для узлов
        self.node_text = TextBox(plt.axes([0.1, 0.18, 0.15, 0.04]), 'Узел:')
        
        # Текстовые поля для связей
        self.edge_from_text = TextBox(plt.axes([0.3, 0.18, 0.1, 0.04]), 'От:')
        self.edge_to_text = TextBox(plt.axes([0.45, 0.18, 0.1, 0.04]), 'К:')
        self.relation_text = TextBox(plt.axes([0.6, 0.18, 0.1, 0.04]), 'Связь:')
        
        # Кнопки управления
        self.add_node_btn = Button(plt.axes([0.1, 0.05, 0.1, 0.06]), 'Добавить узел')
        self.add_edge_btn = Button(plt.axes([0.22, 0.05, 0.1, 0.06]), 'Добавить связь')
        self.delete_node_btn = Button(plt.axes([0.34, 0.05, 0.1, 0.06]), 'Удалить узел')
        self.clear_btn = Button(plt.axes([0.46, 0.05, 0.1, 0.06]), 'Очистить всё')
        
        # Кнопки работы с файлами
        self.save_btn = Button(plt.axes([0.58, 0.05, 0.1, 0.06]), 'Сохранить')
        self.save_as_btn = Button(plt.axes([0.70, 0.05, 0.1, 0.06]), 'Сохранить как')
        self.load_btn = Button(plt.axes([0.82, 0.05, 0.1, 0.06]), 'Загрузить')
        
        # Информационное поле
        self.info_text = TextBox(plt.axes([0.1, 0.01, 0.8, 0.03]), 'Статус:', initial='Готов к работе')
        
        # Привязка событий
        self.add_node_btn.on_clicked(self.add_node)
        self.add_edge_btn.on_clicked(self.add_edge)
        self.delete_node_btn.on_clicked(self.delete_node)
        self.clear_btn.on_clicked(self.clear_network)
        self.save_btn.on_clicked(self.save_network)
        self.save_as_btn.on_clicked(self.save_network_as)
        self.load_btn.on_clicked(self.load_network)
        
        # Привязка события клика по графику
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        
    def on_click(self, event):
        if event.inaxes == self.ax:
            # Поиск ближайшего узла
            if self.G.number_of_nodes() > 0:
                pos = nx.spring_layout(self.G)
                for node, (x, y) in pos.items():
                    if ((event.xdata - x)**2 + (event.ydata - y)**2) < 0.01:
                        self.selected_node = node
                        self.info_text.set_val(f'Выбран узел: {node}')
                        self.highlight_connections(node)
                        return
                self.selected_node = None
                self.draw_network()
        
    def highlight_connections(self, node):
        self.draw_network()
        
        if self.G.number_of_nodes() > 0:
            pos = nx.spring_layout(self.G)
            
            # Подсветка выбранного узла
            nx.draw_networkx_nodes(self.G, pos, nodelist=[node], 
                                  node_color='red', node_size=2500, ax=self.ax)
            
            # Подсветка связанных узлов
            predecessors = list(self.G.predecessors(node))
            successors = list(self.G.successors(node))
            
            if predecessors:
                nx.draw_networkx_nodes(self.G, pos, nodelist=predecessors, 
                                      node_color='orange', node_size=2200, ax=self.ax)
            
            if successors:
                nx.draw_networkx_nodes(self.G, pos, nodelist=successors, 
                                      node_color='yellow', node_size=2200, ax=self.ax)
            
            # Перерисовываем подписи связей для выделенного узла
            edge_labels = {}
            for u, v, data in self.G.edges(data=True):
                if u == node or v == node:
                    edge_labels[(u, v)] = data['relation']
            
            current_pos = nx.spring_layout(self.G)
            nx.draw_networkx_edge_labels(self.G, current_pos, edge_labels=edge_labels, 
                                        ax=self.ax, font_size=9, font_weight='bold',
                                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
            
            plt.draw()
        
    def add_node(self, event):
        node_name = self.node_text.text.strip()
        
        if node_name:
            if node_name not in self.G.nodes():
                self.G.add_node(node_name)
                self.info_text.set_val(f'Добавлен узел: {node_name}')
                self.draw_network()
            else:
                self.info_text.set_val(f'Узел {node_name} уже существует!')
        
    def add_edge(self, event):
        from_node = self.edge_from_text.text.strip()
        to_node = self.edge_to_text.text.strip()
        relation = self.relation_text.text.strip() or "связан с"
        
        if from_node and to_node:
            if from_node in self.G.nodes() and to_node in self.G.nodes():
                if not self.G.has_edge(from_node, to_node):
                    self.G.add_edge(from_node, to_node, relation=relation)
                    self.info_text.set_val(f'Добавлена связь: {from_node} → {to_node} ({relation})')
                    self.draw_network()
                else:
                    self.info_text.set_val(f'Связь уже существует!')
            else:
                self.info_text.set_val('Один из узлов не существует!')
        
    def delete_node(self, event):
        if self.selected_node:
            self.G.remove_node(self.selected_node)
            self.info_text.set_val(f'Удален узел: {self.selected_node}')
            self.selected_node = None
            self.draw_network()
        else:
            node_to_delete = self.node_text.text.strip()
            if node_to_delete in self.G.nodes():
                self.G.remove_node(node_to_delete)
                self.info_text.set_val(f'Удален узел: {node_to_delete}')
                self.draw_network()
            else:
                self.info_text.set_val('Укажите узел для удаления!')
        
    def clear_network(self, event):
        self.G.clear()
        self.selected_node = None
        self.current_filename = None
        self.info_text.set_val('Сеть очищена')
        self.draw_network()
        
    def save_network(self, event):
        if self.current_filename:
            self._save_to_file(self.current_filename)
        else:
            self.save_network_as(event)
        
    def save_network_as(self, event):
        root = tk.Tk()
        root.withdraw()  # Скрываем основное окно Tkinter
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Сохранить семантическую сеть как"
        )
        
        root.destroy()
        
        if filename:
            self.current_filename = filename
            self._save_to_file(filename)
        
    def _save_to_file(self, filename):
        try:
            data = {
                'nodes': list(self.G.nodes(data=True)),
                'edges': list(self.G.edges(data=True))
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.info_text.set_val(f'Сеть сохранена в {os.path.basename(filename)}')
        except Exception as e:
            self.info_text.set_val(f'Ошибка сохранения: {str(e)}')
        
    def load_network(self, event):
        root = tk.Tk()
        root.withdraw()  # Скрываем основное окно Tkinter
        
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Загрузить семантическую сеть"
        )
        
        root.destroy()
        
        if filename:
            self._load_from_file(filename)
        
    def _load_from_file(self, filename):
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.G.clear()
                
                # Загрузка узлов
                for node_data in data['nodes']:
                    if isinstance(node_data, list) and len(node_data) == 2:
                        node, attrs = node_data
                        self.G.add_node(node, **attrs)
                    else:
                        # Для обратной совместимости со старым форматом
                        self.G.add_node(node_data)
                
                # Загрузка связей
                for edge_data in data['edges']:
                    if isinstance(edge_data, list) and len(edge_data) == 3:
                        from_node, to_node, attrs = edge_data
                        self.G.add_edge(from_node, to_node, **attrs)
                    else:
                        # Для обратной совместимости
                        from_node, to_node = edge_data
                        self.G.add_edge(from_node, to_node, relation="связан с")
                
                self.current_filename = filename
                self.info_text.set_val(f'Сеть загружена из {os.path.basename(filename)}')
                self.draw_network()
            else:
                self.info_text.set_val(f'Файл не найден!')
        except Exception as e:
            self.info_text.set_val(f'Ошибка загрузки: {str(e)}')
    
    def optimize_edge_label_positions(self, pos, edge_labels):
        """Оптимизация позиций надписей связей чтобы не перекрывались"""
        optimized_positions = {}
        
        for (u, v), label in edge_labels.items():
            if u in pos and v in pos:
                x1, y1 = pos[u]
                x2, y2 = pos[v]
                
                # Позиция посередине связи
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                
                # Смещение перпендикулярно линии связи
                dx = x2 - x1
                dy = y2 - y1
                length = np.sqrt(dx**2 + dy**2)
                
                if length > 0:
                    # Нормализованный перпендикулярный вектор
                    perp_x = -dy / length
                    perp_y = dx / length
                    
                    # Смещение на фиксированное расстояние
                    offset = 0.1
                    optimized_positions[(u, v)] = (mid_x + perp_x * offset, mid_y + perp_y * offset)
                else:
                    optimized_positions[(u, v)] = (mid_x, mid_y)
        
        return optimized_positions
        
    def draw_network(self):
        self.ax.clear()
        
        if self.G.number_of_nodes() == 0:
            # self.ax.text(0.5, 0.5, 'Добавьте узлы и связи\n\n'
            
            # Показываем текущий файл если есть
            if self.current_filename:
                file_info = f'\n\nТекущий файл: {os.path.basename(self.current_filename)}'
                self.ax.text(0.5, 0.1, file_info, ha='center', va='center', fontsize=10, color='blue')
            
            plt.draw()
            return
        
        # Позиционирование узлов
        pos = nx.spring_layout(self.G, k=3, iterations=100)
        
        # Все узлы одного цвета
        node_colors = ['lightblue'] * len(self.G.nodes())
        
        # Рисуем узлы
        nx.draw_networkx_nodes(self.G, pos, node_color=node_colors, 
                              node_size=2000, ax=self.ax, alpha=0.8)
        
        # Рисуем подписи узлов
        nx.draw_networkx_labels(self.G, pos, ax=self.ax, font_size=10)
        
        # Рисуем связи
        nx.draw_networkx_edges(self.G, pos, ax=self.ax, 
                              arrowstyle='->', arrowsize=20, 
                              edge_color='gray', width=2)
        
        # Подписи связей с оптимизацией позиций
        edge_labels = {(u, v): d['relation'] for u, v, d in self.G.edges(data=True)}
        
        # Оптимизируем позиции надписей
        label_pos = self.optimize_edge_label_positions(pos, edge_labels)
        
        # Рисуем подписи связей
        for (u, v), label in edge_labels.items():
            if (u, v) in label_pos:
                x, y = label_pos[(u, v)]
                self.ax.text(x, y, label, 
                            ha='center', va='center',
                            fontsize=9, fontweight='bold',
                            bbox=dict(boxstyle='round,pad=0.3', 
                                     facecolor='white', 
                                     edgecolor='gray', 
                                     alpha=0.9))
        
        # Настройка внешнего вида
        title = 'Семантическая сеть'
        if self.current_filename:
            title += f' - {os.path.basename(self.current_filename)}'
        self.ax.set_title(title, fontsize=16, pad=20)
        self.ax.axis('off')
        
        # Информация о сети
        stats_text = f'Узлов: {self.G.number_of_nodes()} | Связей: {self.G.number_of_edges()}'
        self.ax.text(0.02, 0.98, stats_text, transform=self.ax.transAxes, 
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.draw()

# Запуск приложения
if __name__ == "__main__":
    app = SemanticNetworkApp()
    plt.show()