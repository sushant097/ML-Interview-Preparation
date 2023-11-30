# Move Element to the End

**Problem Description**

Given target integer, move all integer equal to given integer to at the end of array inplace in any order. 
Example: 
nums=[1, 2, 5, 10, 3, 4, 3, 11, 2], toMove=3 ==> [1, 5, 10, 4, 11, 2, 3, 3, 3]

**Solution**
```python

#two pointer approach
def move_element_to_end(nums, toMove):
    lp = 0
    rp = len(nums) - 1
    while rp > lp:
        if nums[lp] == toMove and nums[rp] != toMove:
            nums[lp], nums[rp] = nums[rp], nums[lp]
            lp +=1
        elif nums[rp] == toMove and nums[lp] != toMove:
            rp -= 1
        elif nums[lp] != toMove and nums[rp] != toMove:
            lp += 1
    return nums

def move_element_to_end2(nums, toMove):
    lp = 0
    rp = len(nums) - 1
    while rp > lp:
        while lp < rp and nums[rp]==toMove:
            rp -= 1
        if nums[lp] == toMove:
            nums[lp], nums[rp] = nums[rp], nums[lp]

        lp += 1
    return nums


if __name__ == "__main__":
    input_nums = [1, 3, 5, 10, 3, 4, 3, 11, 2]
    input_target = 3
    result = [1, 2, 5, 10, 11, 4, 3, 3, 3]
    output1 = move_element_to_end(input_nums, input_target)
    assert result == output1, "Test output Failed. Result should be: "+str(result)
    print("Output: ", output1)
    output2 = move_element_to_end2(input_nums, input_target)
    assert result == output2, "Test output Failed. Result should be: "+str(result)
    print("Output: ", output2)
```