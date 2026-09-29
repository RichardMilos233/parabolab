"""Read-only source and frozen-configuration checks; makes no E5 acquisitions."""

from __future__ import annotations

import ast
import inspect
import json
from pathlib import Path

import numpy as np

import experiment
from experiment import ChargedOpaque, CELLS
import smooth_field


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    frozen = [
        (0, 0.01, 3, 0.5, 0.0, 1, "cosine_mode_1"),
        (1, 0.01, 3, 0.5, 0.25, 1, "cosine_mode_1"),
        (2, 0.01, 3, 0.5, 0.25, 2, "constant"),
        (3, 0.01, 3, 0.5, 0.0, 3, "constant"),
        (4, 0.01, 5, 0.1, 0.25, 1, "cosine_mode_1"),
        (5, 0.01, 5, 0.1, 0.25, 2, "constant"),
        (6, 0.1, 3, 0.5, 0.0, 1, "cosine_mode_1"),
        (7, 0.1, 3, 0.5, 0.25, 1, "cosine_mode_1"),
        (8, 0.1, 3, 0.5, 0.25, 2, "constant"),
        (9, 0.1, 3, 0.5, 0.0, 3, "constant"),
        (10, 0.1, 5, 0.1, 0.25, 1, "cosine_mode_1"),
        (11, 0.1, 5, 0.1, 0.25, 2, "constant"),
    ]
    actual = [
        (
            cell.index,
            cell.kappa,
            cell.degree,
            cell.tau,
            cell.base,
            cell.derivative_order,
            cell.direction,
        )
        for cell in CELLS
    ]
    require(actual == frozen, "twelve-cell order differs from protocol")
    require(np.__version__ == "2.4.6", f"unexpected NumPy version {np.__version__}")
    require(experiment.verify_frozen_sources() != {}, "frozen source hashes were not checked")

    core_path = Path(smooth_field.__file__)
    core_text = core_path.read_text()
    core_tree = ast.parse(core_text)
    sample = next(
        node
        for node in core_tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "sample_field"
    )
    parameters = [argument.arg for argument in sample.args.args]
    require("known_evaluator" in parameters and "opaque_v" in parameters, "sampler API boundary changed")
    require("cell" not in parameters and "direction" not in parameters, "harness leaked into sampler API")
    require("reference_for_cell" not in core_text, "analytic reference leaked into core sampler")
    require("DELTA" not in core_text, "synthetic perturbation magnitude leaked into core sampler")

    charged_source = inspect.getsource(ChargedOpaque.__call__)
    charge_offset = charged_source.index("charge_oracle")
    callback_offset = charged_source.index("__raw_callback")
    require(charge_offset < callback_offset, "opaque callback occurs before durable charge")
    require("PCG64DXSM" in inspect.getsource(smooth_field.make_generator), "wrong bit generator")
    require("shuffle=True" in inspect.getsource(smooth_field.sample_given_tree), "tuple API changed")
    require("np.mod" in inspect.getsource(smooth_field.sample_given_tree), "torus reduction missing")
    require("edge_gaussians" in inspect.getsource(smooth_field.prepare_gaussian), "edge law missing")

    references = experiment.reference_records()
    require(len(references) == 12, "not all cell references were evaluated")
    require(
        all(record["nonzero_coefficient_index"] in (0, 1) for record in references),
        "reference has an unexpected nonzero mode",
    )
    require(
        all(record["binary64"] != 0.0 for record in references),
        "frozen analytic reference unexpectedly rounded to zero",
    )
    print(
        json.dumps(
            {
                "status": "passed",
                "checks": 15,
                "numpy_version": np.__version__,
                "cell_count": len(CELLS),
                "reference_count": len(references),
                "opaque_calls": 0,
                "official_executed": False,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
