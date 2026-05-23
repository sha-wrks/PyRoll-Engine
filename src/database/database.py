"""Employee data storage — Redis primary, in-memory fallback."""

import json
import logging
import os

logger = logging.getLogger(__name__)

try:
    import redis as _redis
    _REDIS_PKG = True
except ImportError:
    _REDIS_PKG = False

_HOST = os.getenv("REDIS_HOST", "localhost")
_PORT = int(os.getenv("REDIS_PORT", "6379"))
_DB   = int(os.getenv("REDIS_DB",   "0"))
_KEY  = "pyroll:employees"

_DEMO_EMPLOYEES = [
    {"name": "John Doe",   "hours": 40, "rate": 20.0, "deductions": 100.0, "tax_rate": 10.0, "bonus": 50.0},
    {"name": "Jane Smith", "hours": 35, "rate": 25.0, "deductions": 150.0, "tax_rate": 15.0, "bonus": 75.0},
]


class Database:
    """Thin wrapper around Redis with transparent in-memory fallback."""

    def __init__(self) -> None:
        self.using_redis = False
        self._client = None
        self._memory: list[dict] = []
        self._connect()
        self._seed()

    def _connect(self) -> None:
        if not _REDIS_PKG:
            logger.info("redis package not installed — using in-memory storage")
            return
        try:
            client = _redis.StrictRedis(
                host=_HOST, port=_PORT, db=_DB,
                decode_responses=True, socket_connect_timeout=2,
            )
            client.ping()
            self._client = client
            self.using_redis = True
            logger.info("Connected to Redis at %s:%d db=%d", _HOST, _PORT, _DB)
        except Exception as exc:
            logger.warning("Redis unavailable (%s) — falling back to in-memory", exc)

    def _seed(self) -> None:
        """Populate demo records only when storage is empty."""
        if self.using_redis:
            if self._client.llen(_KEY) == 0:
                for emp in _DEMO_EMPLOYEES:
                    self._client.rpush(_KEY, json.dumps(emp))
        elif not self._memory:
            self._memory.extend(_DEMO_EMPLOYEES)

    def save_employee(self, employee: dict) -> None:
        if self.using_redis:
            self._client.rpush(_KEY, json.dumps(employee))
        else:
            self._memory.append(employee)

    def get_all_employees(self) -> list[dict]:
        if self.using_redis:
            return [json.loads(r) for r in self._client.lrange(_KEY, 0, -1)]
        return list(self._memory)
