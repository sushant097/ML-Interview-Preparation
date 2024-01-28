"""
26. Remove Duplicates from Sorted Array
Leetcode Question Link: https://leetcode.com/problems/remove-duplicates-from-sorted-array/

Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once. The relative order of the elements should be kept the same. Then return the number of unique elements in nums.

Consider the number of unique elements of nums to be k, to get accepted, you need to do the following things:

Change the array nums such that the first k elements of nums contain the unique elements in the order they were present in nums initially. The remaining elements of nums are not important as well as the size of nums.
Return k.


"""

# Time: O(n); Space: O(n)
# Using extra memory space
class Solution(object):
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        result = []
        prev = nums[0]
        result.append(prev)
        for i in range(1, len(nums)):
            if prev != nums[i]:
                result.append(nums[i])
            prev = nums[i]

        nums[0:len(result)+1] = result
        return len(result)
    
# Time: O(n)| Space : O(1)
# Using Two pointer approach
# Beats 99.90% of users with Python in Leetcode
class Solution(object):
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        # result = []
        # prev = nums[0]
        # result.append(prev)
        # for i in range(1, len(nums)):
        #     if prev != nums[i]:
        #         result.append(nums[i])
        #     prev = nums[i]

        # nums[0:len(result)+1] = result
        # return len(result)

        k = 1 # pointer to place unique element
        prev = nums[0]
        for i in range(1, len(nums)):
            if nums[i] != prev:
                nums[k] = nums[i]
                k += 1
                prev = nums[i]
        return k
    
