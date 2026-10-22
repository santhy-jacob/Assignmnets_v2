"""Run the suite once per browser and print/save a PASS/FAIL matrix.
Usage: python utils/run_matrix.py [extra pytest args, e.g. -m smoke --env qa]"""
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BROWSERS = ["chromium", "firefox", "webkit"]


def parse(xml_path: Path) -> dict[str, str]:
    results = {}
    for tc in ET.parse(xml_path).getroot().iter("testcase"):
        name = re.sub(r"\[(chromium|firefox|webkit)\]", "", tc.get("name", ""))
        key = f"{tc.get('classname', '').split('.')[-1]}::{name}"
        if tc.find("failure") is not None or tc.find("error") is not None:
            results[key] = "FAIL"
        elif tc.find("skipped") is not None:
            results[key] = "SKIP"
        else:
            results[key] = "PASS"
    return results


def main() -> None:
    extra = sys.argv[1:]
    (ROOT / "reports").mkdir(exist_ok=True)
    all_results: dict[str, dict[str, str]] = {}
    for b in BROWSERS:
        xml = ROOT / "reports" / f"junit-{b}.xml"
        subprocess.run([sys.executable, "-m", "pytest", "--browser", b, f"--junitxml={xml}", "-q", *extra], cwd=ROOT)
        if xml.exists():
            all_results[b] = parse(xml)
    tests = sorted({t for r in all_results.values() for t in r})
    lines = ["| Test | " + " | ".join(b.capitalize() for b in BROWSERS) + " |", "|---|" + "---|" * len(BROWSERS)]
    for t in tests:
        lines.append(f"| {t} | " + " | ".join(all_results.get(b, {}).get(t, "N/A") for b in BROWSERS) + " |")
    table = "\n".join(lines)
    (ROOT / "reports" / "browser_matrix.md").write_text(table + "\n", encoding="utf-8")
    print("\n" + table)


if __name__ == "__main__":
    main()
