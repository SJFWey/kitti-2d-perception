from pathlib import Path
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from configs.local.config_utils import load_local_tools_config
from configs.public.config_utils import cfg_get, cfg_get_list, resolve_path


LOCAL_TOOL_SCRIPTS = (
    "local_tools/prepare_trackeval_kitti.py",
    "local_tools/train_v1.py",
    "local_tools/train_v2.py",
)


class LocalToolsConfigImportTests(unittest.TestCase):
    def test_local_tools_config_loads_from_repo_root(self) -> None:
        cfg = load_local_tools_config(REPO_ROOT)

        sequences = cfg_get_list(
            cfg,
            "trackeval_kitti",
            "sequences",
            ["0011", "0012", "0013"],
        )
        weights_dir = cfg_get(
            cfg,
            "paths",
            "weights_dir",
            str,
            "weights",
        )

        self.assertEqual(["0011", "0012", "0013"], sequences)
        self.assertEqual(REPO_ROOT / "weights", resolve_path(REPO_ROOT, weights_dir))

    def test_local_tools_do_not_use_bare_config_utils_imports(self) -> None:
        for script in LOCAL_TOOL_SCRIPTS:
            with self.subTest(script=script):
                source = (REPO_ROOT / script).read_text(encoding="utf-8")

                self.assertNotIn("from config_utils import", source)
                self.assertIn("configs.local.config_utils", source)


if __name__ == "__main__":
    unittest.main()
