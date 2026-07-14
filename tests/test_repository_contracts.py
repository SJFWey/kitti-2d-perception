import json
from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class RepositoryContractTests(unittest.TestCase):
    def test_local_document_links_resolve(self) -> None:
        documents = [
            REPO_ROOT / "README.md",
            REPO_ROOT / "docs" / "model_card.md",
            REPO_ROOT / "docs" / "reproducibility.md",
            REPO_ROOT / "docs" / "evaluation_protocol.md",
            REPO_ROOT / "result_examples" / "TrackEval_results.md",
        ]

        for document in documents:
            text = document.read_text(encoding="utf-8")
            for target in re.findall(r"]\(([^)]+)\)", text):
                if "://" in target or target.startswith(("#", "mailto:")):
                    continue
                path = target.split("#", 1)[0]
                with self.subTest(document=document.name, target=target):
                    self.assertTrue((document.parent / path).resolve().exists())

    def test_generated_and_private_paths_are_ignored(self) -> None:
        ignore_text = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
        required_patterns = {
            "__pycache__/",
            "data/",
            "weights/",
            "models/",
            "output/",
            "build/",
            "third_party/",
        }
        for pattern in required_patterns:
            with self.subTest(pattern=pattern):
                self.assertIn(pattern, ignore_text)

    def test_training_checkpoint_matches_exporter_contract(self) -> None:
        notebook = json.loads(
            (REPO_ROOT / "src_python" / "train.ipynb").read_text(encoding="utf-8")
        )
        source = "".join(
            line
            for cell in notebook["cells"]
            for line in cell.get("source", [])
        )

        self.assertIn('CHECKPOINT_DIR = Path("weights")', source)
        self.assertIn('best_path = checkpoint_dir / "best_model.pth"', source)
        self.assertIn('ARTIFACT_DIR = Path("output/train_v2")', source)
        self.assertNotIn("{YOUR_PROJECT}", source)

        exporter = (
            REPO_ROOT / "tools_py" / "export_and_verify.py"
        ).read_text(encoding="utf-8")
        self.assertIn('weights_dir / "best_model.pth"', exporter)

    def test_archived_metrics_are_not_presented_as_benchmark_results(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        protocol = (
            REPO_ROOT / "docs" / "evaluation_protocol.md"
        ).read_text(encoding="utf-8")

        self.assertIn("docs/evaluation_protocol.md", readme)
        self.assertIn("not reproducible from a clean clone", readme)
        self.assertIn("official KITTI object-detection metric", protocol)
        self.assertIn("not the full KITTI tracking benchmark", protocol)


if __name__ == "__main__":
    unittest.main()
