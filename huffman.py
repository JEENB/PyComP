from core.data import *


class Node:
    def __init__(self, symbol, freq, left=None, right=None):
        self.symbol = symbol
        self.freq = freq
        self.left = left
        self.right = right
        self.code = ''


class Huffman(Data):

    def __init__(self, symbols: list, frequency: list) -> None:
        super().__init__(symbols, frequency)
        self.huffman_table = {}
        self.leaf_nodes()

    def leaf_nodes(self):
        self.nodes = []
        for s in self.symbols:
            self.nodes.append(Node(s, self.freq_dist[s]/self.M))

    def huffman_tree(self) -> Node:
        while len(self.nodes) > 1:
            # sort all the nodes
            self.nodes = sorted(self.nodes, key=lambda x: x.freq)

            # pick smallest 2 nodes
            right: Node = self.nodes[0]
            left: Node = self.nodes[1]

            left.code = 0
            right.code = 1

            # combine the 2 smallest nodes
            newNode = Node('('+left.symbol+right.symbol+')',
                           left.freq+right.freq, left, right)
            self.nodes.remove(left)
            self.nodes.remove(right)
            self.nodes.append(newNode)

        self.root_node = self.nodes[0]  # root node
        return self.root_node

    def get_codes(self, node: Node, val='', codes={}):
        # huffman code for current node
        newVal = val + str(node.code)

        if (node.left):
            self.get_codes(node=node.left, val=newVal)
        if (node.right):
            self.get_codes(node=node.right, val=newVal)

        if (not node.left and not node.right):
            self.huffman_table[node.symbol] = newVal
        return self.huffman_table

    def encode(self, msg: list):
        root_node = self.huffman_tree()
        self.get_codes(root_node)
        encoded_val = ''
        for m in msg:
            encoded_val += self.huffman_table[m]
        return encoded_val, self.nodes[0]

    @staticmethod
    def decode(encoded_value: str, root_node: Node):
        tree_head: Node = root_node
        decoded_output = []
        for x in encoded_value:
            if x == '1':
                root_node = root_node.right
            elif x == '0':
                root_node = root_node.left
            try:
                if root_node.left.symbol == None and root_node.right.symbol == None:
                    pass
            except AttributeError:
                decoded_output.append(root_node.symbol)
                root_node = tree_head

        string = ''.join([str(item) for item in decoded_output])
        return string


h = Huffman(['a', 'b', 'c', 'd', 'e'], [0.3, 0.25, 0.2, 0.15, 0.1])
a, b = h.encode(['a', 'b', 'c', 'b', 'c', 'e'])
print(h.decode(a, b))
