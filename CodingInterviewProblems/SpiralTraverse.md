# Spiral Traverse

**Problem Description:**
Traverse 2D array in spiral way. Given 2D array, traverse in spiral way and output in 1D array. 
Example: 
```
input_nums = [[1, 2, 3, 4],
                  [12, 13, 14, 5],
                  [11, 16, 15, 6],
                  [10, 9, 8, 7]]

**After Traversing in Spiral way:**

output = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

```

**Solution: Iterative Approach**

```python
#Time:O(N) , Space: O(N); N is the total elements in the array
def sprial_Traverse(array):
    sc, ec = 0, len(array[0]) - 1
    sr, er = 0, len(array) - 1
    spiral_arr = []
    print(sc, ec, sr, er)

    while sc <= ec and sr<= er:
        for col in range(sc, ec+1):
            print(array[sr][col], end=',')
            spiral_arr.append(array[sr][col])
        for row in range(sr+1, er+1):
            print(array[row][ec], end=',')
            spiral_arr.append(array[row][ec])
        for col in reversed(range(sc, ec)):
            spiral_arr.append(array[er][col])
        for row in reversed(range(sr+1, er)):
            print(array[row][sc], end=',')
            spiral_arr.append(array[row][sc])

        sc, ec = sc+1, ec-1
        sr, er = sr+1, er-1
    
    return spiral_arr
```

**Recursive Solution:**

```python 
# Time:O(N) , Space: O(N); N is the total elements in the array
def spiral_Traverse_recursive(array):
    result = []
    spiralfill(array, 0, len(array) -1, 0, len(array[0]) - 1, result)
    return result

def spiralfill(array, sr, er, sc, ec, result):

    if sc > ec or sr > er:
        return 
    for col in range(sc, ec+1):
        result.append(array[sr][col])
    for row in range(sr+1, er+1):
        result.append(array[row][ec])
    for col in reversed(range(sc, ec)):
        result.append(array[er][col])
    for row in reversed(range(sr+1, er)):
        result.append(array[row][sc])

    spiralfill(array, sr+1, er-1, sc+1, ec-1, result)

```


**Test:**
```python
if __name__ == "__main__":
    input_nums = [[1, 2, 3, 4],
                  [12, 13, 14, 5],
                  [11, 16, 15, 6],
                  [10, 9, 8, 7]]
    result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    output1 = spiral_Traverse(input_nums)
    print(output1)
    assert result == output1, "Test output Failed. Result should be: "+str(result)
    print("Output: ", output1)
    output2 = spiral_Traverse_recursive(input_nums)
    print(output2)
    assert result == output2, "Test output Failed. Result should be: "+str(result)
    print("Output: ", output2)
```