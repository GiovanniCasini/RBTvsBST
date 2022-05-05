import sys
import numpy
import time
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.p = None

    def get_children(self):
        children = []
        if self.left is not None:
            children.append(self.left)
            left_child = self.left.key
        else:
            left_child = None
        if self.right is not None:
            children.append(self.right)
            right_child = self.right.key
        else:
            right_child = None
        print(self.key, " l: ", left_child, " r: ", right_child)
        return children


class BST:
    def __init__(self, root):
        self.root = root

    def insert_node(self, node):
        y = None
        x = self.root
        while x is not None and x.key is not None:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right
        node.p = y
        if y is None and self.root is None:
            self.root = node
        elif node.key < y.key:
            node.p.left = node
        else:
            node.p.right = node

    def search(self, x, key):
        if x is None:
            return print(key, " NOT FOUND")
        if key == x.key:
            print(x.key, " FOUND")
            return x
        if key < x.key:
            return self.search(x.left, key)
        else:
            return self.search(x.right, key)

    def iterative_search(self, x, key):
        while x is not None and x.key != key:
            if key < x.key:
                x = x.left
            else:
                x = x.right
        if x is None:
            return print(key, " NOT FOUND")
        else:
            print(x.key, " FOUND")
            return x

    def tree_minimum(self, x):
        while x.left is not None:
            x = x.left
        # print(x.key, " MINIMUM")
        return x

    def tree_maximum(self, x):
        while x.right is not None:
            x = x.right
        # print(x.key, " MAXIMUM")
        return x

    def tree_successor(self, x):
        if x.right is not None:
            return self.tree_minimum(x.right)
        y = x.p
        while y is not None and x == y.right:
            x = y
            y = y.p
        return y

    def transplant(self, u, v):
        if u.p is None:
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        if v is not None:
            v.p = u.p

    def delete_node(self, z):
        if z.left is None:
            self.transplant(z, z.right)
        elif z.right is None:
            self.transplant(z, z.left)
        else:
            y = self.tree_minimum(z.right)
            if y.p != z:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.p = y
            self.transplant(z, y)
            y.left = z.left
            y.left.p = y

    def inorder_tree_walk(self, x):
        if x is not None:
            self.inorder_tree_walk(x.left)
            print(x.key)
            self.inorder_tree_walk(x.right)

    def inorder_tree_walk_root(self):
        x = self.root
        if x is not None:
            self.inorder_tree_walk(x.left)
            print(x.key)
            self.inorder_tree_walk(x.right)

    def preorder_tree_walk(self, x):
        if x is not None:
            print(x.key)
            self.preorder_tree_walk(x.left)
            self.preorder_tree_walk(x.right)

    def postorder_tree_walk(self, x):
        if x is not None:
            self.postorder_tree_walk(x.left)
            self.postorder_tree_walk(x.right)
            print(x.key)


class NodeRBT(Node):
    def __init__(self, key):
        Node.__init__(self, key)
        self.color = None


class RBT:
    def __init__(self, root):
        if root is not None:
            self.root = NodeRBT(root.key)
            self.root.color = 'BLACK'
        else:
            self.root = None
        self.nil = None

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.p = x
        y.p = x.p
        if x.p == self.nil:
            self.root = y
        elif x == x.p.left:
            x.p.left = y
        else:
            x.p.right = y
        y.left = x
        x.p = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.p = x
        y.p = x.p
        if x.p == self.nil:
            self.root = y
        elif x == x.p.right:
            x.p.right = y
        else:
            x.p.left = y
        y.right = x
        x.p = y

    def insert_node_rb(self, z1):
        z = NodeRBT(z1.key)
        y = None
        x = self.root
        while x is not None and x.key is not None:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.p = y
        if y is None:
            self.root = z
            z.p = self.nil
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.left = self.nil
        z.right = self.nil
        z.color = 'RED'
        self.insert_node_rb_fixup(z)

    def insert_node_rb_fixup(self, z):
        while z.p != self.nil and z.p.color == 'RED':
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y is not None and y.color == 'RED':
                    z.p.color = 'BLACK'
                    y.color = 'BLACK'
                    z.p.p.color = 'RED'
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self.left_rotate(z)
                    z.p.color = 'BLACK'
                    z.p.p.color = 'RED'
                    self.right_rotate(z.p.p)
            else:
                y = z.p.p.left
                if y is not None and y.color == 'RED':
                    z.p.color = 'BLACK'
                    y.color = 'BLACK'
                    z.p.p.color = 'RED'
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self.right_rotate(z)
                    z.p.color = 'BLACK'
                    z.p.p.color = 'RED'
                    self.left_rotate(z.p.p)
        self.root.color = 'BLACK'

    def inorder_tree_walk(self, x):
        if x is not None:
            self.inorder_tree_walk(x.left)
            print(x.key, x.color)
            self.inorder_tree_walk(x.right)

    def inorder_tree_walk_root(self):
        x = self.root
        if x is not None:
            self.inorder_tree_walk(x.left)
            print(x.key, x.color)
            self.inorder_tree_walk(x.right)

    def preorder_tree_walk(self, x):
        if x is not None:
            print(x.key, x.color)
            self.inorder_tree_walk(x.left)
            self.inorder_tree_walk(x.right)

    def postorder_tree_walk(self, x):
        if x is not None:
            self.inorder_tree_walk(x.left)
            self.inorder_tree_walk(x.right)
            print(x.key, x.color)


