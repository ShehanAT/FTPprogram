
from math import floor 

class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> TreeNode:
        if not nums:    
            return None 
        mid = floor(len(nums)/2)
        print(mid)
        root = TreeNode(nums[mid])
        root.right = self.sortedArrayToBST(nums[mid+1:])
        root.left = self.sortedArrayToBST(nums[:mid])
        return root 
        