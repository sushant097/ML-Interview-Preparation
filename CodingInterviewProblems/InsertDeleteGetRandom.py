
"""
Description::
Implement the RandomizedSet class:

RandomizedSet() Initializes the RandomizedSet object.
bool insert(int val) Inserts an item val into the set if not present. Returns true if the item was not present, false otherwise.
bool remove(int val) Removes an item val from the set if present. Returns true if the item was present, false otherwise.
int getRandom() Returns a random element from the current set of elements (it's guaranteed that at least one element exists when this method is called). Each element must have the same probability of being returned.
You must implement the functions of the class such that each function works in average O(1) time complexity.

 

Example 1:

Input
["RandomizedSet", "insert", "remove", "insert", "getRandom", "remove", "insert", "getRandom"]
[[], [1], [2], [2], [], [1], [2], []]
Output
[null, true, false, true, 2, true, false, 2]

Explanation
RandomizedSet randomizedSet = new RandomizedSet();
randomizedSet.insert(1); // Inserts 1 to the set. Returns true as 1 was inserted successfully.
randomizedSet.remove(2); // Returns false as 2 does not exist in the set.
randomizedSet.insert(2); // Inserts 2 to the set, returns true. Set now contains [1,2].
randomizedSet.getRandom(); // getRandom() should return either 1 or 2 randomly.
randomizedSet.remove(1); // Removes 1 from the set, returns true. Set now contains [2].
randomizedSet.insert(2); // 2 was already in the set, so return false.
randomizedSet.getRandom(); // Since 2 is the only number in the set, getRandom() will always return 2.

Leetcode Question LInk: https://leetcode.com/problems/insert-delete-getrandom-o1

"""




"""
############ IDEA #################
Intuition
    We need to implement a RandomizedSet class.
    We need to define an initialize method, along with an insert, remove (delete), and getRandom method.
    getRandom() only gets called if there is atleastoneat least oneatleastone element in the data structure (array).

Approach:

Initialize
Initialize a values array.

Insert
Check if the value is not in the values array.
If true, add the value to the values array and return true.
If false, return false.

Remove
Check if the value is in the values array.
If true, remove the value from the values array and return true.
If false, return false.

Get Random
Import random (on line 1).
Return a random value from the values array.

Complexity
Time complexity: O(n)

Space complexity: O(n)

"""

class RandomizedSet(object):

    def __init__(self):
        self.values = []
        self.idx_map = {}

    def insert(self, val):
        """
        :type val: int
        :rtype: bool
        """
        if val in self.idx_map:
            return False
        self.idx_map[val] = len(self.values)
        self.values.append(val)
        return True

    def remove(self, val):
        """
        :type val: int
        :rtype: bool
        """
        if val not in self.idx_map:
            return False
        last_element, idx = self.values[-1], self.idx_map[val]
        self.values[idx], self.idx_map[last_element] = last_element, idx
        # Remove the last element and delete the val from dict
        self.values.pop()
        del self.idx_map[val]
        return True


    def getRandom(self):
        """
        :rtype: int
        """
        return random.choice(self.values)


# Your RandomizedSet object will be instantiated and called as such:
# obj = RandomizedSet()
# param_1 = obj.insert(val)
# param_2 = obj.remove(val)
# param_3 = obj.getRandom()