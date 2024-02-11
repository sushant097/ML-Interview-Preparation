"""
Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

Example 1:
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.

Example 2:

Input: height = [4,2,0,3,2,5]
Output: 9
 

Leetcode Question Link: https://leetcode.com/problems/trapping-rain-water/

"""



class Solution(object):
    def trap(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        maxLeft = [0] * len(height)
        maxRight = [0] * len(height)
        min_lr = [0] * len(height)
        total_water = 0
        temp = 0
        for i in range(1, len(height)):
            temp = max(height[i-1], temp)
            maxLeft[i] = temp
        temp = 0
        for i in range(len(height)-2, -1, -1):
            temp = max(height[i+1], temp)
            maxRight[i] = temp
        
        # finding total water it can reserve in each position
        # formula: min(maxLeft, maxRight) - h[position]
        for i in range(len(height)):
            diff = min(maxLeft[i], maxRight[i]) - height[i]
            if diff > 0:
                total_water += diff
        
        return total_water