# Standard Operating Procedure (SOP): Global Supply Chain Order-to-Delivery (To-Be Automated)

- **Process ID:** `Proc_OrderToDelivery_ToBe`
- **Process Landscape Level:** L3 — Supply Chain Execution (Order-to-Delivery)
- **Owner:** Global Process Documentation & Operations Excellence Team
- **Target End-to-End Cycle Time:** 12.0 hours
- **Mean Step Defect Rate:** 0.56%

## 1. Process Step Execution & System Controls

| Seq | Functional Lane | Activity | Execution Mode | Tool / System | Cycle (h) | Defect Rate |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| 1 | Demand Planning | Automated Multi-Region Forecast Aggregation & DQ Check | Automated System Task | ERP API + DQ Rules | 1.5h | 0.4% |
| 2 | Procurement & Co-Packing | EDI / Portal Co-Packing Schedule Release | Automated System Task | EDI Integration | 3.0h | 0.6% |
| 3 | Procurement & Co-Packing | AI-Assisted Cross-Plant Rebalancing Recommendation | Automated System Task | AI Triage + Planner Approve | 2.5h | 1.1% |
| 4 | Warehouse & Distribution | RF Scanner Guided WMS Pick & Batch Traceability | Human Task | WMS Mobile App | 4.0h | 0.5% |
| 5 | Warehouse & Distribution | Auto-Generate Digital Customs & Cold-Chain Pack | Automated System Task | ERP Document Engine | 1.0h | 0.2% |

## 2. Governance & RACI Responsibility Matrix

| Activity | Demand Planner | Procurement Lead | Warehouse Ops | Process Doc Team |
| :--- | :---: | :---: | :---: | :---: |
| Automated Multi-Region Forecast Aggregation & DQ Check | **R** | C | I | **A / C** |
| EDI / Portal Co-Packing Schedule Release | I | **R** | I | **A / C** |
| AI-Assisted Cross-Plant Rebalancing Recommendation | I | **R** | I | **A / C** |
| RF Scanner Guided WMS Pick & Batch Traceability | I | C | **R** | **A / C** |
| Auto-Generate Digital Customs & Cold-Chain Pack | I | C | **R** | **A / C** |

## 3. User Adoption & Quick-Reference Onboarding Checklist
1. Verify role-based access in ERP/WMS before executing step handoffs.
2. Review automated Data Quality and Available-to-Promise (ATP) exception alerts.
3. Log any manual override or master-data discrepancy in the Process Governance portal.
