# SPDX-License-Identifier: GPL-3.0-or-later
"""Where OpenExample keeps its files, in which language it speaks, and what start() says. Every folder is
a temporary one, named by the variables every Open3D app reads."""

import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import openexample
from openexample import folders


class Folders(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.settings = self.root / "settings"
        self.data = self.root / "data"
        variables = {"OPEN3D_SETTINGS_DIR": str(self.settings), "OPEN3D_DATA_DIR": str(self.data)}
        patcher = mock.patch.dict(os.environ, variables)
        patcher.start()
        self.addCleanup(patcher.stop)

    def choose(self, language):
        """The shared preference, as the launcher or another app keeps it."""
        self.settings.mkdir(exist_ok=True)
        (self.settings / "settings.json").write_text(json.dumps({"language": language}), encoding="utf-8")

    def test_the_folders_are_named_after_the_app(self):
        self.assertEqual(folders.settings_dir(), self.settings / "OpenExample")
        self.assertEqual(folders.data_dir(), self.data / "OpenExample")

    def test_without_any_variable_there_is_no_folder(self):
        with mock.patch.dict(os.environ, clear=True):
            self.assertIsNone(folders.settings_dir())
            self.assertIsNone(folders.data_dir())

    def test_the_shared_language_is_the_one_shown(self):
        self.choose("es")
        self.assertEqual(folders.language(), "es")
        self.choose("en")
        self.assertEqual(folders.language(), "en")

    def test_start_says_where_the_files_go_in_the_shared_language(self):
        self.choose("es")
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            line = openexample.start()
        self.assertEqual(printed.getvalue(), line + "\n")
        expected = (
            f"OpenExample {openexample.__version__}: Idioma: español; "
            f"Ajustes: {self.settings / 'OpenExample'}; Otros archivos: {self.data / 'OpenExample'}"
        )
        self.assertEqual(line, expected)

    def test_start_creates_nothing(self):
        self.choose("en")
        with contextlib.redirect_stdout(io.StringIO()):
            openexample.start()
        self.assertEqual(sorted(path.name for path in self.root.iterdir()), ["settings"])
        self.assertEqual([path.name for path in self.settings.iterdir()], ["settings.json"])

    def test_a_missing_folder_is_said(self):
        self.assertEqual(
            folders.describe("en", None, None), "Language: English\nSettings: (no folder)\nOther files: (no folder)"
        )
        self.assertTrue(folders.describe("es", None, None).endswith("Otros archivos: (ninguna carpeta)"))


if __name__ == "__main__":
    unittest.main()
