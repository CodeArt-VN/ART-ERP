"""CLI entry: console mode on any OS; Windows Service commands on Win32."""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    # Windows service verbs must be handled before argparse.
    if sys.platform == "win32" and argv and argv[0].lower() in {
        "install",
        "update",
        "remove",
        "start",
        "stop",
        "restart",
        "debug",
    }:
        from edge_face.service import handle_windows_service_command

        # Temporarily restore argv for pywin32
        old = sys.argv
        sys.argv = [old[0], *argv]
        try:
            handle_windows_service_command()
        finally:
            sys.argv = old
        return 0

    parser = argparse.ArgumentParser(prog="art-edge-face", description="ART Edge Face AI")
    parser.add_argument(
        "-c",
        "--config",
        default=None,
        help="Path to config.json (or set EDGE_FACE_CONFIG)",
    )
    parser.add_argument(
        "--dry-check-config",
        action="store_true",
        help="Load config and exit (no models / cameras)",
    )
    args = parser.parse_args(argv)

    if args.dry_check_config:
        from edge_face.config import load_config
        from edge_face.service import _default_config_path

        path = args.config or _default_config_path()
        cfg = load_config(path)
        print(
            f"OK branch={cfg.branch_id} cameras={len(cfg.enabled_cameras)} "
            f"threshold={cfg.confidence_threshold} hq={cfg.hq.events_url}"
        )
        return 0

    from edge_face.service import run_console

    return run_console(args.config)


if __name__ == "__main__":
    raise SystemExit(main())
