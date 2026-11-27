# Standard Operating Procedure (SOP): Global Supply Chain Order-to-Delivery (As-Is)

- **Process ID:** `Proc_OrderToDelivery_AsIs`
- **Process Landscape Level:** L3 — Supply Chain Execution (Order-to-Delivery)
- **Owner:** Global Process Documentation & Operations Excellence Team
- **Target End-to-End Cycle Time:** 62.0 hours
- **Mean Step Defect Rate:** 6.8%

## 1. Process Step Execution & System Controls

| Seq | Functional Lane | Activity | Execution Mode | Tool / System | Cycle (h) | Defect Rate |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| 1 | Demand Planning | Consolidate Regional Excel Forecasts (Manual Email) | Human Task | Manual Spreadsheet | 14.0h | 8.5% |
| 2 | Procurement & Co-Packing | Issue Co-Packing & Packaging POs via Email | Human Task | Email + Legacy ERP | 18.0h | 6.2% |
| 3 | Procurement & Co-Packing | Escalate & Reallocate Cross-Plant Inventory | Human Task | Phone/Email Escalation | 12.0h | 9.0% |
| 4 | Warehouse & Distribution | Manual Warehouse Pick, Pack & Batch Scan | Human Task | Paper Pick List | 9.5h | 4.8% |
| 5 | Warehouse & Distribution | Prepare Export & Cold-Chain Manifests Manually | Human Task | Manual PDF/Excel | 8.5h | 5.5% |

## 2. Governance & RACI Responsibility Matrix

| Activity | Demand Planner | Procurement Lead | Warehouse Ops | Process Doc Team |
| :--- | :---: | :---: | :---: | :---: |
| Consolidate Regional Excel Forecasts (Manual Email) | **R** | C | I | **A / C** |
| Issue Co-Packing & Packaging POs via Email | I | **R** | I | **A / C** |
| Escalate & Reallocate Cross-Plant Inventory | I | **R** | I | **A / C** |
| Manual Warehouse Pick, Pack & Batch Scan | I | C | **R** | **A / C** |
| Prepare Export & Cold-Chain Manifests Manually | I | C | **R** | **A / C** |

## 3. User Adoption & Quick-Reference Onboarding Checklist
1. Verify role-based access in ERP/WMS before executing step handoffs.
2. Review automated Data Quality and Available-to-Promise (ATP) exception alerts.
3. Log any manual override or master-data discrepancy in the Process Governance portal.