nValues = 10
maxTime = 3
keys_array = []
for i in range(0, 7):
    keys_array.append(numpy.random.randint(0, sys.maxsize, nValues))
    nValues *= 10

execTimeBSTRandom = []
execTimeBSTInOrder = []
execTimeRBTRandom = []
execTimeRBTInOrder = []

executionTime = 0
run = 0
nValues = 10
while executionTime < maxTime:
    nodes = []
    bst = BST(None)
    # keys = numpy.random.randint(0, 1000000, nValues)
    keys = keys_array[run]
    for i in range(0, nValues):
        nodes.append(Node(keys[i]))
    startTime = time.time()
    for i in range(0, nValues):
        bst.insert_node(nodes[i])
    endTime = time.time()
    executionTime = endTime - startTime
    execTimeBSTRandom.append(executionTime)
    print("BST Random inserted ", nValues, " in ", executionTime)
    nValues *= 10
    run += 1

print("--------------------------------------")
executionTime = 0
nValues = 10
while executionTime < maxTime:
    nodes = []
    bst = BST(None)
    for i in range(0, nValues):
        nodes.append(Node(i+1))
    startTime = time.time()
    for i in range(0, nValues):
        bst.insert_node(nodes[i])
    endTime = time.time()
    executionTime = endTime - startTime
    execTimeBSTInOrder.append(executionTime)
    print("BST InOrder inserted ", nValues, " in ", executionTime)
    nValues *= 10

print("--------------------------------------")
executionTime = 0
nValues = 10
run = 0
while executionTime < maxTime:
    nodes = []
    rbt = RBT(None)
    # keys = numpy.random.randint(0, 1000000, nValues)
    keys = keys_array[run]
    for i in range(0, nValues):
        nodes.append(NodeRBT(keys[i]))
    startTime = time.time()
    for i in range(0, nValues):
        rbt.insert_node_rb(nodes[i])
    endTime = time.time()
    executionTime = endTime - startTime
    execTimeRBTRandom.append(executionTime)
    print("RBT Random inserted ", nValues, " in ", executionTime)
    nValues *= 10
    run += 1

print("--------------------------------------")
nValues = 10
executionTime = 0
while executionTime < maxTime:
    nodes = []
    rbt = RBT(None)
    for i in range(0, nValues):
        nodes.append(NodeRBT(i))
    startTime = time.time()
    for i in range(0, nValues):
        rbt.insert_node_rb(nodes[i])
    endTime = time.time()
    executionTime = endTime - startTime
    execTimeRBTInOrder.append(executionTime)
    print("RBT InOrder inserted ", nValues, " in ", executionTime)
    nValues *= 10

x = []
plt.xscale("log")
plt.yscale("log")
plt.ylim(0.000001, 10)
for i in range(1, len(execTimeBSTRandom)+1):
    x.append(10**i)
plt.plot(x, execTimeBSTRandom, 'o-')
x = []
for i in range(1, len(execTimeBSTInOrder)+1):
    x.append(10**i)
plt.plot(x, execTimeBSTInOrder, 'o-')
plt.title("Inserimento randomico e ordinato per BST")
plt.xlabel("Numero elementi")
plt.ylabel("Tempo (s)")
plt.legend(["Randomico", "Ordinato"])
plt.show()

plt.xscale("log")
plt.yscale("log")
plt.ylim(0.00001, 10)
x = []
for i in range(1, len(execTimeRBTRandom)+1):
    x.append(10**i)
plt.plot(x, execTimeRBTRandom, 'o-')
x = []
for i in range(1, len(execTimeRBTInOrder)+1):
    x.append(10**i)
plt.plot(x, execTimeRBTInOrder, 'o-')
plt.title("Inserimento randomico e ordinato per RBT")
plt.xlabel("Numero elementi")
plt.ylabel("Tempo (s)")
plt.legend(["Randomico", "Ordinato"])
plt.show()

# CONFRONTI

x = []
plt.xscale("log")
plt.yscale("log")
plt.ylim(0.000001, 10)
for i in range(1, len(execTimeBSTRandom)+1):
    x.append(10**i)
plt.plot(x, execTimeBSTRandom, 'o-')
x = []
for i in range(1, len(execTimeRBTRandom)+1):
    x.append(10**i)
plt.plot(x, execTimeRBTRandom, 'o-')
plt.title("Confronto inserimento randomico tra BST e RBT")
plt.xlabel("Numero elementi")
plt.ylabel("Tempo (s)")
plt.legend(["BST", "RBT"])
plt.show()

x = []
plt.xscale("log")
plt.yscale("log")
plt.ylim(0.000001, 10)
for i in range(1, len(execTimeBSTInOrder)+1):
    x.append(10**i)
plt.plot(x, execTimeBSTInOrder, 'o-')
x = []
for i in range(1, len(execTimeRBTInOrder)+1):
    x.append(10**i)
plt.plot(x, execTimeRBTInOrder, 'o-')
plt.title("Confronto inserimento ordinato tra BST e RBT")
plt.xlabel("Numero elementi")
plt.ylabel("Tempo (s)")
plt.legend(["BST", "RBT"])
plt.show()
