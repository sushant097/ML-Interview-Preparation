# Monotonic Array

**Problem Description**
The given array is not entirely non-increasing or non-decreasing. You should output boolean True or False whether the given array is monotonic or not.
Example:
nums=[-1, -10, -20, -500, -500, -600, -602, -800]
output: True

Note: There maybe numbers which are equal to each other and still the array can be monotonic.

**Solution:**
```python

# Time: O(N), Space: O(1)
def isMonotonic(arr):
    if len(arr) < 2:
        return True
    direction = arr[1] - arr[0]
    for i in range(2, len(arr)):
        if direction == 0:
            direction = arr[i] - arr[i-1]
            continue
        if breakDirectionCondition(direction, arr[i], arr[i-1]):
            return False
        
    return True

def breakDirectionCondition(direction, currNum, prevNum):
    diff = currNum - prevNum
    if direction > 0:
        return diff < 0
    return diff > 0


if __name__ == "__main__":
    input_nums = [-1, -10, -20, -500, -500, -600, -602, -800]
    result = True
    output1 = isMonotonic(input_nums)
    assert result == output1, "Test output Failed. Result should be: "+str(result)
    print("Output: ", output1)
```