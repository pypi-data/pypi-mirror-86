#!/usr/bin/env python3
# -*- coding: future_fstrings -*-
"""
Usage:
    
    ## for genomic or other data with span-like data structures (chromsome, start, stop).
    # chromosome could be set to the same for other non-genomic span data. 
    
    from RBTree import RBDict
    # 2010-1-26 RBDict is more efficiency than binary_tree.
    rbDict = RBDict(cmpfn=leftWithinRightAlsoEqualCmp)
    for segment in segment_ls:
        chromosome, start, stop = segment[:3]
        segmentKey = CNVSegmentBinarySearchTreeKey(chromosome=chromosome,
            span_ls=[start, stop], \
            min_reciprocal_overlap=min_reciprocal_overlap)
        rbDict[segmentKey] = segment
    
    ## keys that are easier to be hashed and compared
    rbDict = RBDict()
    key1 = 0.5
    individual1 = "1978001"
    rbDict[key1] = individual1
    
    for rbNode in rbDict:
        print rbNode.key
        print rbNode.value


2010-1-26 downloaded from http://newcenturycomputers.net/projects/rbtree.html
#
# This code adapted from C source from
# Thomas Niemann's Sorting and Searching Algorithms: A Cookbook
#
# From the title page:
#	Permission to reproduce this document, in whole or in part, is
#	given provided the original web site listed below is referenced,
#	and no additional restrictions apply. Source code, when part of
#	a software project, may be used freely without reference to the
#	author.
#
# Adapted by Chris Gonnerman <chris.gonnerman@newcenturycomputers.net>
#   and Graham Breed
#
# Updated by Charles Tolman <ct@acm.org>
#   inheritance from object class
#   added RBTreeIter class
#   added lastNode and prevNode routines to RBTree
#   added RBList class and associated tests
#
# Updated by Stefan Fruhner <marycue@gmx.de>
#       Added item count to RBNode, which counts the occurence
#       of objects. The tree is kept unique, but insertions 
#       of the same object are counted
#       changed RBList.count():  returns the number of occurences of 
#                                an item
#       Renamed RBList.count to RBList.elements, because of a name 
#       mismatch with RBList.count()
#       changed RBTree.insertNode to count insertions of the same item
#       changed RBList.insert(): uncommented some superfluid code
#       changed RBList.remove(): If called with all=True, then all instances
#                                of the node are deleted from the tree;
#                                else only node.count is decremented,
#                                if finally node.count is 1 the node 
#                                is deleted.  all is True by default.
#        changed RBTree.deleteNode : same changes as for RBList.remove()
#       finally I've changed the __version__ string to '1.6'

RBTree.py -- Red/Black Balanced Binary Trees with Dictionary Interface

Introduction:

This code adapted from C source from
Thomas Niemann's Sorting and Searching Algorithms: A Cookbook

From the title page:
    Permission to reproduce this document, in whole or in part, is 
    given provided the original web site listed below is referenced, 
    and no additional restrictions apply. Source code, when part of 
    a software project, may be used freely without reference to the 
    author.

-------------------------------------------------------------------------------
Usage:

RBTree.py defines a class, RBDict, which creates dictionary-like objects
implemented using a Red/Black tree (a form of balanced binary tree). 

Red/Black trees, I'm told, remain "nearly" balanced, and evidently the
algorithm is somehow inferior to the AVL tree.  However, Red/Black trees
have similar performance and the algorithm is much simpler IMHO.

Anyway, an RBDict instance behaves in almost every way like a dictionary;
however the .keys() method returns ordered keys instead of the "random"
keys returned by the normal (hashed) dictionary.

RBTree.py also contains a class, RBTree, which defines the tree without
the dictionary interface; RBDict is a subclass of RBTree, adding the 
interface goodies.

-------------------------------------------------------------------------------
Installation:

RBTree.py contains an internal Distutils-based installer; just run:

    python RBTree.py install

(as root/Administrator if needed) and you're done.

-------------------------------------------------------------------------------

"""
#for Python2&3 compatibility
from __future__ import absolute_import, division, print_function
from builtins import (bytes, str, open, super, range,
    zip, round, input, int, pow, object)
from future import standard_library
standard_library.install_aliases()
from future.builtins import next
from future.builtins import object

__version__ = "1.6"
import sys, os
import string, math
from palos.utils import PassingData

BLACK = 0
RED = 1

