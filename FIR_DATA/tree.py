"""
tree class for use in creating data hierarchy
"""

class Node():
    def __init__(self, key, val=None, parent_node=None, child_nodes=None):
        self._key = key
        self._data = val
        if parent_node is not None and type(parent_node) is not Node:
            raise TypeError('parent_node must be a Node')
        self._parent = parent_node
        if child_nodes is not None and type(child_nodes) is not list:
            raise TypeError('child_nodes must be a list of Nodes')
        if child_nodes:
            for child in child_nodes:
                if type(child) is not Node:
                    raise TypeError('children must be Nodes')
        self._children = child_nodes

    def is_parent(self):
        return not self._parent

    def is_leaf(self):
        return not self._children

    def get_node_data(self):
        return self._data

    def update_parent(self, parent_node):
        if type(parent_node) is not Node:
            raise TypeError('parent_node must be a Node')
        self._parent = parent_node

    def add_child(self, child_node):
        if type(child_node) is not Node:
            raise TypeError('child_node must be a Node')
        if self._children:
            self._children.append(child_node)
        else:
            self._children = [child_node]


class Tree():
    def __init__(self, root_ids=None):
        self._nodes = {}
        if root_ids and type(root_ids) is not list:
            raise TypeError('root_ids must be a list')
        for root_id in root_ids:
            self._nodes[root_id] = Node(root_id)

    def add_node(self, node_id, node_val, parent_id):
        # 1. first check if node exists.  if so, we will update the node
        #    if not, create the node withough parent or children
        if node_id in self._nodes:
            new_node = self._nodes[node_id]
        else:
            new_node = Node(node_id)
        # 2. check if parent node exists - if so, id & add new_node as child
        if parent_id in self._nodes:
            parent_node = self._nodes[parent_id]
            parent_node.add_child(new_node)
        # 3. otherwise, create parent node & add new_node as child
        else:
            parent_node = Node(parent_id, child_nodes=[new_node])
            self._nodes[parent_id] = parent_node
        # 4. update new node with parent
        new_node.update_parent(parent_node)
        # 5. add new node to Tree
        self._nodes.append(new_node)
