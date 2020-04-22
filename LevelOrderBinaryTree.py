class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        l1 = []
        l2 = []
        q = []
        if root is None:
            return []
        q.append(root)
        while q:
            n = len(q)
            while(n > 0):
                temp = q.pop(0)
                l2.append(temp.val)
                if temp.left:
                    q.append(temp.left)
                if temp.right:
                    q.append(temp.right)
                n -= 1
            l1.append(l2)
            l2 = []
        return l1 
        