class RBNode(object):
    def __init__(self, key = None, value = None, color = RED):
        self.left = self.right = self.parent = None
        self.color = color
        self.key = key
        self.value = value
        self.nonzero = 1
        self.count = 1
    
    def __str__(self):
        return repr(self.key) + ': ' + repr(self.value)

    def __nonzero__(self):
        return self.nonzero

    def __len__(self):
        """imitate sequence"""
        return 2

    def __getitem__(self, index):
        """imitate sequence"""
        if index==0:
            return self.key
        if index==1:
            return self.value
        raise IndexError('only key and value as sequence')

    def depth(self):
        """
        2010-1-26
            Return the how deep the tree is. copied from class node in BinarySearchTree.py
        """
        if not self.left is None and self.left.nonzero!=0:
            # 2010-1-26 in RBTree(), 
            #   left and right are set to self.sentinel (whose nonzero is 0) by default.
            leftdepth = self.left.depth()
        else:
            leftdepth = 0

        if not self.right is None and self.right.nonzero!=0:
            rightdepth = self.right.depth()
        else:
            rightdepth = 0

        return max(leftdepth, rightdepth) + 1
    
class RBTreeIter(object):

    def __init__(self, tree):
        self.tree = tree
        self.index = -1 
        # ready to iterate on the next() call
        self.node = None
        self.stopped = False

    def __iter__(self):
        """
        #2010-8-2 return the whole node, rather than node.value
        
        Return the current item in the container
        """
        return self.node

    def next(self):
        """
        #2010-8-2 return the whole node, rather than node.value
        
        Return the next item in the container
        Once we go off the list we stay off even if the list changes
        """
        if self.stopped or (self.index + 1 >= self.tree.__len__()):
            self.stopped = True
            raise StopIteration
        #
        self.index += 1
        if self.index == 0:
            self.node = self.tree.firstNode()
        else:
            self.node = self.tree.nextNode(self.node)
        return self.node

cmp = lambda a,b: (a>b)-(a<b)

