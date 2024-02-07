"""
Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.

 

Example 1:

Input: nums = [1,2,3,4]
Output: [24,12,8,6]
Example 2:

Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]

Leetcode: https://leetcode.com/problems/product-of-array-except-self/description/

"""

class Solution(object):
    # Time: O(n) | Space: O(n)
    def productExceptSelf(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        n = len(nums)
        result_left = [1] * n
        result_right = [1] * n
        answer = [1] * n

        # calculate products from left
        for i in range(1, n):
            result_left[i] = nums[i-1] * result_left[i-1]
        
        # calculate products from right
        for i in range(n-2, -1, -1):
            result_right[i] = nums[i+1] * result_right[i+1]
        
        # calculate the final answer: product array
        for i in range(n):
            answer[i] = result_left[i] * result_right[i]

        return answer
        
