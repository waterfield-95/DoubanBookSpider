# -*- coding: utf-8 -*-
"""
@Time   : 2021/1/21 8:40 PM
@author : Yuan Tian
"""


class Solution(object):
    def merge(self, nums1, m, nums2, n):
        """
        :type nums1: List[int]
        :type m: int
        :type nums2: List[int]
        :type n: int
        :rtype: None Do not return anything, modify nums1 in-place instead.
        """
        # two get pointers for nums1 and nums2
        p1 = m - 1
        p2 = n - 1
        # set pointer for nums1
        p = m + n - 1
        while p >= 0 and p2 >= 0:
            if p1 < 0:
                nums1[p] = nums2[p2]
                p2 -= 1
                p -= 1
                continue
            if nums2[p2] > nums1[p1]:
                nums1[p] = nums2[p2]
                p2 -= 1
            else:
                nums1[p] = nums1[p1]
                p1 -= 1
            p -= 1


if __name__ == '__main__':
    n1 = [2, 0]
    n2 = [1]
    s = Solution()
    s.merge(n1, 1, n2, 1)
    print(n1)