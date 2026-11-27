from pathlib import Path
import openpyxl
from pptx import Presentation

from src.ai_sop_generator import build_all_sops, parse_bpmn_process
from src.build_deliverables import (
    build_excel_process_review,
    build_powerpoint_pitch,
    render_process_visuals,
)

ROOT_DIR = Path(__file__).resolve().parent.parent


def test_bpmn_parsing_and_sop_generation():
    as_is = parse_bpmn_process(ROOT_DIR / "processes" / "bpmn" / "order_to_delivery_as_is.bpmn")
    to_be = parse_bpmn_process(ROOT_DIR / "processes" / "bpmn" / "order_to_delivery_to_be.bpmn")

    assert len(as_is["steps"]) == 5
    assert len(to_be["steps"]) == 5
    assert to_be["total_cycle_hours"] < as_is["total_cycle_hours"]

    sops = build_all_sops()
    assert len(sops) == 2
    assert all(
        p.exists() and "RACI Responsibility Matrix" in p.read_text(encoding="utf-8") for p in sops
    )


def test_excel_and_powerpoint_deliverables():
    imgs = render_process_visuals()
    assert len(imgs) == 2 and all(p.exists() for p in imgs)

    xlsx = build_excel_process_review()
    wb = openpyxl.load_workbook(xlsx)
    assert set(wb.sheetnames) == {"Executive_KPI_Dashboard", "AI_Documentation_ROI"}

    pptx = build_powerpoint_pitch(imgs)
    prs = Presentation(pptx)
    assert len(prs.slides) == 4
