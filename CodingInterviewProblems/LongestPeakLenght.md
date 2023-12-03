**Longest Peak**
Given the arrary of integers find the length of longest peak.

Example:
```bash

arr = [1,2 4, 3, 6, 10, 8, 7, 5] => longestPeak = 4
                ^             ^
                |<----------->|
                     4

```

**Solution**

```python 
# Time: O(N) | Space: O(1)
def findLongestPeakLenght(arr):
    i = 1
    longestPeakLength = 0
    while i < len(arr) - 1:
        isPeak = arr[i-1] < arr[i] and arr[i+1] > arr[i]
        if not isPeak:
            i +=1 
            continue
        leftIdx = i - 2
        while leftIdx <= 0 and arr[leftIdx] < arr[leftIdx - 1]:
            leftIdx -= 1
        rightIdx = i + 2
        while rightIdx < len(arr) and arr[rightIdx] < arr[rightIdx + 1]:
            rightIdx += 1

        currPeakLenght = rightIdx - leftIdx -1
        longestPeakLength = max(longestPeakLength, currPeakLenght)
        i = rightIdx
        return longestPeakLength
        
```