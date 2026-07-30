"""Windows Service host (pywin32) — headless, no GUI."""

from __future__ import annotations

import logging
import os
import sys
import threading
from pathlib import Path

log = logging.getLogger("edge_face.service")


def _default_config_path() -> Path:
    env = os.environ.get("EDGE_FACE_CONFIG")
    if env:
        return Path(env)
    if getattr(sys, "frozen", False):
        here = Path(sys.executable).resolve().parent
    else:
        here = Path(__file__).resolve().parents[1]
    candidate = here / "config.json"
    if candidate.exists():
        return candidate
    return Path.cwd() / "config.json"


def run_console(config_path: str | Path | None = None) -> int:
    from edge_face.config import load_config
    from edge_face.logging_setup import setup_logging
    from edge_face.pipeline.runner import EdgePipeline

    path = Path(config_path) if config_path else _default_config_path()
    cfg = load_config(path)
    setup_logging(cfg.service.log_level, str(Path(cfg.service.log_dir)))
    pipeline = EdgePipeline(cfg)
    try:
        pipeline.run()
    except FileNotFoundError as exc:
        log.error("%s", exc)
        return 2
    return 0


def _build_service_class():
    import servicemanager
    import win32event
    import win32service
    import win32serviceutil

    from edge_face.config import load_config
    from edge_face.logging_setup import setup_logging
    from edge_face.pipeline.runner import EdgePipeline

    class ARTEdgeFaceService(win32serviceutil.ServiceFramework):
        _svc_name_ = "ARTEdgeFace"
        _svc_display_name_ = "ART Edge Face AI"
        _svc_description_ = (
            "Headless edge face recognition for restaurant POS (OpenVINO/iGPU)."
        )

        def __init__(self, args):
            win32serviceutil.ServiceFramework.__init__(self, args)
            self.stop_event = win32event.CreateEvent(None, 0, 0, None)
            self._thread: threading.Thread | None = None
            self._pipeline: EdgePipeline | None = None

        def SvcStop(self):
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            if self._pipeline is not None:
                self._pipeline.stop()
            win32event.SetEvent(self.stop_event)

        def SvcDoRun(self):
            servicemanager.LogInfoMsg("ART Edge Face starting")
            cfg = load_config(_default_config_path())
            setup_logging(cfg.service.log_level, str(Path(cfg.service.log_dir)))
            self._pipeline = EdgePipeline(cfg)

            def _target():
                try:
                    assert self._pipeline is not None
                    self._pipeline.run()
                except Exception as exc:
                    servicemanager.LogErrorMsg(f"ART Edge Face crashed: {exc}")

            self._thread = threading.Thread(
                target=_target, name="edge-face-pipeline", daemon=True
            )
            self._thread.start()
            win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
            if self._thread:
                self._thread.join(timeout=15)
            servicemanager.LogInfoMsg("ART Edge Face stopped")

    return ARTEdgeFaceService


def handle_windows_service_command() -> bool:
    """Return True if argv was consumed as a Windows service command."""
    if sys.platform != "win32":
        return False
    if len(sys.argv) > 1 and sys.argv[1].lower() in {
        "install",
        "update",
        "remove",
        "start",
        "stop",
        "restart",
        "debug",
    }:
        import win32serviceutil

        win32serviceutil.HandleCommandLine(_build_service_class())
        return True
    return False
