# Model Card

## Overview

This project uses a Faster R-CNN ResNet50-FPN V2 detector as a baseline for a
KITTI-style 2D perception pipeline. The detector is trained in PyTorch, exported
to ONNX, and consumed by the C++ ONNX Runtime application.

The model is not presented as a production-quality perception model. It is used
to demonstrate the engineering workflow from training to C++ inference,
tracking, visualization, and TrackEval-style reporting.

## Model Details

| Item | Value |
| --- | --- |
| Architecture | Faster R-CNN ResNet50-FPN V2 |
| Framework | PyTorch / torchvision |
| Deployment format | ONNX |
| Runtime | ONNX Runtime C++ |
| Input size | 384 x 1248 |
| Foreground classes | Car, Pedestrian, Cyclist |
| Background class | 0 |
| Default score threshold | 0.8 |
| Tracker | Class-aware SORT-style tracker with IoU matching |

The class ids used by the app are:

```text
0 = background
1 = Car
2 = Pedestrian
3 = Cyclist
```

## Training Data And Workflow

The training workflow is tracked in `src_python/train.ipynb`. It expects the
KITTI 2D object detection dataset and reads labels for Car, Pedestrian, and
Cyclist. The original training run was performed in Colab, then the resulting
checkpoint was exported to ONNX for local C++ inference.

Datasets and checkpoints are not committed:

```text
data/      # local KITTI data
weights/   # PyTorch checkpoints
models/    # exported ONNX models
```

## Evaluation Summary And Scope

The repository includes archived TrackEval result tables and screenshots under
`result_examples/`. The preserved three-sequence subset summary is:

| Split | HOTA | MOTA | IDF1 |
| --- | ---: | ---: | ---: |
| Car combined | 82.544 | 91.642 | 90.326 |
| Pedestrian combined | 69.723 | 77.394 | 85.963 |

These results cover only KITTI tracking training sequences 0011, 0012, and
0013. The exact checkpoint digest, TrackEval revision, and conversion script
were not preserved, so the tables cannot be reproduced from a clean clone and
must not be compared with official KITTI leaderboard results. The training
notebook also uses a custom validation AP implementation rather than the
official KITTI object-detection metric. See
[evaluation_protocol.md](evaluation_protocol.md).

## Known Limitations

- Small or distant objects are frequently missed.
- Occlusion and truncation can reduce detection confidence and tracking
  stability.
- Cyclist examples are less represented than cars, so class quality is less
  reliable.
- The detector is trained as a compact baseline, not heavily tuned for maximum
  mAP.
- SORT uses motion and IoU association only; it does not use appearance
  embeddings, so identity switches can happen in crowded or crossing scenes.
- This implementation is not a verbatim reproduction of original SORT: it
  enforces class-consistent matching and uses class-dependent Kalman noise
  scales. These heuristic settings have not been supported by an ablation.
- The C++ app currently assumes the exported model contract used by
  `tools_py/export_and_verify.py`.

## Intended Use

This model is intended for:

- Demonstrating a training-to-deployment perception workflow
- Producing qualitative detection and tracking demos
- Generating CSV outputs for downstream evaluation
- Studying model export, inference, tracking, and reproducibility tradeoffs

It is not intended for safety-critical perception, autonomous driving deployment,
or claims of state-of-the-art KITTI performance.

## Reproduction Notes

To reproduce the model path:

1. Prepare the KITTI 2D detection dataset locally.
2. Run or adapt `src_python/train.ipynb`.
3. Place the checkpoint at `weights/best_model.pth`.
4. Export with `tools_py/export_and_verify.py`.
5. Run the C++ app against KITTI tracking image sequences.
6. Record the exact checkpoint digest, score threshold, input size, tracker
   settings, evaluated sequences, TrackEval revision, and conversion command
   with any newly reported metrics.