class RBTree(object):
    def __init__(self, cmpfn=cmp, unique=True):
        self.sentinel = RBNode()
        self.sentinel.left = self.sentinel.right = self.sentinel
        self.sentinel.color = BLACK
        self.sentinel.nonzero = 0
        self.root = self.sentinel
        self.elements = 0
        
        #SF: If self.unique is True, all elements in the tree have 
            #SF  to be unique and an exception is raised for multiple 
            #SF insertions of a node
            #SF If self.unique is set to False, nodes can be added multiple 
            #SF times. There is still only one node, but all insertions are
            #SF counted in the variable node.count
        self.unique = unique
        # changing the comparison function for an existing tree is dangerous!
        self.__cmp = cmpfn

    def __contains__(self, key):
        """
        2010-1-28
            copied from BinarySearchTree.py
        
            Check if a key is present in the tree.
            invoked in syntax such as "if key in tree: ...".
        """
        n = self.findNode(key)
        if n:
            return True
        else:
            return False
        
    def __len__(self):
        return self.elements

    def __del__(self):
        # unlink the whole tree
        s = [ self.root ]
        if self.root is not self.sentinel:
            while s:
                cur = s[0]
                if cur.left and cur.left != self.sentinel:
                    s.append(cur.left)
                if cur.right and cur.right != self.sentinel:
                    s.append(cur.right)
                cur.right = cur.left = cur.parent = None
                cur.key = cur.value = None
                s = s[1:]

        self.root = None
        self.sentinel = None

    def __str__(self):
        return "<RBTree object>"

    def __repr__(self):
        return "<RBTree object>"

    def __iter__(self):
        return RBTreeIter(self)

    def rotateLeft(self, x):

        y = x.right
        # establish x.right link
        x.right = y.left
        if y.left != self.sentinel:
            y.left.parent = x

        # establish y.parent link
        if y != self.sentinel:
            y.parent = x.parent
        if x.parent:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        else:
            self.root = y

        # link x and y
        y.left = x
        if x != self.sentinel:
            x.parent = y

    def rotateRight(self, x):

        #***************************
        #  rotate node x to right
        #***************************

        y = x.left

        # establish x.left link
        x.left = y.right
        if y.right != self.sentinel:
            y.right.parent = x

        # establish y.parent link
        if y != self.sentinel:
            y.parent = x.parent
        if x.parent:
            if x == x.parent.right:
                x.parent.right = y
            else:
                x.parent.left = y
        else:
            self.root = y

        # link x and y
        y.right = x
        if x != self.sentinel:
            x.parent = y

    def insertFixup(self, x):
        #************************************
        #  maintain Red-Black tree balance  *
        #  after inserting node x        	*
        #************************************

        # check Red-Black properties

        while x != self.root and x.parent.color == RED:

            # we have a violation

            if x.parent == x.parent.parent.left:

                y = x.parent.parent.right

                if y.color == RED:
                    # uncle is RED
                    x.parent.color = BLACK
                    y.color = BLACK
                    x.parent.parent.color = RED
                    x = x.parent.parent

                else:
                    # uncle is BLACK
                    if x == x.parent.right:
                        # make x a left child
                        x = x.parent
                        self.rotateLeft(x)

                    # recolor and rotate
                    x.parent.color = BLACK
                    x.parent.parent.color = RED
                    self.rotateRight(x.parent.parent)
            else:

                # mirror image of above code

                y = x.parent.parent.left

                if y.color == RED:
                    # uncle is RED
                    x.parent.color = BLACK
                    y.color = BLACK
                    x.parent.parent.color = RED
                    x = x.parent.parent

                else:
                    # uncle is BLACK
                    if x == x.parent.left:
                        x = x.parent
                        self.rotateRight(x)

                    x.parent.color = BLACK
                    x.parent.parent.color = RED
                    self.rotateLeft(x.parent.parent)

        self.root.color = BLACK

    def insertNode(self, key, value):
        #**********************************************
        #  allocate node for data and insert in tree  *
        #**********************************************

        # we aren't interested in the value, we just
        # want the TypeError raised if appropriate
        hash(key)

        # find where node belongs
        current = self.root
        parent = None
        while current != self.sentinel:
            # GJB added comparison function feature
            # slightly improved by JCG: don't assume that ==
            # is the same as self.__cmp(..) == 0
            rc = self.__cmp(key, current.key)
            if rc == 0:
                #SF This item is inserted for the second, 
                #SF third, ... time, so we have to increment 
                #SF the count
                if self.unique == False: 
                    current.count += 1
                else: # raise an Error
                    print("Warning: This element is already in the list ... ignored!")
                    #SF I don't want to raise an error because I want to keep 
                    #SF the code compatible to previous versions
                    #SF But here would be the right place to do this
                    #raise IndexError ("This item is already in the tree.")
                return current
            parent = current
            if rc < 0:
                current = current.left
            else:
                current = current.right

        # setup new node
        x = RBNode(key, value)
        x.left = x.right = self.sentinel
        x.parent = parent

        self.elements = self.elements + 1

        # insert node in tree
        if parent:
            if self.__cmp(key, parent.key) < 0:
                parent.left = x
            else:
                parent.right = x
        else:
            self.root = x

        self.insertFixup(x)
        return x

    def deleteFixup(self, x):
        #************************************
        #  maintain Red-Black tree balance  *
        #  after deleting node x        	*
        #************************************

        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.rotateLeft(x.parent)
                    w = x.parent.right

                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self.rotateRight(w)
                        w = x.parent.right

                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self.rotateLeft(x.parent)
                    x = self.root

            else:
                w = x.parent.left
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.rotateRight(x.parent)
                    w = x.parent.left

                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self.rotateLeft(w)
                        w = x.parent.left

                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self.rotateRight(x.parent)
                    x = self.root

        x.color = BLACK

    def deleteNode(self, z, all=True):
        #****************************
        #  delete node z from tree  *
        #****************************

        if not z or z == self.sentinel:
            return
            
        #SF If the object is in this tree more than once the node 
        #SF has not to be deleted. We just have to decrement the 
        #SF count variable
        #SF we don't have to check for uniquness because this was
        #SF already captured in insertNode() and for this reason 
        #SF z.count cannot be greater than 1
        #SF If all=True then the complete node has to be deleted
        if z.count > 1 and not all: 
            z.count -= 1
            return

        if z.left == self.sentinel or z.right == self.sentinel:
            # y has a self.sentinel node as a child
            y = z
        else:
            # find tree successor with a self.sentinel node as a child
            y = z.right
            while y.left != self.sentinel:
                y = y.left

        # x is y's only child
        if y.left != self.sentinel:
            x = y.left
        else:
            x = y.right

        # remove y from the parent chain
        x.parent = y.parent
        if y.parent:
            if y == y.parent.left:
                y.parent.left = x
            else:
                y.parent.right = x
        else:
            self.root = x

        if y != z:
            z.key = y.key
            z.value = y.value

        if y.color == BLACK:
            self.deleteFixup(x)

        del y
        self.elements = self.elements - 1

    def findNode(self, key):
        #******************************
        #  find node containing data
        #******************************

        # we aren't interested in the value, we just
        # want the TypeError raised if appropriate
        hash(key)
        
        current = self.root

        while current != self.sentinel:
            # GJB added comparison function feature
            # slightly improved by JCG: don't assume that ==
            # is the same as self.__cmp(..) == 0
            rc = self.__cmp(key, current.key)
            if rc == 0:
                return current
            else:
                if rc < 0:
                    current = current.left
                else:
                    current = current.right

        return None
    
    def findFirstAncestralNodeSmallerThanCurrent(self, current=None,):
        """
        2012.11.28
            find the first ancestral branch which is the right branch
        """
        parent = current.parent
        nodeToReturn = None
        while parent:
            if current == parent.right:
                nodeToReturn = parent
                break
            current = parent
            parent = parent.parent
        return nodeToReturn
    
    def findFirstAncestralNodeBiggerThanCurrent(self, current=None,):
        """
        2012.11.28
            find the first ancestral branch which is the right branch
        """
        parent = current.parent
        nodeToReturn = None
        while parent:
            if current == parent.left:
                nodeToReturn = parent
                break
            current = parent
            parent = parent.parent
        return nodeToReturn
    
    def findClosestNode(self, key=None):
        """
        2012.11.28
            given the key, find the exact matching node or
                the one/two nodes that are closest to the key.
            The return structure is either None or PassingData(smallerNode=, biggerNode=).
        """
        #******************************
        #  find node containing data
        #******************************

        # we aren't interested in the value, we just
        # want the TypeError raised if appropriate
        hash(key)
        
        current = self.root
        
        objectToReturn = None	#default, find nothing
        
        while current != self.sentinel:
            # GJB added comparison function feature
            # slightly improved by JCG: don't assume that ==
            # is the same as self.__cmp(..) == 0
            rc = self.__cmp(key, current.key)
            if rc == 0:
                objectToReturn = PassingData(smallerNode=current, biggerNode=current)
                break
            else:
                if rc < 0:	#to the left of current
                    if current.left ==self.sentinel:#but there is no more left
                        objectToReturn = PassingData(
                            smallerNode=self.findFirstAncestralNodeSmallerThanCurrent(current),
                            biggerNode=current)
                        break
                    current = current.left
                else:	#to the right of current
                    if current.right == self.sentinel:	#but there is no more right
                        objectToReturn = PassingData(smallerNode=current,
                            biggerNode=self.findFirstAncestralNodeBiggerThanCurrent(current))
                        break
                    current = current.right
        return objectToReturn
    
    def traverseTree(self, f):
        if self.root == self.sentinel:
            return
        s = [ None ]
        cur = self.root
        while s:
            if cur.left.key is not None:
                s.append(cur)
                cur = cur.left
            else:
                f(cur)
                while cur.right.key is None:
                    cur = s.pop()
                    if cur is None or cur.key is None:
                        return
                    f(cur)
                cur = cur.right
        # should not get here.
        return

    def nodesByTraversal(self):
        """return all nodes as a list"""
        result = []
        def traversalFn(x, K=result):
            K.append(x)
        self.traverseTree(traversalFn)
        return result

    def nodes(self):
        """return all nodes as a list"""
        cur = self.firstNode()
        result = []
        while cur and cur.key is not None:
            result.append(cur)
            cur = self.nextNode(cur)
        return result

    def firstNode(self):
        cur = self.root
        while cur.left.key is not None:
            cur = cur.left
        return cur

    def lastNode(self):
        cur = self.root
        while cur.right.key is not None:
            cur = cur.right
        return cur

    def nextNode(self, prev):
        """returns None if there isn't one"""
        cur = prev
        if cur.right.key is not None:
            cur = prev.right
            while cur.left.key is not None:
                cur = cur.left
            return cur
        while 1:
            cur = cur.parent
            if cur is None or cur.key is None:
                return None
            if self.__cmp(cur.key, prev.key)>=0:
                return cur

    def prevNode(self, next_node):
        """returns None if there isn't one"""
        cur = next_node
        if cur.left.key is not None:
            cur = next_node.left
            while cur.right.key is not None:
                cur = cur.right
            return cur
        while 1:
            cur = cur.parent
            if cur is None:
                return None
            if self.__cmp(cur.key, next_node.key)<0:
                return cur
    
    def depth(self):
        """
        2010-1-26
            copied from class node in BinarySearchTree.py
        
        Return the how deep the tree is.
        """

        if not self.root is None:
            return self.root.depth()
        else:
            return 0
        
    def optimumdepth(self):
        """
        2010-1-26
            copied from class node in BinarySearchTree.py
        
        Calculate the optimum depth of the tree based on how many nodes there are.
            The formula is: log2(n + 1)
        """

        return math.log(self.elements + 1, 2)

    def possibleused(self):
        """
        2010-1-26
            copied from class node in BinarySearchTree.py
        
        Calculate how many nodes could be used based on the depth of the tree.
        The formula is: (2 ^ depth) - 1.
        """

        return (2 ** self.depth()) - 1

    def efficiency(self):
        """
        2010-1-26
            copied from class node in BinarySearchTree.py
        
        Calculate the efficiency of the tree (how many slots are being wasted). The formula is:
            n / possibleused
        """
        return float(self.elements)/self.possibleused()
    
