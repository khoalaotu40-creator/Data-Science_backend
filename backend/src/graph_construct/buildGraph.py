'''
Xử lý lưu trữ vào Graph Database
'''
import networkx as nx
import os

class KnowledgeGraphBuilder:
    def __init__(self):
        # Sử dụng DiGraph (Directed Graph) vì quan hệ pháp luật thường có hướng 
        # (VD: A -> phạt -> B)
        self.graph = nx.DiGraph() 

    def add_data(self, extraction_data: dict):
        """Thêm nodes và edges vào đồ thị từ dữ liệu dictionary"""
        nodes = extraction_data.get("nodes", [])
        edges = extraction_data.get("edges", [])

        # Thêm Nodes
        for node in nodes:
            node_id = node.get("id")
            if node_id:
                # NetworkX tự động xử lý trùng lặp (deduplication) dựa trên ID
                self.graph.add_node(node_id, label=node.get("label", ""))

        # Thêm Edges
        for edge in edges:
            source = edge.get("source")
            target = edge.get("target")
            relation = edge.get("relation")
            
            if source and target and source in self.graph and target in self.graph:
                self.graph.add_edge(source, target, relation=relation)

    def save_graph(self, output_dir: str, filename="knowledge_graph.graphml"):
        """Lưu đồ thị ra file .graphml (Có thể mở bằng phần mềm Gephi)"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        filepath = os.path.join(output_dir, filename)
        nx.write_graphml(self.graph, filepath)
        print(f"Đã lưu đồ thị GraphRAG tại: {filepath}")
        print(f"Tổng số Nodes: {self.graph.number_of_nodes()}")
        print(f"Tổng số Edges: {self.graph.number_of_edges()}")
        
    def get_graph(self):
        return self.graph