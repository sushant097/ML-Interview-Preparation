"""
Given an array nums of size n, return the majority element.

The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.

 

Example 1:

Input: nums = [3,2,3]
Output: 3
Example 2:

Input: nums = [2,2,1,1,1,2,2]
Output: 2
 

https://leetcode.com/problems/majority-element/description
"""

# Time: O(n) | Space: O(1)
class Solution(object):
    def majorityElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        store = {}
        n = len(nums)/2
        for i in range(len(nums)):
            store[nums[i]] = store.get(nums[i], 0) + 1
        
        for i in store:
            if store[i] > n:
                return i
                
"""
How to achieve Space Complexity as O(1): Using Boyer-Moore Voting ALgorithm.

To achieve O(1) space complexity for finding the majority element in an array, you can use the Boyer-Moore Voting Algorithm. This algorithm is a clever way to find the majority element without needing extra space for hash maps or counters.

The Boyer-Moore Voting Algorithm works under the assumption that there is a majority element in the array (an element that appears more than n/2 times). The key idea of the algorithm is to maintain a count of a potential majority element. If we see the same element as the current potential majority, we increment the count, otherwise, we decrement it. If the count reaches zero, we choose the current element as the new potential majority element and reset the count.
"""

# Time: O(n) | Space: O(1)
class Solution(object):
    def majorityElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        count = 0
        candidate = None
        for num in nums:
            if count == 0:
                candidate  = num
            count += (1 if num == candidate else -1)
        return candidate