class RBList(RBTree):
    """ List class uses same object for key and value
        Assumes you are putting sortable items into the list.
    """

    def __init__(self, list=[], cmpfn=cmp, unique=True):
        #SF new option: unique trees, see RBTree.__init__() for 
        #SF more information
        RBTree.__init__(self, cmpfn, unique)
        for item in list:
            self.insertNode(item, item)

    def __getitem__(self, index):
        node = self.findNodeByIndex(index)
        return node.value

    def __delitem__(self, index):
        node = self.findNodeByIndex(index)
        self.deleteNode(node)

    def __contains__(self, item):
        return self.findNode(item) is not None

    def __str__(self):
        # eval(str(self)) returns a regular list
        return '['+ ','.join(map(lambda x: str(x.value), self.nodes()))+']'

    def findNodeByIndex(self, index):
        if (index < 0) or (index >= self.elements):
            raise IndexError("pop index out of range")
        #
        if index < self.elements/2:
            # simple scan from start of list
            node = self.firstNode()
            currIndex = 0
            while currIndex < index:
                node = self.nextNode(node)
                currIndex += 1
        else:
            # simple scan from end of list
            node = self.lastNode()
            currIndex = self.elements - 1
            while currIndex > index:
                node = self.prevNode(node)
                currIndex -= 1
        #
        return node

    def insert(self, item):
        #SF The function inserNode already checks for existing Nodes 
        #SF so this code seems to be superfluid
        #node = self.findNode(item)
        #if node is not None:
            #self.deleteNode(node)
        # item is both key and value for a list
        self.insertNode(item, item)

    def append(self, item):
        # list is always sorted
        self.insert(item)

    #SF this function is not implemented as a common list in python
    #def count(self):
        #return len(self)
        
    #SF Because we count all equal items in one node 
    #SF we now can use the function count as used in 
    #SF common python lists
    def count(self, item):
        node = self.findNode(item)
        return node.count

    def index(self, item):
        """
        return the index of the item in the RB list.
        """
        index = -1
        node = self.findNode(item)
        while node and node.value is not None:
            node = self.prevNode(node)
            index += 1
        if index < 0:
            raise ValueError("RBList.index: item not in list")
        return index

    def extend(self, otherList):
        for item in otherList:
            self.insert(item)

    def pop(self, index=None):
        if index is None:
            index = self.elements - 1
        node = self.findNodeByIndex(index)
        value = node.value	  # must do this before removing node
        self.deleteNode(node)
        return value

    def remove(self, item, all=True):
        #SF When called with all=True then all occurences are deleted
        node = self.findNode(item)
        if node is not None:
            self.deleteNode(node, all)

    def reverse(self):
        # not implemented
        raise AssertionError("RBlist.reverse Not implemented")

    def sort(self):
        # Null operation
        pass

    def clear(self):
        """delete all entries"""
        self.__del__()
        #copied from RBTree constructor
        self.sentinel = RBNode()
        self.sentinel.left = self.sentinel.right = self.sentinel
        self.sentinel.color = BLACK
        self.sentinel.nonzero = 0
        self.root = self.sentinel
        self.elements = 0

    def values(self):
        return list(map(lambda x: x.value, self.nodes()))

    def reverseValues(self):
        values = list(map(lambda x: x.value, self.nodes()))
        values.reverse()
        return values


