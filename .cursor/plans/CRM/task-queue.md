# Task queue · WAITING_SPONSOR_CONFIRM_G3

```json
{
  "program": "CRM-Wedding",
  "branch": "AI/crm-wedding-g1-a303",
  "status": "WAITING_SPONSOR_CONFIRM_G3",
  "tasks": [
    { "id": "g1-biz-flow", "status": "done" },
    { "id": "g2-forms", "status": "done" },
    {
      "id": "g3-prototype",
      "status": "waiting_confirm",
      "artifact": ".cursor/plans/CRM/prototype/index.html"
    },
    { "id": "g4-build-test", "status": "blocked", "dependsOn": ["g3-prototype"] },
    { "id": "g5-uat-guide", "status": "blocked" },
    { "id": "g6-golive", "status": "blocked" }
  ]
}
```
