from __future__ import annotations
import logging
from typing import Optional, Dict, List

from app.services.engine_base import TTSBackend
from app.services.backends.edge_tts_backend import EdgeTTSBackend
from app.services.backends.moss_tts_backend import MOSSTTSBackend

logger = logging.getLogger(__name__)

_backends: Dict[str, TTSBackend] = {}
_default_backend: str = "edge-tts"


def register_backend(backend: TTSBackend, make_default: bool = False) -> None:
    _backends[backend.name] = backend
    if make_default or len(_backends) == 1:
        global _default_backend
        _default_backend = backend.name
    logger.info("Registered TTS backend: %s (%s)", backend.name, backend.display_name)


def get_backend(name: Optional[str] = None) -> TTSBackend:
    if name is None:
        name = _default_backend
    backend = _backends.get(name)
    if backend is None:
        logger.warning("Backend '%s' not found, falling back to '%s'", name, _default_backend)
        return _backends[_default_backend]
    return backend


def list_available_backends() -> List[dict]:
    results = []
    for name, backend in _backends.items():
        results.append({
            "name": backend.name,
            "display_name": backend.display_name,
            "requires_gpu": backend.requires_gpu,
            "requires_env_setup": backend.requires_env_setup,
        })
    return results


def initialize_backends() -> None:
    register_backend(EdgeTTSBackend(), make_default=True)

    try:
        moss = MOSSTTSBackend()
        register_backend(moss)
    except Exception as e:
        logger.warning("Failed to register MOSS-TTS-Nano backend: %s", e)