class RBDict(RBTree):
    """
    Examples:
        
    """
    def __init__(self, dictionaryStructure={}, cmpfn=cmp):
        RBTree.__init__(self, cmpfn)
        for key, value in dictionaryStructure.items():
            self[key]=value
        # changing the comparison function for an existing tree is dangerous!
        self.__cmp = cmpfn
    
    def __str__(self):
        """
        2010-6-17
            better str() function
        """
        # eval(str(self)) returns a regular dictionary
        return_ls = []
        tree = self
        return_ls.append("Node Count: %d" % len(self))
        return_ls.append("Depth: %d" % tree.depth())
        return_ls.append("Optimum Depth: %f (%d) (%f%% depth efficiency)" % (
            tree.optimumdepth(), math.ceil(tree.optimumdepth()),
            math.ceil(tree.optimumdepth()) / tree.depth()))
        
        return_ls.append("Efficiency: %f%% (total possible used: %d, total wasted: %d): " % (
            tree.efficiency() * 100,
            len(tree) / tree.efficiency(),
            (len(tree) / tree.efficiency()) - len(tree)))
        
        return '\n'.join(return_ls)
    
    def __repr__(self):
        return "<RBDict object " + str(self) + ">"

    def __getitem__(self, key):
        n = self.findNode(key)
        if n:
            return n.value
        raise IndexError

    def __setitem__(self, key, value):
        n = self.findNode(key)
        if n:
            n.value = value
        else:
            self.insertNode(key, value)

    def __delitem__(self, key):
        n = self.findNode(key)
        if n:
            self.deleteNode(n)
        else:
            raise IndexError

    def get(self, key, default=None):
        n = self.findNode(key)
        if n:
            return n.value
        return default

    def keys(self):
        return map(lambda x: x.key, self.nodes())

    def values(self):
        return map(lambda x: x.value, self.nodes())

    def items(self):
        return map(tuple, self.nodes())

    def has_key(self, key):
        return self.findNode(key) or None

    def clear(self):
        """delete all entries"""

        self.__del__()

        #copied from RBTree constructor
        self.sentinel = RBNode()
        self.sentinel.left = self.sentinel.right = self.sentinel
        self.sentinel.color = BLACK
        self.sentinel.nonzero = 0
        self.root = self.sentinel
        self.elements = 0

    def copy(self):
        """return shallow copy"""
        # there may be a more efficient way of doing this
        return RBDict(self)

    def update(self, other):
        """Add all items from the supplied mapping to this one.

        Will overwrite old entries with new ones.

        """
        for key in other.keys():
            self[key] = other[key]

    def setdefault(self, key, value=None):
        if self.has_key(key):
            return self[key]
        self[key] = value
        return value
    
    def findNodes(self, key=None, node_ls=[], current=None, compareIns=None):
        """
        Examples:
            segmentKey = CNVSegmentBinarySearchTreeKey(chromosome=str(row.chromosome), \
                span_ls=[row.start, row.stop], \
                min_reciprocal_overlap=0.0000001)
                #min_reciprocal_overlap doesn't matter here.
                # it's decided by compareIns.
            node_ls = []
            genomeRBDict.findNodes(segmentKey, node_ls=node_ls, compareIns=compareIns)
        
        2010-8-17
            add argument compareIns, an instance of a class which has function cmp().
            
        2010-6-17
            find all nodes whose key could be matched and put them into node_ls
        """
        # we aren't interested in the value, we just
        # want the TypeError raised if appropriate
        hash(key)
        if current is None:
            current = self.root

        while current != self.sentinel:
            # GJB added comparison function feature
            # slightly improved by JCG: don't assume that ==
            # is the same as self.__cmp(..) == 0
            if compareIns is not None:	#2010-8-17
                rc = compareIns.cmp(key, current.key)
            else:
                rc = self.__cmp(key, current.key)
            if rc == 0:
                node_ls.append(current)
                self.findNodes(key, node_ls, current=current.left)
                self.findNodes(key, node_ls, current=current.right)
                break
            else:
                if rc < 0:
                    current = current.left
                else:
                    current = current.right
        return None

