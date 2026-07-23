# Task queue — khớp cổng confirm với anh

Plan: [plan.md](plan.md)  
Trạng thái: **WAITING_G1**

```json
{
  "program": "CRM-Wedding",
  "branch": "feature/crm-wedding",
  "canonicalPlan": ".cursor/plans/CRM/plan.md",
  "status": "WAITING_G1",
  "rule": "Không sang gate sau khi chưa có Confirm sponsor trong gates/G#.md",
  "tasks": [
    {
      "id": "g1-biz-flow",
      "dependsOn": [],
      "agent": "BA+PM",
      "sponsorGate": "G1",
      "status": "pending",
      "dod": ["Artifact nghiệp vụ+flow gửi anh", "Xin họp/confirm", "gates/G1.md Confirm"]
    },
    {
      "id": "g2-forms",
      "dependsOn": ["g1-biz-flow"],
      "agent": "BA",
      "sponsorGate": "G2",
      "status": "pending",
      "dod": ["docs draft 03+04+05", "Xin confirm", "gates/G2.md Confirm"]
    },
    {
      "id": "g3-prototype",
      "dependsOn": ["g2-forms"],
      "agent": "DEV",
      "sponsorGate": "G3",
      "status": "pending",
      "dod": ["Prototype FE demo", "Anh chốt UI", "gates/G3.md Confirm"]
    },
    {
      "id": "g4-build-test",
      "dependsOn": ["g3-prototype"],
      "agent": "DEV+TEST",
      "sponsorGate": "G4",
      "status": "pending",
      "dod": ["BE+FE theo prototype", "Unit/API test TC pass", "gates/G4.md test summary"]
    },
    {
      "id": "g5-uat-guide",
      "dependsOn": ["g4-build-test"],
      "agent": "PM+BA+TEST",
      "sponsorGate": "G5",
      "status": "pending",
      "dod": ["UAT demo", "Anh UAT OK", "Hướng dẫn sử dụng + 5 docs", "gates/G5.md"]
    },
    {
      "id": "g6-golive",
      "dependsOn": ["g5-uat-guide"],
      "agent": "ORCH",
      "sponsorGate": "G6",
      "status": "pending",
      "dod": ["Lệnh anh bật flag", "gates/G6.md"]
    }
  ]
}
```
