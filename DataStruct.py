#!/usr/bin/env python
# _*_ coding:utf-8 _*_

__author__ = 'Huoyunren'


class TreeNode(object):
    """
    二叉树节点
    """

    def __init__(self, data=0, left=0, right=0):
        self.data = data
        self.left = left
        self.right = right


class BTress(object):
    """
    二叉树
    """

    def __init__(self, root=0):
        self.root = root

    def is_empty(self):
        """
        :return:
        """
        if self.root is 0:
            return True
        else:
            return False

    def pre_order(self, tree_node):
        """
        先序遍历
        :param tree_node:
        :return:
        """
        if tree_node is 0:
            return
        print tree_node.data
        self.pre_order(tree_node.left)
        self.pre_order(tree_node.right)

    def mid_order(self, tree_node):
        """
        中序遍历
        :param tree_node:
        :return:
        """
        if tree_node is 0:
            return
        self.mid_order(tree_node.left)
        print tree_node.data
        self.mid_order(tree_node.right)

    def later_order(self, tree_node):
        """
        后序遍历
        :param tree_node:
        :return:
        """
        if tree_node is 0:
            return
        self.later_order(tree_node.left)
        self.later_order(tree_node.right)
        print tree_node.data


def get_btree():
    n1 = TreeNode(5)
    n2 = TreeNode(4, n1)
    n3 = TreeNode(3)
    n4 = TreeNode(2, n3, n2)
    n5 = TreeNode(7)
    n6 = TreeNode(6, n5)
    n7 = TreeNode(1, n4, n6)

    btree = BTress(n7)
    # btree.pre_order(btree.root)
    # btree.mid_order(btree.root)
    btree.later_order(btree.root)


if __name__ == "__main__":
    get_btree()
