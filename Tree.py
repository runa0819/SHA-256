import json
from typing import List, Union

class TreeNode:
    def __init__(self, value: Union[int, None], index: Union[int, None] = None, left=None, right=None):
        self.value = value
        self.index = index
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode(value={self.value}, index={self.index}, left={self.left}, right={self.right})"

def build_sum_tree(values: List[int]) -> TreeNode:
    """
    子ノードを足し算してツリーを構築する関数。
    初期の値は葉ノードとして扱う。
    """
    # 初期の葉ノードを作成（インデックス付き）
    nodes = [TreeNode(value, index=i) for i, value in enumerate(values)]

    # ツリーを構築（1つのノードが残るまで繰り返す）
    while len(nodes) > 1:
        new_nodes = []
        for i in range(0, len(nodes), 2):
            if i + 1 < len(nodes):
                # 2つのノードを1つに結合
                combined_value = nodes[i].value + nodes[i + 1].value
                new_node = TreeNode(combined_value, left=nodes[i], right=nodes[i + 1])
            else:
                # ノード数が奇数の場合は最後のノードをそのまま持ち越す
                new_node = nodes[i]
            new_nodes.append(new_node)
        nodes = new_nodes

    # 最後に残ったノードがルート
    return nodes[0]

def detect_difference(tree1: TreeNode, tree2: TreeNode) -> Union[int, None]:
    """
    2つのツリーを比較し、異なる葉ノードのインデックスを探索する関数。
    ノード同士を比較した回数も出力する。
    """
    comparison_count = 0

    def compare_nodes(node1: TreeNode, node2: TreeNode) -> Union[int, None]:
        nonlocal comparison_count
        

        # 両方のノードがNoneの場合
        if not node1 and not node2:
            return None
        comparison_count += 1
        # どちらかのノードがNone、または値が異なる場合
        if not node1 or not node2 or node1.value != node2.value:
            
            # 葉ノードの場合、そのインデックスを返す
            if node1 and node1.left is None and node1.right is None:
                return node1.index
            if node2 and node2.left is None and node2.right is None:
                return node2.index

            # 再帰的に異なるノードを探索
            left_difference = compare_nodes(node1.left, node2.left)
            if left_difference is not None:
                return left_difference
            right_difference = compare_nodes(node1.right, node2.right)
            if right_difference is not None:
                return right_difference
        
        return None

    difference = compare_nodes(tree1, tree2)
    print(f"ノード比較回数: {comparison_count}")
    return difference

def main():
    # 2つのJSONデータを用意（16個のデータで1つだけ異なる）
    json_data1 = json.dumps([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    json_data2 = json.dumps([0,1,2,3,4,5,6,7,8,9,10,11,12,13,114,15])

    # JSONデータを解析
    values1 = json.loads(json_data1)
    values2 = json.loads(json_data2)

    # データの検証（整数のリストであることを確認）
    if not all(isinstance(lst, list) and all(isinstance(x, int) for x in lst) for lst in [values1, values2]):
        print("無効なデータです: JSONは整数のリストである必要があります。")
        return

    # それぞれのツリーを構築
    root1 = build_sum_tree(values1)
    root2 = build_sum_tree(values2)

    # ツリーのルートノードを出力
    print("ツリー1のルート:", root1)
    print("ツリー2のルート:", root2)

    # 異なるノードを探索
    difference_index = detect_difference(root1, root2)
    if difference_index is not None:
        print("異なるデータのインデックス:", difference_index)
    else:
        print("2つの木は等しいです。")

if __name__ == "__main__":
    main()
