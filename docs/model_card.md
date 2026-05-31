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
| Tracker | SORT with IoU matching |

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

## Evaluation Summary

The repository includes example TrackEval result tables and screenshots under
`result_examples/`. The headline combined metrics currently shown in the README
are:

| Split | HOTA | MOTA | IDF1 |
| --- | ---: | ---: | ---: |
| Car combined | 82.544 | 91.642 | 90.326 |
| Pedestrian combined | 69.723 | 77.394 | 85.963 |

These results should be interpreted as a record of this pipeline on selected
KITTI tracking sequences, not as a broad benchmark claim. Exact reproduction
requires the same local data, checkpoint, score threshold, tracker settings, and
TrackEval preparation.

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
- The C++ app currently assumes the exported model contract used by
  `tools_py/export_and_verify.py`.

## Intended Use

This model is intended for:

- Demonstrating a training-to-deployment perception workflow
- Producing qualitative detection and tracking demos
- Generating CSV outputs for downstream evaluation
- Supporting interview discussion around model export, inference, tracking, and
  reproducibility tradeoffs

It is not intended for safety-critical perception, autonomous driving deployment,
or claims of state-of-the-art KITTI performance.

## Reproduction Notes

To reproduce the model path:

1. Prepare the KITTI 2D detection dataset locally.
2. Run or adapt `src_python/train.ipynb`.
3. Place the checkpoint at `weights/best_model.pth`.
4. Export with `tools_py/export_and_verify.py`.
5. Run the C++ app against KITTI tracking image sequences.
6. Record the exact checkpoint, score threshold, input size, and tracker
   settings with any reported metrics.
