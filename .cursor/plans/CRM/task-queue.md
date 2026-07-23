# Task queue — khớp cổng confirm với anh

Plan: [plan.md](plan.md)  
Trạng thái: **WAITING_SPONSOR_CONFIRM_G1**

```json
{
  "program": "CRM-Wedding",
  "branch": "AI/crm-wedding-g1-a303",
  "canonicalPlan": ".cursor/plans/CRM/plan.md",
  "status": "WAITING_SPONSOR_CONFIRM_G1",
  "rule": "Không sang gate sau khi chưa có Confirm sponsor trong gates/G#.md",
  "tasks": [
    {
      "id": "g1-biz-flow",
      "dependsOn": [],
      "agent": "BA+PM",
      "sponsorGate": "G1",
      "status": "waiting_confirm",
      "artifact": ".cursor/plans/CRM/docs/g1-nghiep-vu-flow.md",
      "dod": ["Artifact G1 gửi anh", "Xin Confirm G1", "gates/G1.md Confirm"]
    },
    {
      "id": "g2-forms",
      "dependsOn": ["g1-biz-flow"],
      "agent": "BA",
      "sponsorGate": "G2",
      "status": "blocked",
      "dod": ["docs draft 03+04+05", "Xin confirm", "gates/G2.md Confirm"]
    },
    {
      "id": "g3-prototype",
      "dependsOn": ["g2-forms"],
      "agent": "DEV",
      "sponsorGate": "G3",
      "status": "blocked",
      "dod": ["Prototype FE demo", "Anh chốt UI", "gates/G3.md Confirm"]
    },
    {
      "id": "g4-build-test",
      "dependsOn": ["g3-prototype"],
      "agent": "DEV+TEST",
      "sponsorGate": "G4",
      "status": "blocked",
      "dod": ["BE+FE theo prototype", "Unit/API test TC pass", "gates/G4.md test summary"]
    },
    {
      "id": "g5-uat-guide",
      "dependsOn": ["g4-build-test"],
      "agent": "PM+BA+TEST",
      "sponsorGate": "G5",
      "status": "blocked",
      "dod": ["UAT demo", "Anh UAT OK", "Hướng dẫn sử dụng + 5 docs", "gates/G5.md"]
    },
    {
      "id": "g6-golive",
      "dependsOn": ["g5-uat-guide"],
      "agent": "ORCH",
      "sponsorGate": "G6",
      "status": "blocked",
      "dod": ["Lệnh anh bật flag", "gates/G6.md"]
    }
  ]
}
```
