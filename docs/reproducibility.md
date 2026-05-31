# Reproducibility Guide

This project is intentionally lightweight. The repository contains source code,
configuration, tests, the training notebook, and small result examples. It does
not contain KITTI data, trained PyTorch checkpoints, ONNX weights, full runtime
outputs, or third-party binary packages.

## 1. Create The Python Environment

```bash
conda env create -f environment.yml
conda activate perception2d
```

The Python utilities cover training-notebook support, checkpoint export, ONNX
Runtime verification, and KITTI label visualization.

## 2. Prepare Data

For training, download the KITTI 2D object detection data and arrange it so the
notebook can find:

```text
data/kitti_detection/
  data_object_image_2/training/image_2/
  data_object_label_2/training/label_2/
```

For C++ tracking demos and TrackEval-style evaluation, arrange image sequences
under:

```text
data/kitti_tracking/
  images/
    0011/
      000000.png
      000001.png
```

KITTI data is not redistributed by this repository. Keep downloaded data under
`data/`, which is ignored by Git.

## 3. Train Or Provide A Checkpoint

The tracked training workflow is `src_python/train.ipynb`. It expects the KITTI
2D detection dataset and trains a Faster R-CNN ResNet50-FPN V2 detector with
three foreground classes:

```text
1 = Car
2 = Pedestrian
3 = Cyclist
```

The trained checkpoint should be placed at:

```text
weights/best_model.pth
```

Training was originally run in Colab, so exact wall-clock time and GPU behavior
depend on the runtime. Keep checkpoints under `weights/`, which is ignored by
Git.

## 4. Export ONNX

Export the PyTorch checkpoint to the ONNX model consumed by the C++ app:

```bash
python tools_py/export_and_verify.py \
  --weights-dir weights \
  --output-onnx models/best_model.onnx
```

If the checkpoint was saved in a format that requires full pickle loading, only
use this option for checkpoints you trust:

```bash
python tools_py/export_and_verify.py \
  --weights-dir weights \
  --output-onnx models/best_model.onnx \
  --allow-unsafe-load
```

The exporter also runs an ONNX Runtime consistency check against the PyTorch
model on a dummy input.

## 5. Build The C++ App

Install or provide:

- CMake >= 3.20
- A C++17 compiler
- OpenCV C++ libraries
- ONNX Runtime C++ package
- CLI11 headers

Recommended local dependency layout:

```text
third_party/
  onnxruntime/
    include/onnxruntime_cxx_api.h
    lib/libonnxruntime.so
  cli11/
    include/CLI/CLI.hpp
```

Then build:

```bash
cmake -S . -B build \
  -DORT_ROOT=/path/to/onnxruntime \
  -DCLI11_ROOT=/path/to/CLI11
cmake --build build -j
```

`third_party/` and `build/` are ignored by Git.

## 6. Run Detection And Tracking

```bash
./build/perception2d_app \
  --input data/kitti_tracking/images/0011 \
  --sequence 0011 \
  --model-path models/best_model.onnx \
  --output output/0011 \
  --score-threshold 0.8 \
  --max-frames 200
```

Expected output:

```text
output/0011/
  detections.csv
  tracks.csv
  vis/
```

`output/` is ignored by Git. The GIF and MP4 previews in `result_examples/` are
compressed presentation assets generated from local runs, not full output
archives.

## 7. TrackEval Reporting

The public repository includes result screenshots and tables in
`result_examples/`. Full TrackEval reproduction requires local KITTI tracking
ground truth and helper tooling that is kept outside the public release surface.

Use the existing CSV outputs as the stable boundary:

```text
detections.csv
tracks.csv
```

When reporting metrics, include the evaluated sequences, model checkpoint,
score threshold, tracker settings, and whether the result is from a local or
published run.

## 8. Verification

Run the lightweight unit tests:

```bash
uv run python -m unittest discover -s tests
```

These tests do not require datasets, weights, ONNX Runtime C++ libraries, or
local helper scripts. A clean clone should still make it clear which external
assets are missing and where to place them.
