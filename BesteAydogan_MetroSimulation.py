import heapq
import collections
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.widgets import Button
import sys

class Station:
    def __init__(self, name, x=0, y=0):
        self.name = name
        self.neighbors = []  # List of (neighbor_station, transfer_time, travel_time) tuples
        self.x = x
        self.y = y

    def add_neighbor(self, neighbor, transfer_time=0, travel_time=1):
        self.neighbors.append((neighbor, transfer_time, travel_time))

class MetroNetwork:
    def __init__(self):
        self.stations = {}
        self.current_figure = None

    def add_station(self, name, x=0, y=0):
        if name not in self.stations:
            self.stations[name] = Station(name, x, y)

    def add_connection(self, name1, name2, transfer_time=0, travel_time=1):
        self.add_station(name1)
        self.add_station(name2)
        self.stations[name1].add_neighbor(self.stations[name2], transfer_time, travel_time)
        self.stations[name2].add_neighbor(self.stations[name1], transfer_time, travel_time)

    def bfs(self, start_name, goal_name):
        """
        Finds a path with the minimum number of transfers using Breadth-First Search.
        """
        start = self.stations.get(start_name)
        goal = self.stations.get(goal_name)
        if not start or not goal:
            return None  # Handle case where start or goal station doesn't exist

        queue = collections.deque([(start, [start])])  # (current_station, path_so_far)
        visited = {start}  # Use a set for efficient membership checking

        while queue:
            current, path = queue.popleft()
            if current == goal:
                return [station.name for station in path]  # Return path as station names

            for neighbor, _, _ in current.neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None  # No path found

    def a_star(self, start_name, goal_name):
        start = self.stations.get(start_name)
        goal = self.stations.get(goal_name)
        if not start or not goal:
            return None, float('inf')

        def heuristic(a, b):
            return abs(a.x - b.x) + abs(a.y - b.y)

        queue = [(0, start, [start], 0)]  # (f_score, current_station, path_so_far, g_score)
        visited = set()

        while queue:
            f_score, current, path, g_score = heapq.heappop(queue)
            if current == goal:
                return [station.name for station in path], g_score

            visited.add(current)
            for neighbor, transfer_time, travel_time in current.neighbors:
                if neighbor not in visited:
                    g_score_new = g_score + travel_time + transfer_time
                    h_score = heuristic(neighbor, goal)
                    f_score_new = g_score_new + h_score
                    heapq.heappush(queue, (f_score_new, neighbor, path + [neighbor], g_score_new))

        return None, float('inf')
    
    def exit_program(self, event):
        """Exit butonu için callback fonksiyonu"""
        plt.close('all')  # Tüm açık pencereleri kapat
        print("Program kapatılıyor...")
        sys.exit(0)  # Programdan çık
        
    def visualize(self, path=None):
        """
        Ağı görselleştirir ve isteğe bağlı olarak belirtilen yolu vurgular.
        path: İstasyon adlarından oluşan liste (yol)
        """
        # Yeni şekil oluştur
        self.current_figure = plt.figure(figsize=(12, 10))
        
        G = nx.Graph()
        
        # İstasyonları ekle
        for name, station in self.stations.items():
            # Eğer x ve y koordinatları 0 ise, rastgele koordinat atayalım
            if station.x == 0 and station.y == 0:
                station.x = np.random.random() * 10
                station.y = np.random.random() * 10
            G.add_node(name, pos=(station.x, station.y))
        
        # Bağlantıları ekle
        for name, station in self.stations.items():
            for neighbor, transfer_time, travel_time in station.neighbors:
                G.add_edge(name, neighbor.name, transfer=transfer_time, travel=travel_time, 
                          weight=travel_time+transfer_time)
        
        # Ana grafik için alan oluştur
        graph_ax = plt.axes([0.05, 0.1, 0.9, 0.8])
        
        # Exit butonu için alan oluştur (altta)
        button_ax = plt.axes([0.8, 0.02, 0.15, 0.05])
        button = Button(button_ax, 'Programı Kapat', color='lightcoral', hovercolor='red')
        button.on_clicked(self.exit_program)
        
        # Ana grafiği çiz
        plt.sca(graph_ax)
        
        # Düğüm pozisyonlarını al
        pos = nx.get_node_attributes(G, 'pos')
        
        # Varsayılan olarak tüm kenarları çiz
        nx.draw_networkx_edges(G, pos, alpha=0.5, width=1.0)
        
        # Yol varsa, yoldaki kenarları vurgula
        if path and len(path) > 1:
            path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=3.0)
        
        # Düğümleri çiz
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='skyblue')
        
        # Düğüm etiketlerini çiz
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
        
        # Kenarlardaki ağırlıkları etiket olarak göster
        edge_labels = {(u, v): f"T:{d['travel']} Tr:{d['transfer']}" 
                      for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
        
        plt.title("Metro Ağı Görselleştirmesi")
        graph_ax.set_axis_off()  # Eksenleri gizle
        plt.tight_layout()
        plt.show()
        
    def visualize_path_comparison(self, start, goal):
        """
        BFS ve A* algoritmaları tarafından bulunan yolları karşılaştırmalı olarak görselleştirir.
        """
        # BFS ve A* ile yolları bul
        bfs_path = self.bfs(start, goal)
        a_star_path, a_star_cost = self.a_star(start, goal)
        
        # Yeni şekil oluştur
        self.current_figure = plt.figure(figsize=(20, 10))
        
        # İki grafik için alan oluştur
        ax1 = plt.subplot(1, 2, 1)
        ax2 = plt.subplot(1, 2, 2)
        
        # Exit butonu için alan oluştur (altta)
        button_ax = plt.axes([0.8, 0.02, 0.15, 0.05])
        button = Button(button_ax, 'Programı Kapat', color='lightcoral', hovercolor='red')
        button.on_clicked(self.exit_program)
        
        G = nx.Graph()
        
        # İstasyonları ekle
        for name, station in self.stations.items():
            # Eğer x ve y koordinatları 0 ise rastgele atama
            if station.x == 0 and station.y == 0:
                station.x = np.random.random() * 10
                station.y = np.random.random() * 10
            G.add_node(name, pos=(station.x, station.y))
        
        # Bağlantıları ekle
        for name, station in self.stations.items():
            for neighbor, transfer_time, travel_time in station.neighbors:
                G.add_edge(name, neighbor.name, transfer=transfer_time, travel=travel_time, 
                          weight=travel_time+transfer_time)
        
        # Düğüm pozisyonlarını al
        pos = nx.get_node_attributes(G, 'pos')
        
        # BFS yolunu çiz
        plt.sca(ax1)
        nx.draw_networkx_edges(G, pos, alpha=0.3, width=1.0, ax=ax1)
        
        if bfs_path and len(bfs_path) > 1:
            path_edges = [(bfs_path[i], bfs_path[i+1]) for i in range(len(bfs_path)-1)]
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='blue', width=3.0, ax=ax1)
        
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='skyblue', ax=ax1)
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold', ax=ax1)
        
        ax1.set_title(f"BFS Yolu: {start} -> {goal}\nYol: {bfs_path}")
        ax1.set_axis_off()
        
        # A* yolunu çiz
        plt.sca(ax2)
        nx.draw_networkx_edges(G, pos, alpha=0.3, width=1.0, ax=ax2)
        
        if a_star_path and len(a_star_path) > 1:
            path_edges = [(a_star_path[i], a_star_path[i+1]) for i in range(len(a_star_path)-1)]
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3.0, ax=ax2)
        
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='skyblue', ax=ax2)
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold', ax=ax2)
        
        ax2.set_title(f"A* Yolu: {start} -> {goal}\nYol: {a_star_path}, Maliyet: {a_star_cost}")
        ax2.set_axis_off()
        
        plt.tight_layout()
        plt.show()

