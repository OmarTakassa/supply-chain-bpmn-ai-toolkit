from pathlib import Path
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import openpyxl
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Font, PatternFill
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

from src.ai_sop_generator import build_all_sops, parse_bpmn_process

ROOT_DIR = Path(__file__).resolve().parent.parent


def render_process_visuals() -> list[Path]:
    assets_dir = ROOT_DIR / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    as_is = parse_bpmn_process(ROOT_DIR / "processes" / "bpmn" / "order_to_delivery_as_is.bpmn")
    to_be = parse_bpmn_process(ROOT_DIR / "processes" / "bpmn" / "order_to_delivery_to_be.bpmn")

    # Visual 1: Swimlane BPMN Comparison Diagram (As-Is vs To-Be)
    fig, axes = plt.subplots(2, 1, figsize=(14, 7.2))
    configs = [
        (
            axes[0],
            as_is,
            "AS-IS Process Flow (Manual Email & Spreadsheet Handoffs — 62.0h Total)",
            "#FDEDEC",
            "#C0392B",
        ),
        (
            axes[1],
            to_be,
            "TO-BE Process Flow (ERP/EDI Integration & AI Exception Routing — 12.0h Total)",
            "#EAFAF1",
            "#1E8449",
        ),
    ]

    for ax, proc_data, title, box_fill, border_col in configs:
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 28)
        ax.axis("off")
        ax.set_title(title, fontsize=12, fontweight="bold", loc="left", color="#1B365D", pad=8)

        # Start event circle
        start_circle = patches.Circle(
            (3.5, 14), 2.0, facecolor="#2ECC71", edgecolor="#1B365D", lw=1.5
        )
        ax.add_patch(start_circle)
        ax.text(3.5, 9.2, "Start", ha="center", fontsize=8, fontweight="bold")

        steps = proc_data["steps"]
        n_steps = len(steps)
        start_x = 9.0
        usable_w = 81.0
        gap = 2.2
        box_w = (usable_w - gap * (n_steps - 1)) / n_steps

        prev_right = 5.5
        for idx, step in enumerate(steps):
            x0 = start_x + idx * (box_w + gap)
            rect = patches.FancyBboxPatch(
                (x0, 6.5),
                box_w,
                15.0,
                boxstyle="round,pad=0.4",
                facecolor=box_fill,
                edgecolor=border_col,
                linewidth=1.5,
            )
            ax.add_patch(rect)

            short_lane = step["lane"].split("&")[0].strip()
            short_name = step["step_name"][:34] + ("..." if len(step["step_name"]) > 34 else "")
            ax.text(
                x0 + box_w / 2,
                19.0,
                f"[{short_lane}]",
                ha="center",
                va="center",
                fontsize=7.5,
                fontweight="bold",
                color="#1B365D",
            )
            ax.text(
                x0 + box_w / 2,
                13.8,
                short_name,
                ha="center",
                va="center",
                fontsize=7.5,
                wrap=True,
            )
            ax.text(
                x0 + box_w / 2,
                8.3,
                f"{step['avg_cycle_hours']:.1f}h | Err {step['error_rate_pct']:.1f}%",
                ha="center",
                va="center",
                fontsize=7.5,
                fontweight="bold",
                color=border_col,
            )

            ax.annotate(
                "",
                xy=(x0 - 0.3, 14),
                xytext=(prev_right, 14),
                arrowprops=dict(arrowstyle="->", color="#34495E", lw=1.4),
            )
            prev_right = x0 + box_w + 0.3

        end_circle = patches.Circle(
            (95.5, 14), 2.0, facecolor="#E74C3C", edgecolor="#1B365D", lw=2.2
        )
        ax.add_patch(end_circle)
        ax.annotate(
            "",
            xy=(93.2, 14),
            xytext=(prev_right, 14),
            arrowprops=dict(arrowstyle="->", color="#34495E", lw=1.4),
        )
        ax.text(95.5, 9.2, "End", ha="center", fontsize=8, fontweight="bold")

    plt.tight_layout()
    p1 = assets_dir / "bpmn_as_is_vs_to_be.png"
    fig.savefig(p1, dpi=180)
    plt.close(fig)

    # Visual 2: Step-Level Cycle Time & Defect Rate Reduction Chart
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 4.8))
    stage_labels = [
        "1. Demand Sync",
        "2. Co-Packing PO",
        "3. Stock Realloc.",
        "4. Warehouse Pick",
        "5. Customs/Docs",
    ]
    as_is_hrs = [s["avg_cycle_hours"] for s in as_is["steps"]]
    to_be_hrs = [s["avg_cycle_hours"] for s in to_be["steps"]]

    x_pos = range(len(stage_labels))
    axes[0].bar(
        [x - 0.18 for x in x_pos], as_is_hrs, width=0.36, label="As-Is (Manual)", color="#C0392B"
    )
    axes[0].bar(
        [x + 0.18 for x in x_pos], to_be_hrs, width=0.36, label="To-Be (Automated)", color="#1E8449"
    )
    axes[0].set_xticks(list(x_pos))
    axes[0].set_xticklabels(stage_labels, rotation=15)
    axes[0].set_ylabel("Cycle Time (Hours)")
    axes[0].set_title("Cycle Time Reduction by Process Stage (-80.6% Total)", fontweight="bold")
    axes[0].legend()

    kpis = ["Lead Time (h)", "Avg Defect Rate (%)", "SOP Authoring (h)"]
    before_vals = [62.0, 6.8, 12.0]
    after_vals = [12.0, 0.56, 3.5]
    x_k = range(len(kpis))
    axes[1].bar(
        [x - 0.18 for x in x_k], before_vals, width=0.36, label="As-Is Baseline", color="#7F8C8D"
    )
    axes[1].bar(
        [x + 0.18 for x in x_k], after_vals, width=0.36, label="To-Be + AI SOPs", color="#1B365D"
    )
    axes[1].set_xticks(list(x_k))
    axes[1].set_xticklabels(kpis)
    axes[1].set_ylabel("Metric Value")
    axes[1].set_title("Operational Excellence & AI Enablement Impact", fontweight="bold")
    axes[1].legend()

    plt.tight_layout()
    p2 = assets_dir / "supply_chain_kpi_impact.png"
    fig.savefig(p2, dpi=180)
    plt.close(fig)

    return [p1, p2]


