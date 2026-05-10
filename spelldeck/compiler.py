import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from spelldeck.spells_data import PACKAGE_ROOT


DEFAULT_PRINTABLE_TEX = PACKAGE_ROOT / "tex" / "printable.tex"
DEFAULT_OUTPUT_PDF = PACKAGE_ROOT / "tex" / "printable.pdf"
DEFAULT_ITEMS_PRINTABLE_TEX = PACKAGE_ROOT / "tex" / "printable_items.tex"
DEFAULT_ITEMS_OUTPUT_PDF = PACKAGE_ROOT / "tex" / "printable_items.pdf"
DEFAULT_ITEMS_ONEPAGE_TEX = PACKAGE_ROOT / "tex" / "printable_onepage.tex"
DEFAULT_ITEMS_ONEPAGE_OUTPUT_PDF = PACKAGE_ROOT / "tex" / "printable_onepage.pdf"
DEFAULT_SPELLS_DRIVER_TEX = PACKAGE_ROOT / "tex" / "cards.tex"
DEFAULT_ITEMS_DRIVER_TEX = PACKAGE_ROOT / "tex" / "items_cards.tex"


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


def build_latexmk_command(printable_tex=DEFAULT_PRINTABLE_TEX, driver_tex=DEFAULT_SPELLS_DRIVER_TEX):
    printable_path = Path(printable_tex)
    driver_path = Path(driver_tex)

    # Keep the historical invocation so the generated auxiliary files land in
    # the same place as the existing shell workflow.
    return [
        "latexmk",
        "-xelatex",
        "-cd",
        str(driver_path.relative_to(PACKAGE_ROOT)),
        str(printable_path.relative_to(PACKAGE_ROOT)),
    ]


def compile_latex_pdf(
    printable_tex=DEFAULT_PRINTABLE_TEX,
    output_pdf=DEFAULT_OUTPUT_PDF,
    driver_tex=DEFAULT_SPELLS_DRIVER_TEX,
):
    ensure_latexmk_available()
    command = build_latexmk_command(printable_tex, driver_tex=driver_tex)
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


def compile_spell_pdf(
    printable_tex=DEFAULT_PRINTABLE_TEX,
    output_pdf=DEFAULT_OUTPUT_PDF,
):
    return compile_latex_pdf(
        printable_tex=printable_tex,
        output_pdf=output_pdf,
        driver_tex=DEFAULT_SPELLS_DRIVER_TEX,
    )


def compile_items_pdf(
    printable_tex=DEFAULT_ITEMS_PRINTABLE_TEX,
    output_pdf=DEFAULT_ITEMS_OUTPUT_PDF,
):
    return compile_latex_pdf(
        printable_tex=printable_tex,
        output_pdf=output_pdf,
        driver_tex=DEFAULT_ITEMS_DRIVER_TEX,
    )


def compile_single_page_items_pdf(
    printable_tex=DEFAULT_ITEMS_ONEPAGE_TEX,
    output_pdf=DEFAULT_ITEMS_ONEPAGE_OUTPUT_PDF,
):
    return compile_latex_pdf(
        printable_tex=printable_tex,
        output_pdf=output_pdf,
        driver_tex=DEFAULT_ITEMS_DRIVER_TEX,
    )
