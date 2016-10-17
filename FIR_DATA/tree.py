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

    def update_node_val(self, node_val):
        self._data = node_val

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
    def __init__(self):
        self._nodes = {}
        self._root_nodes = []  # List of ids of root nodes

    def add_node(self, node_id, parent_id, node_val=None):
        # 1. first check if node exists.  if so, we will update the node
        #    if not, create the node withough parent or children
        if node_id in self._nodes:
            new_node = self._nodes[node_id]
            self._root_nodes.remove(node_id)
            new_node.update_node_val(node_val)
        else:
            new_node = Node(node_id, node_val)
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

    def get_node(self, node_id):
        if node_id in self._nodes:
            return self._nodes[node_id]

    def get_all_roots(self):
        """ Returns a copy of the root_node list """
        return list(self._root_nodes)

    def has_node(self, node_id):
        return node_id in self._nodes
