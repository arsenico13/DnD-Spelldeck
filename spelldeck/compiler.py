import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from spelldeck.spells_data import PACKAGE_ROOT


DEFAULT_PRINTABLE_TEX = PACKAGE_ROOT / "tex" / "printable.tex"
DEFAULT_OUTPUT_PDF = PACKAGE_ROOT / "tex" / "printable.pdf"


@dataclass
class LatexCompileResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str
    output_pdf: Path

    @property
    def succeeded(self):
        return self.returncode == 0


def ensure_latexmk_available():
    latexmk_path = shutil.which("latexmk")
    if latexmk_path is None:
        raise RuntimeError("`latexmk` is not available in PATH.")

    return latexmk_path


def build_latexmk_command(printable_tex=DEFAULT_PRINTABLE_TEX):
    printable_path = Path(printable_tex)
    cards_tex = printable_path.parent / "cards.tex"

    # Keep the historical invocation so the generated auxiliary files land in
    # the same place as the existing shell workflow.
    return [
        "latexmk",
        "-xelatex",
        "-cd",
        str(cards_tex.relative_to(PACKAGE_ROOT)),
        str(printable_path.relative_to(PACKAGE_ROOT)),
    ]


def compile_spell_pdf(printable_tex=DEFAULT_PRINTABLE_TEX, output_pdf=DEFAULT_OUTPUT_PDF):
    ensure_latexmk_available()
    command = build_latexmk_command(printable_tex)
    completed = subprocess.run(
        command,
        cwd=PACKAGE_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    return LatexCompileResult(
        command=command,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
        output_pdf=Path(output_pdf),
    )

