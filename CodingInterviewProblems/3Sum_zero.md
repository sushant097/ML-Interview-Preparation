

## 3 Sum
Leetcode Question: [Three Sum Problem](https://leetcode.com/problems/3sum/)

**Question Asked By: Google**

**Problem Description:**
Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

Example 1:

Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
Explanation: 
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter.


**Approach1: Brute Force Solutionl Time Complexity: O(N^3); Space Complexity: O(N)**

```python


class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        # Brute Force Approach:
        # Time: O(N^3), Space: O(N)
        triplets = []
        
        if len(nums) <=2:
            return triplets
        
        # Sort for better handling:
        nums.sort()

        for i in range(len(nums) - 2):
            # Skip duplicates to avoid duplicate triplets
            if i > 0 and nums[i] == nums[i-1]:
                continue
            for j in range(i+1, len(nums)-1):
                # Skip duplicate for second element
                while j > i + 1 and nums[j] == nums[j-1]:
                    continue
                for k in range(j+1, len(nums)):
                    if nums[i] + nums[j] + nums[k] == 0:
                        triplets.append([nums[i], nums[j], nums[k]])
                        # Skip duplicate for third element
                        while k < len(nums) - 1 and nums[k] == nums[k+1]:
                            k += 1
 
        return triplets
```

**Approach2: Two Pointer Time Complexity: O(N^2); Space Complexity: O(N)**
```python
class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        # Brute Force Approach:
        # Time: O(N^2), Space: O(N)
        triplets = []
        
        if len(nums) < 3:
            return triplets
        
        # Sort for better handling:
        nums.sort()

        for i in range(len(nums) - 2):
           if i > 0 and nums[i] == nums[i-1]:
               continue
           leftP = i + 1
           rightP = len(nums) - 1
           while rightP > leftP:
            sum = nums[i] + nums[leftP] + nums[rightP]
            if sum == 0:
                temp = [nums[i], nums[leftP], nums[rightP]]
                if temp not in triplets:
                    triplets.append(temp)
                leftP += 1
                rightP -= 1
            elif sum > 0:
                rightP -= 1
            elif sum < 0:
                leftP += 1
            
        return triplets

```

