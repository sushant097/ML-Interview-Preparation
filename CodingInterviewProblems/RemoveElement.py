
"""
Given an integer array nums and an integer val, remove all occurrences of val in nums in-place. The order of the elements may be changed. Then return the number of elements in nums which are not equal to val.

Consider the number of elements in nums which are not equal to val be k, to get accepted, you need to do the following things:

Change the array nums such that the first k elements of nums contain the elements which are not equal to val. The remaining elements of nums are not important as well as the size of nums.
Return k.


Idea:
Single Pointer Approach::
A more straightforward approach would be to move all elements that are not equal to val to the front of the array. This way, you don't need to explicitly count the number of elements equal to val, as the index of the next position to place a non-val element will give you the count of non-val elements (i.e., k). 


The k index is used to track the position where the next non-val element should be placed. Each time a non-val element is found, it's moved to the kth position, and k is incremented. The final value of k will be the count of elements not equal to val, and the first k elements in nums will be those elements. 
"""

class Solution(object):
    # Time: O(n) ; Space: O(1)
    def removeElement(self, nums, val):
        """
        :type nums: List[int]
        :type val: int
        :rtype: int
        """
        rp = len(nums) -1
        lp = 0
        count = 0 # number of elements equal to val
        while lp <= rp:
            if nums[lp] == val:
                count += 1
                if nums[rp] == val:
                    while nums[rp] == val:
                        count += 1
                        rp -= 1
                # swap
                nums[lp], nums[rp] = nums[rp], nums[lp]
                rp -= 1
            lp += 1

        # print(count)
        # print(nums)
        return len(nums) - count # numbers not equal to val