""" ----------------------------------------------------------------------------
    TEST ROUTINES
"""
def testRBlist():
    import random
    print("\n--- Testing RBList ---")
    print("Basic tests...")

    initList = [5,3,6,7,2,4,21,8,99,32,23]
    rbList = RBList(initList)
    initList.sort()
    print(f"initList after sort: {initList}\n")
    assert rbList.values() == initList
    print('rbList.values() == sorted initList')
    initList.reverse()
    assert rbList.reverseValues() == initList
    
    print("Test if index(i) is equal to i.")
    rbList = RBList([0,1,2,3,4,5,6,7,8,9])
    print(f"len(rbList): {len(rbList)}.")
    for i in range(10):
        #print(f'i={i}, rbList.index(i)={rbList.index(i)}')
        assert i == rbList.index(i)
        #print("Test success.")

    # remove odd values
    for i in range(1,10,2):
        rbList.remove(i)
    
    print(f"rbList.values() after deleting 1,3,5,7: {rbList.values()}")
    assert rbList.values() == [0,2,4,6,8]

    print("Pop tests")
    assert rbList.pop() == 8
    assert rbList.values() == [0,2,4,6]
    assert rbList.pop(1) == 2
    assert rbList.values() == [0,4,6]
    assert rbList.pop(0) == 0
    assert rbList.values() == [4,6]

    print("Random number insertion test")
    rbList = RBList()
    for i in range(5):
        k = random.randrange(10) + 1
        print("	Inserting", k)
        rbList.insert(k)
    print("	Random contents:", rbList)

    print("	Inserting 0.")
    rbList.insert(0)
    print("	Inserting 1.")
    rbList.insert(1)
    print("	Inserting 10.")
    rbList.insert(10)

    print("	With 0, 1 and 10:", rbList)
    n = rbList.findNode(0)
    print("\n")
    print("	Forward from 0:")
    while n is not None:
        print("(" + str(n) + ")",)
        n = rbList.nextNode(n)
    print("\n")

    n = rbList.findNode(10)
    print("	Backward from 10:",)
    while n is not None:
        print("(" + str(n) + ")",)
        n = rbList.prevNode(n)

    if rbList.nodes() != rbList.nodesByTraversal():
        print("node lists don't match")
    print("\n")

