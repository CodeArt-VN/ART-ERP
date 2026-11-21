#!/usr/bin/env python3
"""Deny agent edits to GenCode outputs. Rules only advise; this hook blocks the tool."""
import json
import re
import sys

PROTECTED_SUFFIXES = (
    "src/app/services/static/services.service.ts",
    "src/app/services/static/api-list.ts",
    "src/app/models/model-list-interface.ts",
    "API/Controllers/APIControllers.cs",
    "ClassLibrary/Model.Context.cs",
)
TBL_RE = re.compile(r"(^|/)ClassLibrary/tbl_[^/]+\.cs$")
PATH_KEYS = {
    "path",
    "file_path",
    "file",
    "uri",
    "target_file",
    "target_notebook",
    "notebook_path",
}
READ_TOOLS = {
    "Read",
    "Grep",
    "Glob",
    "SemanticSearch",
    "ReadLints",
    "WebSearch",
    "WebFetch",
    "GetDynamicTools",
    "CallDynamicTool",
    "TodoWrite",
    "AskQuestion",
    "SwitchMode",
    "AwaitShell",
    "GenerateImage",
    "FetchMcpResource",
    "ListMcpResources",
    "Task",
    "XSearch",
}


def allow():
    sys.stdout.write(json.dumps({"permission": "allow"}))
    sys.exit(0)


def deny(path):
    shown = path or "a GenCode output"
    sys.stdout.write(
        json.dumps(
            {
                "permission": "deny",
                "user_message": "Đã chặn sửa file GenCode: %s" % shown,
                "agent_message": (
                    "DENIED by project hook .cursor/hooks/block-gencode-edit.py. "
                    "Do not retry and do not use the shell to write this file. "
                    "%s is GenCode output and will be overwritten. "
                    "Extra FE endpoints go on the existing APIList key in "
                    "ART-ERP-FE/src/app/services/static/global-variable.ts, "
                    "or in a new file under services/ or pages/. "
                    "BE CRUD changes go in CustomBusiness partial hooks or CustomAPI, "
                    "not tbl_*.cs, Model.Context.cs, or APIControllers.cs."
                )
                % shown,
            }
        )
    )
    sys.exit(0)


def is_protected(text):
    if not text:
        return False
    normalized = text.replace("\\", "/")
    for suffix in PROTECTED_SUFFIXES:
        if normalized.endswith(suffix) or ("/" + suffix) in normalized:
            return True
    if "/CustomBusiness/" in normalized:
        return False
    return TBL_RE.search(normalized) is not None


def iter_paths(value, key=None):
    if isinstance(value, dict):
        for child_key, child in value.items():
            for found in iter_paths(child, child_key):
                yield found
    elif isinstance(value, list):
        for child in value:
            for found in iter_paths(child, key):
                yield found
    elif isinstance(value, str) and key in PATH_KEYS:
        yield value


def shell_writes(command):
    if re.search(r">|[|] *tee\b", command):
        return True
    if re.search(r"\b(sed|perl)\b", command) and re.search(r"(^|\s)-i(nplace|\s|\b)", command):
        return True
    if re.search(r"\b(python3?|node|ruby|php|perl)\b", command):
        return True
    if re.search(r"\b(cp|mv|rm|truncate|dd|install|sponge)\b", command):
        return True
    if re.search(r"\bgit\s+(apply|checkout|restore|switch|reset|am)\b", command):
        return True
    return False


def main():
    raw = sys.stdin.read()
    data = json.loads(raw) if raw.strip() else {}
    tool = data.get("tool_name") or ""
    event = data.get("hook_event_name") or ""
    tool_input = data.get("tool_input") or {}
    if isinstance(tool_input, str):
        try:
            tool_input = json.loads(tool_input)
        except json.JSONDecodeError:
            tool_input = {"command": tool_input}

    command = data.get("command") or ""
    if isinstance(tool_input, dict):
        command = command or tool_input.get("command") or ""

    if event == "beforeShellExecution" or tool == "Shell":
        if is_protected(command) and shell_writes(command):
            deny(command.strip()[:180])
        allow()

    if tool in READ_TOOLS:
        allow()

    for path in iter_paths(tool_input):
        if is_protected(path):
            deny(path)
    allow()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        allow()
