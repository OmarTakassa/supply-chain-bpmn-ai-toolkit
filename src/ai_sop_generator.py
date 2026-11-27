import xml.etree.ElementTree as ET
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
BPMN_NS = {"bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL"}


def parse_bpmn_process(bpmn_path: Path) -> dict:
    tree = ET.parse(bpmn_path)
    root = tree.getroot()
    proc = root.find("bpmn:process", BPMN_NS)
    proc_name = proc.attrib.get("name", bpmn_path.stem)

    node_to_lane = {}
    for lane in proc.findall(".//bpmn:lane", BPMN_NS):
        lane_name = lane.attrib.get("name", "General Operations")
        for ref in lane.findall("bpmn:flowNodeRef", BPMN_NS):
            if ref.text:
                node_to_lane[ref.text.strip()] = lane_name

    tasks = []
    for tag in ("userTask", "serviceTask"):
        for node in proc.findall(f"bpmn:{tag}", BPMN_NS):
            node_id = node.attrib["id"]
            impl = node.attrib.get(
                "implementation", "Standard | Avg Cycle: 2.0h | Error Rate: 1.0%"
            )
            parts = [p.strip() for p in impl.split("|")]
            system_tool = parts[0] if len(parts) > 0 else "ERP"
            cycle_hours = float(parts[1].replace("Avg Cycle:", "").replace("h", "").strip())
            error_pct = float(parts[2].replace("Error Rate:", "").replace("%", "").strip())

            tasks.append(
                {
                    "step_id": node_id,
                    "task_type": "Automated System Task" if tag == "serviceTask" else "Human Task",
                    "lane": node_to_lane.get(node_id, "Operations"),
                    "step_name": node.attrib.get("name", node_id),
                    "system_tool": system_tool,
                    "avg_cycle_hours": cycle_hours,
                    "error_rate_pct": error_pct,
                }
            )

    # Preserve logical process order by step definition sequence
    all_nodes = []
    for elem in proc:
        local_tag = elem.tag.split("}")[-1]
        if local_tag in {"userTask", "serviceTask"}:
            match = next(t for t in tasks if t["step_id"] == elem.attrib["id"])
            all_nodes.append(match)

    return {
        "process_id": proc.attrib.get("id", bpmn_path.stem),
        "process_name": proc_name,
        "steps": all_nodes,
        "total_cycle_hours": round(sum(s["avg_cycle_hours"] for s in all_nodes), 2),
        "avg_error_rate_pct": round(
            sum(s["error_rate_pct"] for s in all_nodes) / max(1, len(all_nodes)), 2
        ),
    }


def generate_sop_markdown(bpmn_path: Path, output_md: Path) -> Path:
    parsed = parse_bpmn_process(bpmn_path)
    lines = [
        f"# Standard Operating Procedure (SOP): {parsed['process_name']}",
        "",
        f"- **Process ID:** `{parsed['process_id']}`",
        "- **Process Landscape Level:** L3 — Supply Chain Execution (Order-to-Delivery)",
        "- **Owner:** Global Process Documentation & Operations Excellence Team",
        f"- **Target End-to-End Cycle Time:** {parsed['total_cycle_hours']} hours",
        f"- **Mean Step Defect Rate:** {parsed['avg_error_rate_pct']}%",
        "",
        "## 1. Process Step Execution & System Controls",
        "",
        "| Seq | Functional Lane | Activity | Execution Mode | Tool / System | Cycle (h) | Defect Rate |",
        "| :--- | :--- | :--- | :--- | :--- | :---: | :---: |",
    ]

    for idx, step in enumerate(parsed["steps"], start=1):
        lines.append(
            f"| {idx} | {step['lane']} | {step['step_name']} | {step['task_type']} | "
            f"{step['system_tool']} | {step['avg_cycle_hours']:.1f}h | {step['error_rate_pct']:.1f}% |"
        )

    lines.extend(
        [
            "",
            "## 2. Governance & RACI Responsibility Matrix",
            "",
            "| Activity | Demand Planner | Procurement Lead | Warehouse Ops | Process Doc Team |",
            "| :--- | :---: | :---: | :---: | :---: |",
        ]
    )

    for step in parsed["steps"]:
        lane = step["lane"]
        r_dp = "**R**" if "Demand" in lane else "I"
        r_pr = "**R**" if "Procurement" in lane else "C"
        r_wh = "**R**" if "Warehouse" in lane else "I"
        lines.append(f"| {step['step_name']} | {r_dp} | {r_pr} | {r_wh} | **A / C** |")

    lines.extend(
        [
            "",
            "## 3. User Adoption & Quick-Reference Onboarding Checklist",
            "1. Verify role-based access in ERP/WMS before executing step handoffs.",
            "2. Review automated Data Quality and Available-to-Promise (ATP) exception alerts.",
            "3. Log any manual override or master-data discrepancy in the Process Governance portal.",
        ]
    )

    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_md


def build_all_sops() -> list[Path]:
    bpmn_dir = ROOT_DIR / "processes" / "bpmn"
    sop_dir = ROOT_DIR / "processes" / "sops"
    outputs = []
    for bpmn_file, sop_name in [
        ("order_to_delivery_as_is.bpmn", "SOP_01_Order_to_Delivery_As_Is.md"),
        ("order_to_delivery_to_be.bpmn", "SOP_02_Order_to_Delivery_To_Be.md"),
    ]:
        outputs.append(generate_sop_markdown(bpmn_dir / bpmn_file, sop_dir / sop_name))
    return outputs


if __name__ == "__main__":
    generated = build_all_sops()
    print(f"Generated {len(generated)} standardized SOPs: {[p.name for p in generated]}")
