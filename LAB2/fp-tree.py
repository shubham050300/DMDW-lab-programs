import csv


# def load_data() :
#   dset = []
#   with open('test_dataset_1.csv') as csv_file:
#       csv_reader = csv.reader(csv_file, delimiter=',')
#       for row in csv_reader:
#           dset.append(row)
#   return dset

def load_data() :
    dset = []
    with open('retail_dataset.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0 :
                dset.append(row)
            line_count += 1
    return dset

def find_frequent_itemsets(transactions, minimum_support):

    items={}
    for i in range(len(transactions)):
        for j in range(len(transactions[i])):
            if(transactions[i][j] not in items.keys()):
                items[transactions[i][j]]=1
            else:
                items[transactions[i][j]]+=1

    # Remove infrequent items from the item support dictionary
    items = dict((item, support) for item, support in items.items() if support >= minimum_support)

    #sort in decreasing order and remove infrequent items
    def clean_transaction(transaction):
        transaction = filter(lambda v: v in items, transaction)
        transaction = sorted(transaction, key=lambda v: items[v], reverse=True)
        return transaction

    master = FPTree()
    print("Constructing the tree")
    for transaction in map(clean_transaction, transactions):
        master.add(transaction)

    def find_with_suffix(tree, suffix):
        for item, nodes in tree.items():
            support = sum(n.count for n in nodes)
            if support >= minimum_support and item not in suffix:
                found_set = [item] + suffix
                yield (found_set, support)

                # Build a conditional tree and '''recursively''' search for frequent
                # itemsets within it.
                cond_tree = conditional_tree_from_paths(tree.prefix_paths(item))
                for s in find_with_suffix(cond_tree, found_set):
                    yield s

    for itemset in find_with_suffix(master, []):
        yield itemset

from collections import namedtuple

class FPTree(object):

    Route = namedtuple('Route', 'head tail')
    def __init__(self):
        self._root = FPNode(self, None, None)
        self._routes = {}

    @property
    def root(self):
        """The root node of the tree."""
        return self._root

    def add(self, transaction):
        """Add a transaction to the tree."""
        point = self._root

        for item in transaction:
            next_point = point.search(item)
            if next_point:

                next_point.increment()
            else:

                next_point = FPNode(self, item)
                point.add(next_point)

                self._update_route(next_point)

            point = next_point

    def _update_route(self, point):
        """Add the given node to the route through all nodes for its item."""
        assert self is point.tree

        try:
            route = self._routes[point.item]
            route[1].neighbor = point # route[1] is the tail
            self._routes[point.item] = self.Route(route[0], point)
        except KeyError:
            # First node for this item; start a new route.
            self._routes[point.item] = self.Route(point, point)

    def items(self):
        for item in self._routes.keys():
            yield (item, self.nodes(item))

    def nodes(self, item):

        try:
            node = self._routes[item][0]
        except KeyError:
            return

        while node:
            yield node
            node = node.neighbor

    def prefix_paths(self, item):
        """Generate the prefix paths that end with the given item."""

        def collect_path(node):
            path = []
            while node and not node.root:
                path.append(node)
                node = node.parent
            path.reverse()
            return path

        return (collect_path(node) for node in self.nodes(item))

def conditional_tree_from_paths(paths):
    """Build a conditional FP-tree from the given prefix paths."""
    tree = FPTree()
    condition_item = None
    items = set()

    for path in paths:
        if condition_item is None:
            condition_item = path[-1].item

        point = tree.root
        for node in path:
            next_point = point.search(node.item)
            if not next_point:
                # Add a new node to the tree.
                items.add(node.item)
                count = node.count if node.item == condition_item else 0
                next_point = FPNode(tree, node.item, count)
                point.add(next_point)
                tree._update_route(next_point)
            point = next_point

    assert condition_item is not None

    # Calculate the counts of the non-leaf nodes.
    for path in tree.prefix_paths(condition_item):
        count = path[-1].count
        for node in reversed(path[:-1]):
            node._count += count

    return tree

class FPNode(object):

    def __init__(self, tree, item, count=1):
        self._tree = tree
        self._item = item
        self._count = count
        self._parent = None
        self._children = {}
        self._neighbor = None

    def add(self, child):
        """Add the given FPNode `child` as a child of this node."""

        if not isinstance(child, FPNode):
            raise TypeError("Can only add other FPNodes as children")

        if not child.item in self._children:
            self._children[child.item] = child
            child.parent = self

    def search(self, item):
        try:
            return self._children[item]
        except KeyError:
            return None

    def __contains__(self, item):
        return item in self._children

    @property
    def tree(self):
        return self._tree

    @property
    def item(self):
        return self._item

    @property
    def count(self):
        return self._count

    def increment(self):
        if self._count is None:
            raise ValueError("Root nodes have no associated count.")
        self._count += 1

    @property
    def root(self):
        return self._item is None and self._count is None

    @property
    def leaf(self):
        return len(self._children) == 0

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def neighbor(self):

        return self._neighbor

    @neighbor.setter
    def neighbor(self, value):
        self._neighbor = value



if __name__ == '__main__':

    minsup=3000
    transactions = load_data()

    result = []
    for itemset, support in find_frequent_itemsets(transactions, minsup):
        result.append((itemset,support))

    result = sorted(result, key=lambda i: i[1])
    for itemset, support in result:
        print (str(itemset).ljust(20) + ': ' + str(support))