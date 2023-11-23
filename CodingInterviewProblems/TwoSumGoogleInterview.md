## Two Sum


Leetcode Question: [Two Sum Problem](https://leetcode.com/problems/two-sum/)

**Question Asked By: Google**

**Problem Description:**
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

Example 1:

Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].



**Edge Cases:**
| S.N. | Nums | Target | Return |
| :------------ | :------------ |:---------------:| -----:|
| 1 | [1, 3, 6, 8, 4]    | target=5 | [0, 4] |
| 2 | []    | target=0 | None |
| 3 | [1, 5, 8]    | target=7 | None |
| 4 | [5]    | target=5 | None |
| 5 | [1, 4]    | target=5 | [0, 1] |


**Approach1: Brute Force Solutionl Time Complexity: O(N^2); Space Complexity: O(1)**

Solution: 
```python
class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return None

```

![image](https://github.com/sushant097/TSAI-ERAv1-Assignments/assets/30827903/f7267de0-698d-4c4d-a41c-e68abafe2dc2)


**Approach 2 (Optimal); Time Complexity: O(N), Space COmplexity: O(N)**

Solution: 
```python
class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        dict_i = {}
        for i in range(len(nums)):
            diff = target-nums[i]
            if diff not in dict_i:
                dict_i[nums[i]] = i
            else:
                return [dict_i[diff], i]
        return None

``````

![image](https://github.com/sushant097/TSAI-ERAv1-Assignments/assets/30827903/6902d4b5-00a2-477d-8c58-da6d99a9e313)