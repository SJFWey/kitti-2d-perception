# Evaluation Protocol And Evidence Boundaries

This repository contains two different kinds of evaluation. They should not be
interpreted as the same benchmark.

## Training Validation Metric

`src_python/train.ipynb` uses a deterministic random image split with seed 42.
The validation code implements a compact, project-local AP calculation:

- classes: Car, Pedestrian, and Cyclist
- score filter: 0.05
- at most 100 predictions per image
- 101-point interpolated precision
- IoU thresholds from 0.50 to 0.95 in steps of 0.05

This metric is useful for choosing a checkpoint within this training workflow.
It is **not** the official KITTI object-detection metric. In particular, it does
not apply KITTI difficulty levels, minimum object heights, or `DontCare`
handling. The training plot is therefore labeled as a custom validation AP
result and should not be compared with the KITTI leaderboard.

## Archived Tracking Subset

`result_examples/TrackEval_results.md` preserves the output of an older local
TrackEval run on KITTI tracking training sequences 0011, 0012, and 0013. This is
a three-sequence development subset, not the full KITTI tracking benchmark.

The exact checkpoint digest, TrackEval revision, and CSV-to-KITTI conversion
script from that run were not preserved. Consequently:

- the tables are retained as historical engineering evidence only;
- they are not reproducible from a clean clone of this repository;
- they must not be presented as official KITTI benchmark or leaderboard
  results;
- they should not be used to compare this tracker with published methods.

Future reported runs should include the evaluated sequence list, checkpoint
SHA-256, application config, TrackEval commit, conversion command, and generated
tracker files.

## What A Clean Clone Can Verify

A clean clone can currently verify the public configuration loader and
repository contracts with:

```bash
uv run python -m unittest discover -s tests
```

Full model export, C++ inference, and tracking evaluation additionally require
local KITTI data, a trained checkpoint, ONNX Runtime C++ libraries, and CLI11.