def testRBdict():
    import random
    print("\n--- Testing RBDict ---")

    rbDict = RBDict()
    for i in range(10):
        k = random.randrange(10) + 1
        rbDict[k] = i
    rbDict[1] = 0
    rbDict[2] = "value of key 2"
    
    print("Node Count: %d" % len(rbDict))
    print("Depth: %d" % rbDict.depth())
    print("Optimum Depth: %f (%d) (%f%% depth efficiency)" % (
        rbDict.optimumdepth(), math.ceil(rbDict.optimumdepth()),
        math.ceil(rbDict.optimumdepth()) / rbDict.depth()))
    print("Efficiency: %f" % rbDict.efficiency())
    
    print("	Value at 1:", rbDict.get(1, "Default"))
    print("	Value at 2:", rbDict.get(2, "Default"))
    print("	Value at 99:", rbDict.get(99, "Default"))
    print("	Keys:", list(rbDict.keys()))
    print("	values:", list(rbDict.values()))
    print("	Items:", list(rbDict.items()))

    if rbDict.nodes() != rbDict.nodesByTraversal():
        print("node lists don't match")

    # convert our RBDict to a dictionary-display,
    # evaluate it (creating a dictionary), and build a new RBDict
    # from it in reverse order.
    print(f'str(rbDict): {str(rbDict)}.')
    #revDict = RBDict(eval(str(rbDict)), lambda x, y: cmp(y,x))
    #print("	" + str(revDict))
    #print("\n")


if __name__ == "__main__":
    import sys
    if len(sys.argv) <= 1:
        testRBdict()
        testRBlist()
    else:
        from distutils.core import setup, Extension
        setup(name="RBTree",
            version=__version__,
            description="Red/Black Tree",
            long_description="Red/Black Balanced Binary Tree plus Dictionary and List",
            author="Yu Huang, Chris Gonnerman, Graham Breed, Charles Tolman, and Stefan Fruhner",
            author_email="polyactis@gmail.com",
            url="https://github.com/polyactis/pymodule",
            py_modules=["RBTree"]
        )
    sys.exit(0)


# end of file.
