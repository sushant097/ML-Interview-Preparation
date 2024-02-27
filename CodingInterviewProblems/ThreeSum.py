"""


"""

class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        result = set()
        n = len(nums)
        nums.sort()

        for i in range(n-2):
            left = i+1
            right = n - 1
            while right > left:
                sum_ = nums[i] + nums[left] + nums[right]
                if sum_ == 0:
                    result.add((nums[i], nums[left],nums[right]))
                elif sum_ < 0:
                    left += 1
                else: 
                    right -= 1
        
        return result