def build_excel_process_review() -> Path:
    as_is = parse_bpmn_process(ROOT_DIR / "processes" / "bpmn" / "order_to_delivery_as_is.bpmn")
    to_be = parse_bpmn_process(ROOT_DIR / "processes" / "bpmn" / "order_to_delivery_to_be.bpmn")

    excel_path = ROOT_DIR / "deliverables" / "excel" / "supply_chain_process_review.xlsx"
    excel_path.parent.mkdir(parents=True, exist_ok=True)

    wb = openpyxl.Workbook()
    ws_dash = wb.active
    ws_dash.title = "Executive_KPI_Dashboard"

    navy_fill = PatternFill("solid", fgColor="1B365D")
    sub_fill = PatternFill("solid", fgColor="EAF2F8")
    white_bold = Font(bold=True, color="FFFFFF", size=11)
    title_font = Font(bold=True, color="1B365D", size=14)

    ws_dash["A1"] = "Global Supply Chain Process Review & Optimization Model (As-Is vs. To-Be)"
    ws_dash["A1"].font = title_font

    headers = [
        "Stage #",
        "Functional Lane",
        "Process Stage",
        "As-Is Cycle (h)",
        "To-Be Cycle (h)",
        "Hours Saved",
        "As-Is Error (%)",
        "To-Be Error (%)",
    ]
    ws_dash.append([])
    ws_dash.append(headers)
    for col_idx in range(1, len(headers) + 1):
        cell = ws_dash.cell(row=3, column=col_idx)
        cell.fill = navy_fill
        cell.font = white_bold
        cell.alignment = Alignment(horizontal="center")

    stage_names = [
        "Demand Forecast Consolidation",
        "Co-Packing & Supplier PO Release",
        "Cross-Plant Inventory Reallocation",
        "Warehouse Pick, Pack & Traceability",
        "Export & Cold-Chain Documentation",
    ]

    for idx, (s_old, s_new, st_name) in enumerate(
        zip(as_is["steps"], to_be["steps"], stage_names), start=1
    ):
        r = idx + 3
        ws_dash.append(
            [
                idx,
                s_old["lane"],
                st_name,
                s_old["avg_cycle_hours"],
                s_new["avg_cycle_hours"],
                f"=D{r}-E{r}",
                s_old["error_rate_pct"],
                s_new["error_rate_pct"],
            ]
        )

    # Total Row with Excel Formulas
    ws_dash.append(
        [
            "TOTAL",
            "End-to-End Supply Chain",
            "Order-to-Delivery Lead Time",
            "=SUM(D4:D8)",
            "=SUM(E4:E8)",
            "=SUM(F4:F8)",
            "=AVERAGE(G4:G8)",
            "=AVERAGE(H4:H8)",
        ]
    )
    for col_idx in range(1, 9):
        c = ws_dash.cell(row=9, column=col_idx)
        c.fill = sub_fill
        c.font = Font(bold=True, color="1B365D")

    widths = [10, 26, 34, 16, 16, 15, 16, 16]
    for col_idx, w in enumerate(widths, start=1):
        ws_dash.column_dimensions[openpyxl.utils.get_column_letter(col_idx)].width = w

    # Native OpenPyXL Bar Chart
    chart = BarChart()
    chart.type = "col"
    chart.style = 10
    chart.title = "Cycle Time Comparison by Supply Chain Stage (Hours)"
    chart.y_axis.title = "Hours"
    chart.x_axis.title = "Process Stage"
    data_ref = Reference(ws_dash, min_col=4, max_col=5, min_row=3, max_row=8)
    cats_ref = Reference(ws_dash, min_col=3, min_row=4, max_row=8)
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats_ref)
    chart.width = 18
    chart.height = 10
    ws_dash.add_chart(chart, "B11")

    # Sheet 2: AI Enablement & Documentation ROI
    ws_ai = wb.create_sheet("AI_Documentation_ROI")
    ws_ai["A1"] = "AI-Assisted Process Documentation & Governance Efficiency"
    ws_ai["A1"].font = title_font
    ws_ai.append([])
    ws_ai.append(
        [
            "Documentation Deliverable",
            "Manual Effort (h)",
            "AI-Assisted Effort (h)",
            "Time Reduction (%)",
        ]
    )
    for col_idx in range(1, 5):
        c = ws_ai.cell(row=3, column=col_idx)
        c.fill = navy_fill
        c.font = white_bold

    ai_rows = [
        ("L3 BPMN SOP Drafting & Formatting", 6.0, 1.5, "=(B4-C4)/B4"),
        ("RACI Governance Matrix Alignment", 2.5, 0.8, "=(B5-C5)/B5"),
        ("Role-Based User Onboarding Guide", 3.5, 1.2, "=(B6-C6)/B6"),
    ]
    for row_vals in ai_rows:
        ws_ai.append(list(row_vals))
    for r in range(4, 7):
        ws_ai.cell(row=r, column=4).number_format = "0.0%"
    for col_idx, w in enumerate([36, 18, 22, 20], start=1):
        ws_ai.column_dimensions[openpyxl.utils.get_column_letter(col_idx)].width = w

    wb.save(excel_path)
    return excel_path


