
"""
There are n children standing in a line. Each child is assigned a rating value given in the integer array ratings.

You are giving candies to these children subjected to the following requirements:

Each child must have at least one candy.
Children with a higher rating get more candies than their neighbors.
Return the minimum number of candies you need to have to distribute the candies to the children.

 

Example 1:

Input: ratings = [1,0,2]
Output: 5
Explanation: You can allocate to the first, second and third child with 2, 1, 2 candies respectively.
Example 2:

Input: ratings = [1,2,2]
Output: 4
Explanation: You can allocate to the first, second and third child with 1, 2, 1 candies respectively.
The third child gets 1 candy because it satisfies the above two conditions.
 
Leetcode Question link:: https://leetcode.com/problems/candy/
"""

class Solution(object):
    # TIme: O(n) ; Space: O(n)
    def candy(self, ratings):
        """
        :type ratings: List[int]
        :rtype: int
        """
        # Explanation: https://www.youtube.com/watch?v=1IzCRCcK17A
        arr = [1]  * len(ratings)
        
        # Traverse from left to right
        # increment the candy's based off the left neighbor
        for i in range(1, len(ratings)):
            # if the left neighbor is less than the current, then the current deserves one more candy than the prev
            if ratings[i] > ratings[i-1]:
                arr[i] = arr[i-1] + 1

        # Traverse from right to left
        # increment the candy's based off the right neighbor
        for i in range(len(ratings) -2, -1, -1):
            # if the right neighbor is less than the current, then current deserves one more candy than the right
            if ratings[i] > ratings[i+1]:
                 # here is the tricky part, if the current indexes candy is already higher than the right then leave it
                # you don't want to update the current candy to candy[right] + 1 because there is a possibility that
                # it will be less than the first pass iteration
                arr[i] = max(arr[i], arr[i+1] + 1) # candies must be greater than its neighbors
        
        return sum(arr)

        


        
