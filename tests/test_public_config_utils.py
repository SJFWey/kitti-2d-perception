from pathlib import Path
import tempfile
import unittest

import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from configs.public.config_utils import (  # noqa: E402
    cfg_get,
    cfg_get_bool,
    cfg_get_list,
    load_public_config,
    resolve_path,
)


class PublicConfigUtilsTests(unittest.TestCase):
    def test_default_public_config_loads_from_repo_root(self) -> None:
        cfg = load_public_config(REPO_ROOT)

        output_root = cfg_get(cfg, "paths", "output_root", str, "")
        class_ids = cfg_get_list(cfg, "perception2d_app", "class_ids", [])
        score_threshold = cfg_get(
            cfg,
            "perception2d_app",
            "score_threshold",
            float,
            -1.0,
        )
        save_vis = cfg_get_bool(cfg, "perception2d_app", "save_vis", True)

        self.assertEqual("output", output_root)
        self.assertEqual(["1", "2", "3"], class_ids)
        self.assertEqual(0.8, score_threshold)
        self.assertTrue(save_vis)
        self.assertEqual(REPO_ROOT / "output", resolve_path(REPO_ROOT, output_root))

    def test_explicit_config_overrides_public_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            override_path = Path(tmp) / "override.ini"
            override_path.write_text(
                "\n".join(
                    [
                        "[paths]",
                        "output_root = custom_output",
                        "",
                        "[perception2d_app]",
                        "score_threshold = 0.5",
                        "class_ids = 1,3",
                        "save_vis = false",
                    ]
                ),
                encoding="utf-8",
            )

            cfg = load_public_config(
                REPO_ROOT,
                config_path=override_path,
                required=True,
            )

        self.assertEqual("custom_output", cfg_get(cfg, "paths", "output_root", str, ""))
        self.assertEqual(
            ["1", "3"],
            cfg_get_list(cfg, "perception2d_app", "class_ids", []),
        )
        self.assertEqual(
            0.5,
            cfg_get(cfg, "perception2d_app", "score_threshold", float, -1.0),
        )
        self.assertFalse(cfg_get_bool(cfg, "perception2d_app", "save_vis", True))


if __name__ == "__main__":
    unittest.main()
