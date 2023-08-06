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
