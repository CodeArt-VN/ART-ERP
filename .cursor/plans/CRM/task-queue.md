# Task queue

Plan: [plan.md](plan.md) · **WAITING_SPONSOR_CONFIRM_G2**

```json
{
  "program": "CRM-Wedding",
  "branch": "AI/crm-wedding-g1-a303",
  "status": "WAITING_SPONSOR_CONFIRM_G2",
  "tasks": [
    { "id": "g1-biz-flow", "status": "done", "sponsorGate": "G1" },
    {
      "id": "g2-forms",
      "status": "waiting_confirm",
      "sponsorGate": "G2",
      "artifacts": [
        ".cursor/plans/CRM/docs/03-danh-sach-forms.md",
        ".cursor/plans/CRM/docs/04-chuc-nang-trong-form.md",
        ".cursor/plans/CRM/docs/05-test-cases.md"
      ]
    },
    { "id": "g3-prototype", "status": "blocked", "dependsOn": ["g2-forms"] },
    { "id": "g4-build-test", "status": "blocked", "dependsOn": ["g3-prototype"] },
    { "id": "g5-uat-guide", "status": "blocked", "dependsOn": ["g4-build-test"] },
    { "id": "g6-golive", "status": "blocked", "dependsOn": ["g5-uat-guide"] }
  ]
}
```
