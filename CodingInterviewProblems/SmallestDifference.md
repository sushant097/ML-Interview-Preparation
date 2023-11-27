## Smallest Difference

**Question**
Find the pair of numbers where one number come from first array and another number from second array with the smallest difference. 

**Example**
arr1 = [-1, 5, 10, 20, 28, 3]
arr2 = [26, 134, 135, 15, 17]

Smallest Pair of Number = [28, 26]


**Solution**
**Using Two pointer Approach**
Let's simplify the problem. If the two arrays are sorted, how would we find the pair with the smallest absolute difference?

Suppose the two sorted arrays are:

```
arrayOne = [-1, 3, 5, 10, 20, 28];
arrayTwo = [15, 17, 26, 134, 135];
```

If we map the numbers of the two arrays onto a number line, we get:

```
         <--|---|---|---|---|---|---|---|---|---|---|-->
arrayOne:  -1   3   5   10          20      28
arrayTwo:                  15  17      26     134  135
```

It can be noticed that for each number between `-1` and `10` in the `arrayOne`, we only need to compute their absolute difference with regards to `15`. The reason for that is that `-1, 3, 5, 10` are all smaller than `15` and every number after `15` in the `arrayTwo` is greater than `15`, which means all the numbers after `15` are farther away from the numbers `-1, 3, 5, 10` than `15` and therefore we don't need to consider those numbers after `15`. Likewise, for `15` and `17` in `arrayTwo`, we only need to compute their absolute difference with regards to `20`.

We can also noticed that we'll be getting closer and closer to `15` as we go through the numbers `-1, 3, 5, 10`. Similarly, `17` is closer to `20` than any number that comes before `17`.

Based on the above observation, we could solve the simplified version of the problem by maintaining two pointers and moving one of them based on the comparison between the two numbers that the two pointers are pointing at.

We start both pointers at index `0` and use a variable to track the smallest absolute difference so far. Since we are asked to return the pair with the smallest absolute difference, we also need to remember the smallest pair found thus far.

```
smallestAbsDiff = Infinity
smallestPair = []

arrayOne = [ -1, 3, 5, 10, 20, 28 ]   arrayTwo = [ 15, 17, 26, 134, 135 ]
              ^                                    ^
              p1                                   p2
```

First we compute the absolute difference between the numbers that the two pointers point at and update the current smallest absolute difference if necessary. The absolute difference between `-1` and `15` is `16`, which is smaller than the `smallestAbsDiff`, so we set it as the current smallest absolute difference and update the `smallestPair`. Then we need to determine which pointer we should move. `-1` is smaller than `15`, which means we should update the pointer `p1`: `p1 += 1`. The reasons for that are:

1. Since every number after `-1` is for sure going to be greater than `-1`, they might be closer to `15` than `-1`.

2. For the number `-1`, we can ignore all the numbers that are after `15`, because they are all going to be greater than `15` and thus are farther away from `-1`. For instance, the number that follows immediately after `15` is `17`. `-1` and `17` are farther apart than `-1` and `15`.

```
smallestAbsDiff = 16
smallestPair = [ -1, 15 ]

arrayOne = [ -1, 3, 5, 10, 20, 28 ]   arrayTwo = [ 15, 17, 26, 134, 135 ]
                 ^                                 ^
                 p1                                p2
```

The absolute difference between `3` and `15` is `12`, so we have found a smaller absolute difference. Set it as the current smallest absolute difference and update the `smallestPair`.

Since `3` is smaller `15`, we move `p1` to the right by one.

```
smallestAbsDiff = 12
smallestPair = [ 3, 15 ]

arrayOne = [ -1, 3, 5, 10, 20, 28 ]   arrayTwo = [ 15, 17, 26, 134, 135 ]
                    ^                              ^
                    p1                             p2
```

`abs(5 - 15) = 10`, which is smaller than the current smallest absolute difference, so we update the `smallestAbsDiff` and the `smallestPair`.

`5` is smaller than `15`. That means we should move `p1`.

```
smallestAbsDiff = 10
smallestPair = [ 5, 15 ]

arrayOne = [ -1, 3, 5, 10, 20, 28 ]   arrayTwo = [ 15, 17, 26, 134, 135 ]
                       ^                           ^
                       p1                          p2
```

We have found a smaller absolute difference `5`. Update the `smallestAbsDiff` and the `smallestPair`.

