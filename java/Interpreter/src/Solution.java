import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Stack;

public class Solution {
    static class Node {
        int value;
        Node next;

        public Node(int value) {
            this.value = value;
        }
    }

    /*
    一个链表，假设第一个节点我们定为下标为1，第二个为2，那么下标为奇数的结点是升序排序，偶数的结点是降序排序，如何让整个链表有序？
     */
    Node solve(Node head) {
        if (head == null)
            return null;

        Node odd = new Node(-1);
        Node p = odd;

        Node even = new Node(-1);

        while (head != null) {
            Node first = head;
            Node second = first.next;

            head = second == null? null:second.next;

            // 尾插
            p.next = first;
            p = first;

            // 头插
            if (second != null) {
                second.next = even.next;
                even.next = second;
            }
        }
        p.next = null;

        Node result = new Node(-1);
        p = result;
        // 归并
        odd = odd.next;
        even = even.next;

        while (odd != null && even != null) {
            if (odd.value < even.value) {
                p.next = odd;
                odd = odd.next;
            } else {
                p.next = even;
                even = even.next;
            }

            p = p.next;
        }

        if (odd != null)
            p.next = odd;

        if (even != null)
            p.next = even;

        return result.next;
    }



    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        if (root == null)
            return null;

        TreeNode left = lowestCommonAncestor(root.left, p, q);
        TreeNode right = lowestCommonAncestor(root.right, p, q);

        if (root.val == p.val || root.val == q.val)
            return root;

        if (left != null && right != null)
            return root;

        if (left != null)
            return left;

        if (right != null)
            return right;

        return null;
    }

    public boolean isCompleteTree(TreeNode root) {
        if (root == null)
            return true;

        LinkedList<TreeNode> queue = new LinkedList<>();
        queue.add(root);
        boolean seenNull = false;

        while (!queue.isEmpty()) {
            TreeNode node = queue.poll();

            if (node != null) {
                if (seenNull)
                    return false;
                else {
                    queue.add(node.left);
                    queue.add(node.right);
                }
            } else
                seenNull = true;
        }

        return true;
    }

//    private List<List<Integer>> res = new ArrayList<>();
//    private List<Integer> mid = new ArrayList<>();
//    public List<List<Integer>> pathSum(TreeNode root, int sum) {
//        if (root == null)
//            return res;
//        dfs(root, 0, sum);
//
//        return res;
//    }
//
//    private void dfs(TreeNode node, int sum, int target) {
//        mid.add(node.val);
//
//        if (node.left == null && node.right == null) {
//            if (sum + node.val == target)
//                res.add(new ArrayList<>(mid));
//        } else {
//            if (node.left != null)
//                dfs(node.left, sum+node.val, target);
//
//            if (node.right != null)
//                dfs(node.right, sum+node.val, target);
//        }
//
//        mid.remove(mid.size()-1);
//    }


    public List<Integer> inorderTraversal(TreeNode root) {
        List<Integer> res = new ArrayList<>();
        if (root == null)
            return res;

        Stack<TreeNode> stack = new Stack<>();
        TreeNode p = root;

        // 为什么需要有p呢？
        // 回退的时候可以避免再次重复走过的路程
        while (p != null || !stack.isEmpty()) {
            while (p != null) {
                stack.push(p);
                p = p.left;
            }

            if (!stack.isEmpty()) {
                TreeNode node = stack.pop();
                res.add(node.val);
                if (node.right != null)
                    p = node.right;
            }
        }

        return res;
    }

    public List<Integer> postorderTraversal(TreeNode root) {
        List<Integer> res = new ArrayList<>();
        if (root == null)
            return res;

        Stack<TreeNode> stack = new Stack<>();
        stack.push(root);
        TreeNode pre = null;

        while (!stack.isEmpty()) {
            TreeNode node = stack.peek();
            if ((node.left == null && node.right == null) || (pre != null && (pre == node.left || pre == node.right))) {
                res.add(node.val);
                stack.pop();
                pre = node;
            } else {
                if (node.right != null)
                    stack.add(node.right);

                if (node.left != null)
                    stack.add(node.left);
            }
        }

        return res;
    }

    public List<Integer> preorderTraversal(TreeNode root) {
        List<Integer> res = new ArrayList<>();
        if (root == null)
            return res;

        Stack<TreeNode> stack = new Stack<>();
        stack.push(root);

        while (!stack.isEmpty()) {
            TreeNode node = stack.pop();
            while (node != null) {
                res.add(node.val);
                if (node.right != null)
                    stack.add(node.right);
                node = node.left;
            }
        }

        return res;
    }
}



class TreeNode {
   int val;
   TreeNode left;
   TreeNode right;
    TreeNode(int x) { val = x; }
}

