from __future__ import print_function
from sys import stdin
import unittest

class family_tree:
    def __init__ (self, init = None):
        self.__value = self.__name = self.__parent = None
        self.__left = self.__right = None

        if init:
            try:
                for i in init:
                    self.add(i[0], i[1])
            except TypeError:
                self.add(init[0], init[0])

    def __iter__(self):
        if self.__left:
            for node in self.__left:
                yield(node)

        yield(self.__value, self.__name)

        if self.__right:
            for node in self.__right:
                yield(node)

    """ Return a preorder list """
    def preorder(self):
        result = []

        result.append(self.__name)
        if self.__left:
            result += self.__left.preorder()
        if self.__right:
            result += self.__right.preorder()
        return result


    """ Return a inorder list """
    def inorder(self):
        result = []
        if self.__left:
            result += self.__left.inorder()
        result.append(self.__name)
        if self.__right:
            result += self.__right.inorder()
        return result


    """ Return a postorder list """
    def postorder(self):
        result = []
        if self.__left:
            result += self.__left.postorder()
        if self.__right:
            result += self.__right.postorder()
        result.append(self.__name)
        return result
    def __str__(self):
        return(','.join(str(node) for node in self))

    def add(self, value, name):
        if self.__value == self.__left == self.__right == None:
            self.__value = value
            self.__name = name
            self.__parent = None
            return

        if value < self.__value:
            if not self.__left:
                self.__left = family_tree()
                self.__left.__parent = self
                self.__left.__value = value
                self.__left.__name = name
            else:
                self.__left.add(value, name)
        else:
            if not self.__right:
                self.__right = family_tree()
                self.__right.__parent = self
                self.__right.__value = value
                self.__right.__name = name
            else:
                self.__right.add(value, name)

    """ Given a value, return the node with that value. Useful in the
    next two methods """
    def __find(self, value):
        if self.__value == value: return self

        if self.__value > value:
            if self.__left:
                return self.__left.__find(value)
            else:
                raise(LookupError)

        if self.__value < value:
            if self.__right:
                return self.__right.__find(value)
            else:
                raise(LookupError)

    """ Given a value, return the name of that node's parent """
    def find_parent(self, value):
        if self.__left.__value == value or self.__right.__value == value:
            return self.__name
        elif self.__value > value:
            return self.__left.find_parent(value)
        elif self.__value < value:
            return self.__right.find_parent(value)


    """ Given a value, return the name of that node's grand parent """
    def find_grand_parent(self, value):
        if self.__value > value:
            child = self.__left
            if child.__name == self.find_parent(value):
                return self.__name
            else:
                # both child and .__left work with this line. in self .__right self.child did not work.
                return self.__left.find_grand_parent(value)
                # Below is the old code When child worked but told me unresolved reference. I dont know when it started \
                #   telling me that.
                #return self.child.find_grand_parent(value)

        elif self.__value < value:
            child = self.__right
            if child.__name == self.find_parent(value):
                return self.__name
            else:
            # Prof if you see this can you tell me why i must use self.__right instead of being
            #   able to use self.child in this return statement
                return self.__right.find_grand_parent(value)


    """ Create a list of lists, where each of the inner lists
        is a generation """
    def generations(self):
        """ First, create a list 'this_level' with the root,
                and three empty lists: 'next_level', 'result', and
                'names' """
        this_level = [self]
        next_level = []
        result = []
        names = []

        # While 'this_level' has values
        while this_level:

            # Get the first element and append its name to 'names'
            tmp = this_level.pop(0)
            names.append(tmp.__name)

            if tmp.__left:
                    next_level.append(tmp.__left)

            # Nor is this:
            if tmp.__right:
                    next_level.append(tmp.__right)

            if not this_level:
                result.append(names)
                this_level = next_level
                next_level = []
                names = []

        return result

"""
         While 'this_level' has values
             Get the first element and append its name to 'names'

             If the first element has a left, append it to 'next_level'
                Do the same for the right

             If 'this_level' is now empty
                 Append 'names' to 'result', set "this_level' to
                    'next_level', and 'next_level' and 'names' to empty
                    lists
"""
class test_family_tree (unittest.TestCase):
    """
      20
     /  \
    10  30
       /  \
      25  35
    /
    22
    """
    def test_empty(self):
        self.assertEqual(str(family_tree()), '(None, None)')

    def setUp(self):
        self.tree = family_tree([(20, "Grandpa"), (10, "Herb"), \
        (30, "Homer"),(25, "Bart"), (35, "Lisa"), (22, "Patient0")])
        self.expected = "(10, 'Herb'),(20, 'Grandpa'),(22, 'Patient0'),(25, 'Bart'),\
(30, 'Homer'),(35, 'Lisa')"

    def test_add(self):
        bt = family_tree()
        bt.add(20, "Grandpa")
        bt.add(10, "Herb")
        bt.add(30, "Homer")
        bt.add(25, "Bart")
        bt.add(35, "Lisa")
        bt.add(22, "Patient0")
        self.assertEqual(str(bt), self.expected)

    def test_init(self):
        self.assertEqual(str(self.tree), self.expected)

    def test_parent(self):
        self.assertEqual(self.tree.find_parent(35), "Homer")

    def test_parent_papi(self):
        self.assertEqual(self.tree.find_parent(10), "Grandpa")

    def test_parent_Subject0(self):
        self.assertEqual(self.tree.find_parent(22), "Bart")

    def test_grand_parent(self):
        self.assertEqual(self.tree.find_grand_parent(35), "Grandpa")

    def test_grand_parent_Patient0(self):
        self.assertEqual(self.tree.find_grand_parent(22), "Homer")

    def test_generations(self):
        self.assertEqual(self.tree.generations(), \
            [['Grandpa'], ['Herb', 'Homer'], ['Bart', 'Lisa'], ['Patient0']])

    def test_inorder(self):
        self.assertEqual(self.tree.inorder(),
        ['Herb', 'Grandpa', 'Patient0', 'Bart', 'Homer', 'Lisa'])

    def test_postorder(self):
        self.assertEqual(self.tree.postorder(), \
            ['Herb', 'Patient0', 'Bart', 'Lisa', 'Homer', 'Grandpa'])

    def test_preorder(self):
            self.assertEqual(self.tree.preorder(), \
                ['Grandpa', 'Herb', 'Homer', 'Bart', 'Patient0', 'Lisa'])