`10` is smaller than `15`, so we move `p1`.

```
smallestAbsDiff = 5
smallestPair = [ 10, 15 ]

arrayOne = [ -1, 3, 5, 10, 20, 28 ]   arrayTwo = [ 15, 17, 26, 134, 135 ]
                           ^                       ^
                           p1                      p2
```

The absolute difference between `20` and `15` is `5`. That means we don't need to do anything.

Now the number that `p1` points at is greater than the one `p2` points at, thus we move `p2`: `p2 += 1`.

```
smallestAbsDiff = 5
smallestPair = [ 10, 15 ]

arrayOne = [ -1, 3, 5, 10, 20, 28 ]   arrayTwo = [ 15, 17, 26, 134, 135 ]
                           ^                           ^
                           p1                          p2
```

The absolute difference between `20` and `17` is `3`. We've found a smaller absolute difference. Update the `smallestAbsDiff` and the `smallestPair`.

`17` is smaller than `20`, so move `p2`.

```
smallestAbsDiff = 3
smallestPair = [ 20, 17 ]

arrayOne = [ -1, 3, 5, 10, 20, 28 ]   arrayTwo = [ 15, 17, 26, 134, 135 ]
                           ^                               ^
                           p1                              p2
```

The absolute difference between `20` and `26` is `6`. We don't need to do anything.

Since `20` is smaller than `26`, move `p1`.

```
smallestAbsDiff = 3
smallestPair = [ 20, 17 ]

arrayOne = [ -1, 3, 5, 10, 20, 28 ]   arrayTwo = [ 15, 17, 26, 134, 135 ]
                               ^                           ^
                               p1                          p2
```

We found a smaller absolute difference `2`. Update the `smallestAbsDiff` and the `smallestPair`.

`26` is smaller than `28`, so we move `p2`.

```
smallestAbsDiff = 2
smallestPair = [ 28, 26 ]

arrayOne = [ -1, 3, 5, 10, 20, 28 ]   arrayTwo = [ 15, 17, 26, 134, 135 ]
                               ^                                ^
                               p1                               p2
```

`abs(28 - 134) = 106`, so we don't need to do anything.

Since `28` is smaller than `134`, move `p1`.

```
smallestAbsDiff = 2
smallestPair = [ 28, 26 ]

arrayOne = [ -1, 3, 5, 10, 20, 28 ]   arrayTwo = [ 15, 17, 26, 134, 135 ]
                                  ^                            ^
                                  p1                           p2
```

We reach the end of the `arrayOne`, so we are done. We have correctly found the pair.

One might wonder which pointer we should move if the elements that the two pointers point at are equal to each other. In this case, we can just return the two elements, because it is impossible for us to find another pair that has a smaller absolute difference than `0`.

Now to solve the complex version of the problem, we just need to sort the two arrays upfront.

**Algorithm**

- Sort both arrays.

- Use a variable to track the smallest absolute difference so far.

- Initialize an empty array to store the current smallest pair.

- Initialize two pointers `p1` and `p2` to `0`, where `p1` is going to track the current index in the first array, and `p2` is going to track the current index in the second array.

- Loop until we reach the end of one of the two arrays.

  - Compare the absolute difference between the numbers that the two pointers point at with the current smallest absolute difference. If we have found a smaller difference, set it as the current smallest difference and update the current smallest pair.

  - Compare the number that `p1` is pointing at with the number that `p2` is pointing at. If they are equal to each other, break out of the loop. Otherwise, move `p1` to right by one if the number from the first array is smaller, or move `p2` to right by one if the number from the second array is smaller.

- Return the smallest pair.

**Code:**
```python
# Time: O(NlogN + M LogM) ~ O(N.M)| Space: O(1)
def smallestDifference(arr1, arr2):
    # Sort the two arrarys
    arr1.sort()
    arr2.sort()

    lp = 0
    rp = 0
    pair = []
    smallsum = float(inf)

    while lp < len(arr1) and rp < len(arr2):
        if arr1[lp] < arr2[rp]:
            diff = arr2[rp] - arr1[lp]
            lp += 1
        elif arr1[lp] > arr2[rp]:
            diff = arr1[lp] - arr2[rp]
            rp += 1
        else: # if both equal
            return [arr1[lp], arr2[rp]]

        if diff < smallsum:
            smallsum = diff
            pair = [arr1[lp], arr2[rp]]

    return pair

```