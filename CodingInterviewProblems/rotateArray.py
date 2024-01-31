"""
Given an integer array nums, rotate the array to the right by k steps, where k is non-negative.

 

Example 1:

Input: nums = [1,2,3,4,5,6,7], k = 3
Output: [5,6,7,1,2,3,4]
Explanation:
rotate 1 steps to the right: [7,1,2,3,4,5,6]
rotate 2 steps to the right: [6,7,1,2,3,4,5]
rotate 3 steps to the right: [5,6,7,1,2,3,4]
Example 2:

Input: nums = [-1,-100,3,99], k = 2
Output: [3,99,-1,-100]
Explanation: 
rotate 1 steps to the right: [99,-1,-100,3]
rotate 2 steps to the right: [3,99,-1,-100]


Leetcode link: https://leetcode.com/problems/rotate-array/


"""

# We can easily solve this question with extra memory space
# Time: O(n)  | O(n)
class Solution(object):
    def rotate(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: None Do not return anything, modify nums in-place instead.
        """
        # O(n); O(n)
        temp = [None] * len(nums)
        for i in range(len(nums)):
            pos = (i+k) % len(nums)
            temp[pos] = nums[i]
        
        for i in range(len(temp)):
            nums[i] = temp[i]

# How to do it in inplace? i.e O(1) space complexity
"""
Steps to do that:
1. Reverse the whole array.
2. Reverse the first k elements of the array.
3. Reverse the remaining elements
"""

# Time: O(n) | Space: O(1)
class Solution(object):
    def rotate(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: None Do not return anything, modify nums in-place instead.
        """
        # O(n); O(1)
        def __reverse(l, r, nums):
            while l < r:
                nums[l], nums[r] = nums[r] , nums[l]
                l += 1
                r -= 1

        # make sure k is within the range
        k = k % len(nums)

        # First reverse the whole array
        l, r = 0, len(nums) - 1
        __reverse(l, r, nums)

        # Reverse the first k elements
        l, r = 0, k - 1
        __reverse(l, r, nums)

        # Reverse the rest of the elements
        l, r = k, len(nums) - 1
        __reverse(l, r, nums)
