import networkx as nx
import os
import config
# Load the GraphML file
BASE_PATH = config.DATA_PATH

def load_law_tree(law_type):
    assert law_type in ['AI_ACT', 'GDPR', 'HIPAA'], f"Unsupported law type: {law_type}"
    file_path = os.path.join(BASE_PATH, 'law_tree',f'LawTree_{law_type}.graphml')
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    G = nx.read_graphml(file_path)
    return G


if __name__ == "__main__":
    # Example usage
    try:
        law_tree = load_law_tree('GDPR')
        print("Law tree loaded successfully.")
    except Exception as e:
        print(f"Error loading law tree: {e}")