# Ana program - Metro ağını oluştur
def main():
    # Metro ağını oluştur
    metro = MetroNetwork()
    metro.add_connection("A", "B", travel_time=2)
    metro.add_connection("B", "C", transfer_time=1, travel_time=3)
    metro.add_connection("C", "D", travel_time=4)
    metro.add_connection("A", "D", travel_time=5)
    metro.add_station("E", x=10, y=10)
    metro.add_station("F", x=20, y=20) 
    metro.add_connection("D", "E", travel_time=2)
    metro.add_connection("E", "F", travel_time=6)

    # Test durumları
    test_cases = [("A", "F"), ("A", "C"), ("B", "E"), ("A", "A"), ("X", "F")]  # Added test cases

    # Önce BFS ve A* sonuçlarını yazdır
    for start, goal in test_cases:
        bfs_path = metro.bfs(start, goal)
        print(f"BFS Path from {start} to {goal}: {bfs_path}")

        a_star_path, a_star_cost = metro.a_star(start, goal)
        print(f"A* Path from {start} to {goal}: {a_star_path}, Cost: {a_star_cost}")
        print("-" * 20)

    # Metro ağını görselleştir (genel görünüm)
    metro.visualize()

    # Her test durumu için karşılaştırmalı görselleştirme yap
    for start, goal in test_cases:
        if start in metro.stations and goal in metro.stations:
            print(f"{start} ve {goal} arasındaki yolları görselleştirme:")
            metro.visualize_path_comparison(start, goal)

# Eğer bu script direkt çalıştırılıyorsa
if __name__ == "__main__":
    main()