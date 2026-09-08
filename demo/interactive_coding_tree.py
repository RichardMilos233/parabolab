"""Interactive Coding-Tree Playground and Inspection Tool.

This script lets you interactively inspect, step through, and visualize the
coding-tree random variable H = H(T_{t,x,code}).

Usage:
    # 1. Run full interactive demonstration:
    python demo/interactive_coding_tree.py

    # 2. Or import interactively in python (python -i demo/interactive_coding_tree.py):
    >>> pde = allen_cahn_wave_1d(T=0.1)
    >>> tree = inspect_one_tree(pde, x=0.0)
    >>> print_tree(tree)
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional

import numpy as np

from parabolab.library import allen_cahn_wave_1d, merton_hjb
from parabolab.mechanism import Code, Id, SemilinearMechanism
from parabolab.tree import default_rate


@dataclass
class TreeNode:
    """Detailed node in an inspected coding tree."""
    node_id: int
    depth: int
    t_birth: float
    x_birth: float
    code: Code
    is_leaf: bool
    tau: float
    weight: float
    x_death: float
    t_death: float
    terminal_val: Optional[float] = None
    tuple_chosen: Optional[tuple] = None
    children: List["TreeNode"] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []


def inspect_one_tree(
    pde,
    x: float = 0.0,
    t: float = 0.0,
    rate: Optional[float] = None,
    rng: Optional[np.random.Generator] = None,
) -> tuple[float, TreeNode]:
    """Sample one tree and record the full hierarchical tree structure for inspection."""
    if rng is None:
        rng = np.random.default_rng()
    if rate is None:
        rate = default_rate(pde.T)
    mech = getattr(pde, "mechanism", None) or SemilinearMechanism

    node_counter = [0]

    def _build(cur_t: float, cur_x: float, cur_code: Code, depth: int) -> tuple[float, TreeNode]:
        idx = node_counter[0]
        node_counter[0] += 1

        tau = rng.exponential(1.0 / rate)
        remaining = pde.T - cur_t

        if tau > remaining:
            # Leaf node
            if remaining > 0.0:
                w = rng.normal(0.0, math.sqrt(remaining))
            else:
                w = 0.0
            x_leaf = cur_x + w
            term_val = mech.terminal(cur_code, pde, x_leaf)
            surv_weight = math.exp(rate * remaining)
            h = term_val * surv_weight
            node = TreeNode(
                node_id=idx,
                depth=depth,
                t_birth=cur_t,
                x_birth=cur_x,
                code=cur_code,
                is_leaf=True,
                tau=tau,
                weight=surv_weight,
                x_death=x_leaf,
                t_death=pde.T,
                terminal_val=term_val,
            )
            return h, node

        # Branching interior node
        tuples = mech.tuples(cur_code)
        z = tuples[rng.integers(len(tuples))] if len(tuples) > 1 else tuples[0]
        xb = cur_x + rng.normal(0.0, math.sqrt(tau))
        branch_weight = len(tuples) * math.exp(rate * tau) / rate

        node = TreeNode(
            node_id=idx,
            depth=depth,
            t_birth=cur_t,
            x_birth=cur_x,
            code=cur_code,
            is_leaf=False,
            tau=tau,
            weight=branch_weight,
            x_death=xb,
            t_death=cur_t + tau,
            tuple_chosen=z,
        )

        h = branch_weight
        for child_code in z:
            child_h, child_node = _build(cur_t + tau, xb, child_code, depth + 1)
            h *= child_h
            node.children.append(child_node)

        return h, node

    h_val, root_node = _build(t, x, Id(), 0)
    return h_val, root_node


def print_tree(node: TreeNode, indent: str = ""):
    """Pretty-print the full hierarchy of a coding tree."""
    prefix = f"{indent}[Node {node.node_id} | Depth {node.depth}] "
    if node.is_leaf:
        print(
            f"{prefix}LEAF: Code={node.code} | t={node.t_birth:.3f}->{node.t_death:.3f} | "
            f"x={node.x_death:.3f} | phi={node.terminal_val:.4f} | "
            f"surv_weight={node.weight:.4f} (1/Fbar) => val={node.terminal_val*node.weight:.4f}"
        )
    else:
        print(
            f"{prefix}BRANCH: Code={node.code} | t={node.t_birth:.3f}->{node.t_death:.3f} (tau={node.tau:.3f}) | "
            f"xb={node.x_death:.3f} | |M|={node.weight * default_rate(0.1) / math.exp(node.tau * default_rate(0.1)):.0f} | "
            f"branch_weight={node.weight:.4f} (|M|/rho)"
        )
        for c in node.children:
            print_tree(c, indent + "   |-- ")


def demo_interactive():
    print("=" * 75)
    print("CODING TREE 交互式单树可视化 (Interactive Single-Tree Inspection)")
    print("=" * 75)
    pde = allen_cahn_wave_1d(T=0.2)
    print(f"PDE: {pde.name}")
    print("随机生成 3 棵不同的 coding tree，并打印它们内部的节点、分枝和权重：\n")

    rng = np.random.default_rng(42)
    for i in range(1, 4):
        print(f"--- [Tree Sample #{i}] ---")
        h_val, tree = inspect_one_tree(pde, x=0.0, rate=1.0, rng=rng)
        print_tree(tree)
        print(f"==> 此树最终返回的随机变量标量样本 H = {h_val:.6f}\n")

    print("=" * 75)
    print("核心观察结论:")
    print("1. 叶节点 (LEAF): 计算已知终端 phi(X_T)，乘以生存概率倒数 1/F_bar(T - t_birth)。")
    print("2. 分枝节点 (BRANCH): 随机抽取算子 tuple，在死亡位置 xb 繁衍子节点，乘上 |M|/rho(tau)。")
    print("3. 全树相乘: H 就是全树所有内部节点权重与所有叶子值的乘积。")
    print("4. 无偏性: 单棵树 H 波动很大，但均值严格收敛于 PDE 的真解 u(t, x)！")
    print("=" * 75)


if __name__ == "__main__":
    demo_interactive()
