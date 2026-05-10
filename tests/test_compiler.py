import unittest
from pathlib import Path
from unittest import mock

from spelldeck.compiler import (
    DEFAULT_OUTPUT_PDF,
    DEFAULT_PRINTABLE_TEX,
    build_latexmk_command,
    compile_spell_pdf,
    ensure_latexmk_available,
)


class TestCompiler(unittest.TestCase):
    def test_build_latexmk_command(self):
        command = build_latexmk_command()
        self.assertEqual(
            ["latexmk", "-xelatex", "-cd", "tex/cards.tex", "tex/printable.tex"],
            command,
        )

    @mock.patch("spelldeck.compiler.shutil.which", return_value="/usr/bin/latexmk")
    def test_ensure_latexmk_available(self, _which_mock):
        self.assertEqual("/usr/bin/latexmk", ensure_latexmk_available())

    @mock.patch("spelldeck.compiler.shutil.which", return_value=None)
    def test_ensure_latexmk_missing_raises(self, _which_mock):
        with self.assertRaises(RuntimeError):
            ensure_latexmk_available()

    @mock.patch("spelldeck.compiler.subprocess.run")
    @mock.patch("spelldeck.compiler.shutil.which", return_value="/usr/bin/latexmk")
    def test_compile_spell_pdf_success(self, _which_mock, run_mock):
        run_mock.return_value = mock.Mock(returncode=0, stdout="ok", stderr="")

        result = compile_spell_pdf()

        self.assertTrue(result.succeeded)
        self.assertEqual(0, result.returncode)
        self.assertEqual(DEFAULT_OUTPUT_PDF, result.output_pdf)
        run_mock.assert_called_once()

    @mock.patch("spelldeck.compiler.subprocess.run")
    @mock.patch("spelldeck.compiler.shutil.which", return_value="/usr/bin/latexmk")
    def test_compile_spell_pdf_failure(self, _which_mock, run_mock):
        run_mock.return_value = mock.Mock(returncode=12, stdout="", stderr="latex error")

        result = compile_spell_pdf(DEFAULT_PRINTABLE_TEX, Path("tex/printable.pdf"))

        self.assertFalse(result.succeeded)
        self.assertEqual(12, result.returncode)
        self.assertEqual("latex error", result.stderr)

