def minSubArrayLen(target, nums):
    left = 0
    minLen = 99999999
    currSum = 0

    for right in range(len(nums)):
        currSum += nums[right]

        while currSum - nums[left] >= target:
            currSum -= nums[left]
            left += 1

            if right - left + 1 < minLen:
                minLen = right - left + 1

    if currSum < target:
        return 0
    
    print(currSum)

    print(minLen)
        
    return minLen


minSubArrayLen(15, [1,2,3,4,5])