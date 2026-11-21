---
name: i18n-keys
description: Adds or reuses ngx-translate keys in ART-ERP-FE en-US.json and vi-VN.json. Use when adding UI strings, labels, showMessage text, datatable column names, page titles, or the translate pipe.
---

# ART-ERP-FE i18n

Source of truth:

- `ART-ERP-FE/src/assets/i18n/en-US.json`
- `ART-ERP-FE/src/assets/i18n/vi-VN.json`

The key is the English sentence. In `en-US.json` the value equals the key. In `vi-VN.json` the value is the Vietnamese translation. `@ngx-translate` pipe name is `translate`.

Logs under `.cursor/i18m/` are old audits. Do not treat them as the catalog.

## Use an existing key

Search both JSON files before adding a string. Reuse the same English key (`Saving completed!`, `Name`, `Other information`). Do not invent a second key for the same sentence, and do not introduce a code-style key (`PAGE_TITLE`) when the app already uses English sentences.

## Reuse the existing meaning

A status, type or outcome word (`Lost`, `Won`, `Open`, `Done`) is already translated somewhere in `vi-VN.json` or in the CRM screens. Search for the word and reuse that Vietnamese. Do not translate it with a different meaning (`Lost` is a lost deal, not "lý do thua"). When the existing translation fits, change nothing.

## Add a key

1. Confirm the sentence is not already a key.
2. Add it to **both** files. Keep JSON valid.
3. `en-US.json`: `"English sentence": "English sentence"`.
4. `vi-VN.json`: `"English sentence": "câu tiếng Việt"`.
5. Wire the UI with the English key only.

```html
{{ 'Other information' | translate }}
```

```ts
this.env.showMessage('Saving completed!', 'success');
```

Datatable `name` and `app-form-control` `label` are translate keys. Write the English sentence there, not the Vietnamese text.

## Do not

- Do not put Vietnamese in the template or in the JSON key.
- Do not edit only one locale file.
- Do not add a new i18n library or a per-page dictionary.