def build_powerpoint_pitch(visual_paths: list[Path]) -> Path:
    pptx_path = ROOT_DIR / "deliverables" / "powerpoint" / "process_optimization_pitch.pptx"
    pptx_path.parent.mkdir(parents=True, exist_ok=True)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    navy = RGBColor(27, 54, 93)
    accent = RGBColor(192, 57, 43)
    dark_text = RGBColor(44, 62, 80)

    def add_header(slide, title_text: str, subtitle_text: str):
        title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12.1), Inches(0.8))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = navy

        p2 = tf.add_paragraph()
        p2.text = subtitle_text
        p2.font.size = Pt(13)
        p2.font.color.rgb = accent

    # Slide 1: Executive Title Slide
    s1 = prs.slides.add_slide(prs.slide_layouts[6])
    box = s1.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(3.0))
    tf = box.text_frame
    p = tf.paragraphs[0]
    p.text = "Global Supply Chain Process Modelling & AI Enablement"
    p.font.size = Pt(34)
    p.font.bold = True
    p.font.color.rgb = navy

    p_sub = tf.add_paragraph()
    p_sub.text = (
        "BPMN 2.0 Architecture, Bottleneck Analysis & Automated SOP Governance\n"
        "Prepared by Omar Takassa | MSc Business Informatics (TU Wien)"
    )
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = dark_text

    # Slide 2: As-Is vs To-Be BPMN 2.0 Process Landscape
    s2 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(
        s2,
        "End-to-End BPMN 2.0 Process Landscape (As-Is vs. To-Be)",
        "Eliminating manual email/spreadsheet handoffs across Demand Planning, Co-Packing, and Logistics",
    )
    s2.shapes.add_picture(str(visual_paths[0]), Inches(0.55), Inches(1.45), width=Inches(12.2))

    # Slide 3: Quantitative KPI & Bottleneck Impact
    s3 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(
        s3,
        "Supply Chain Cycle Time & Quality Impact",
        "80.6% reduction in order-to-delivery processing time (62.0h to 12.0h) and 91% lower defect rate",
    )
    s3.shapes.add_picture(str(visual_paths[1]), Inches(0.75), Inches(1.55), width=Inches(11.8))

    # Slide 4: AI-Enabled Process Documentation & Rollout Roadmap
    s4 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(
        s4,
        "AI Process Documentation & 6-Month Implementation Roadmap",
        "Accelerating SOP creation, RACI alignment, and user adoption across global operations",
    )
    body = s4.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.6), Inches(5.2))
    btf = body.text_frame
    bullets = [
        "• Automated BPMN-to-SOP Pipeline: Parses XML process models into standardized SOPs, RACI tables, and onboarding guides (~71% faster documentation).",
        "• Phase 1 (Months 1–2): As-Is L1–L3 process discovery workshops, stakeholder interviews, and bottleneck baseline in Excel.",
        "• Phase 2 (Months 3–4): To-Be BPMN 2.0 modelling, ERP/WMS integration rules, and automated Data Quality controls.",
        "• Phase 3 (Months 5–6): Pilot rollout, role-based user training guides, and executive KPI governance tracking.",
    ]
    for idx, text in enumerate(bullets):
        para = btf.paragraphs[0] if idx == 0 else btf.add_paragraph()
        para.text = text
        para.font.size = Pt(17)
        para.font.color.rgb = dark_text
        para.space_after = Pt(16)

    prs.save(pptx_path)
    return pptx_path


if __name__ == "__main__":
    sops = build_all_sops()
    imgs = render_process_visuals()
    xlsx = build_excel_process_review()
    pptx = build_powerpoint_pitch(imgs)
    print(f"Built SOPs={len(sops)}, Excel={xlsx.name}, PPTX={pptx.name}")
