"""
tree class for use in creating data hierarchy
"""

class Node():
    def __init__(self, key, desc=None, val=None,
                 parent_node=None, child_nodes=None):
        self._key = key
        self._decription = desc
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

    def update_val(self, node_val):
        self._data = node_val

    def update_description(self, new_desc):
        self._description = new_desc

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

    def node_key(self):
        return self._key

    def node_description(self):
        return self._description

    def node_val(self):
        return self._data

    def parent_key(self):
        return self._parent.node_key() if self._parent else None

    def get_children(self):
        return self._children

    def child_keys(self):
        if self._children:
            child_id_list = []
            for child in self._children:
                child_id_list.append(child.node_key())
            return child_id_list
        return None


class Tree():
    def __init__(self):
        self._nodes = {}
        self._root_nodes = []  # List of ids of root nodes

    def add_node(self, node_id, parent_id, node_val=None, node_desc=None):
        """
        Adds new node to tree
        Adds new node as child of parent node (creates parent if needed)
        :param node_id: id for new node
        :param parent_id: id of new node's parent (required)
        :param node_val (optional): Node value
        :param node_desc (optional): Human-friendly description of node
        """
        # 1. first check if node exists.  if so, we will update the node
        #    if not, create the node withough parent or children
        if node_id in self._nodes:
            new_node = self._nodes[node_id]
            self._root_nodes.remove(node_id)
            new_node.update_val(node_val)
            if node_desc:
                new_node.update_description(node_desc)
        else:
            new_node = Node(node_id, val=node_val, desc=node_desc)
        # 2. check if parent node exists - if so, id & add new_node as child
        if parent_id in self._nodes:
            parent_node = self._nodes[parent_id]
            parent_node.add_child(new_node)
        # 3. otherwise, create parent node & add new_node as child
        else:
            parent_node = Node(parent_id, child_nodes=[new_node])
            self._nodes[parent_id] = parent_node
            self._root_nodes.append(parent_id)
        # 4. update new node with parent
        new_node.update_parent(parent_node)
        # 5. add new node to Tree
        self._nodes[node_id] = new_node

    def get_node(self, node_id):
        """Returns a specific node from the tree"""
        if node_id in self._nodes:
            return self._nodes[node_id]

    def root_nodes(self):
        """ Returns a copy of the root_node list """
        return list(self._root_nodes)

    def has_node(self, node_id):
        """Returns bookean indicating whether a given node_id is in tree"""
        return node_id in self._nodes

    def update_node_val(self, node_id, new_val):
        """
        Updates the value of a given node
        :param node_id: id of node to update
        :param new_val: value to set for node
        """
        self._nodes[node_id].update_val(new_val)

    def copy_tree(self):
        """returns a copy of the tree"""
        tree_copy = Tree()
        for old_node in self._nodes.values():
            if old_node.parent_key() is not None:  # don't add root nodes here
                tree_copy.add_node(old_node.node_key(), old_node.parent_key())
        return tree_copy

    def traverse_tree(self, node_id):
        """
        Returns an iterator for every node in a tree starting with given root
        Explores each branch to a leaf node & for leaf only, returns value
        :param node_id: id of node to use as starting root
        :returns tba: tbd
        """
        pass
