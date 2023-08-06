class solver:

    def twoSum(nums, target):
        """
        https://leetcode.com/problems/two-sum/
        Given an array of integers nums and an integer target,
        return indices of the two numbers such that they add up to target.

        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        leftovers = {}
        for i, v in enumerate(nums):
            diff = target - v
            if diff in leftovers:
                return [leftovers[diff], i]
            if v not in leftovers:
                leftovers[v] = i
        return []


    def singleNumber(nums):
        """
        https://leetcode.com/problems/single-number/
        Given a non-empty array of integers nums,
        every element appears twice except for one. Find that single one.

        :type nums: List[int]
        :rtype: int
        """
        a = 0
        for i in nums:
            a ^= i
        return a


    def lengthOfLongestSubstring(s):
        """
        https://leetcode.com/problems/longest-substring-without-repeating-characters/
        Given a string s, find the length of the longest substring without repeating characters.

        :type s: str
        :rtype: int
        """
        dicts = {}
        maxlength = start = 0
        for i,value in enumerate(s):
            if value in dicts:
                sums = dicts[value] + 1
                if sums > start:
                    start = sums
            num = i - start + 1
            if num > maxlength:
                maxlength = num
            dicts[value] = i
        return maxlength


# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
    def addTwoNumbers(l1, l2, c = 0):
        """
        https://leetcode.com/problems/add-two-numbers/
        Given two non-empty linked lists representing two non-negative integers.
        The digits are stored in reverse order, and each of their nodes contains a single digit.
        Add the two numbers and return the sum as a linked list.

        Assume the two numbers do not contain any leading zero, except the number 0 itself.
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        val = l1.val + l2.val + c
        c = val // 10
        ret = ListNode(val%10)

        if (l1.next != None or l2.next != None or c != 0):
            if l1.next == None:
                l1.next = ListNode(0)
            if l2.next == None:
                l2.next = ListNode(0)
            ret.next = self.addTwoNumbers(l1.next, l2.next, c)
        return ret


    def reverseList(self, head):
        """
        https://leetcode.com/problems/reverse-linked-list/
        Reverse a singly linked list.

        :type head: ListNode
        :rtype: ListNode
        """
        if not head or not head.next:
            return head
        p = self.reverseList(head.next)
        head.next.next = head
        head.next = None
        return p


# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
    def mergeTrees(self, t1, t2):
        """
        https://leetcode.com/problems/merge-two-binary-trees/
        Given two binary trees and imagine that when you put one of them to cover the other,
        some nodes of the two trees are overlapped while the others are not.
        You need to merge them into a new binary tree. The merge rule is that if two nodes overlap,
        then sum node values up as the new value of the merged node.
        Otherwise, the NOT null node will be used as the node of new tree.

        :type t1: TreeNode
        :type t2: TreeNode
        :rtype: TreeNode
        """
        if not t1:
            return t2
        if not t2:
            return t1
        t = TreeNode(t1.val+t2.val)
        t.left = self.mergeTrees(t1.left, t2.left)
        t.right = self.mergeTrees(t1.right, t2.right)
        return t


    def maxDepth(self, root):
        """
        https://leetcode.com/problems/maximum-depth-of-binary-tree/
        Given a binary tree, find its maximum depth.
        The maximum depth is the number of nodes along the longest path
        from the root node down to the farthest leaf node.

        :type root: TreeNode
        :rtype: int
        """
        if root is None:
            return 0
        else:
            left_h = self.maxDepth(root.left)
            right_h = self.maxDepth(root.right)
            return max(left_h, right_h) + 1


    def invertTree(self, root):
        """
        https://leetcode.com/problems/invert-binary-tree/
        Invert a binary tree.

        :type root: TreeNode
        :rtype: TreeNode
        """
        if root:
            root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root
