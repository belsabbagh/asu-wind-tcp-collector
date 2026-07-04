import argparse
import asyncio
import logging
import signal
from typing import Final

from database import init_db, insert_data

DEFAULT_PORT: Final = 21345
HOST: Final = "0.0.0.0"
MAX_DATA_SIZE: Final = 65536

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


class RawDataProtocol(asyncio.Protocol):
    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        addr = transport.get_extra_info("peername")
        logger.info("Connection from %s", addr)
        self._transport = transport
        self._buffer = b""

    def data_received(self, data: bytes) -> None:
        self._buffer += data
        if len(self._buffer) > MAX_DATA_SIZE:
            logger.warning("Overflow from %s, discarding", self._transport.get_extra_info("peername"))
            self._buffer = b""
            return

        insert_data(data)
        text = data.decode(errors="replace")
        preview = text[:80]
        logger.info(
            "Logged %d bytes from %s: %s%s",
            len(data),
            self._transport.get_extra_info("peername"),
            preview,
            "..." if len(text) > 80 else "",
        )

    def connection_lost(self, exc: Exception | None) -> None:
        addr = self._transport.get_extra_info("peername")
        logger.info("Disconnected from %s", addr)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Raw data TCP collector")
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"TCP port to listen on (default: {DEFAULT_PORT})",
    )
    return parser.parse_args()


async def main_async() -> None:
    args = parse_args()

    init_db()
    logger.info("Database initialized at data.db")

    loop = asyncio.get_running_loop()
    server = await loop.create_server(
        RawDataProtocol, HOST, args.port, reuse_address=True
    )

    async with server:
        logger.info("TCP server listening on %s:%s", HOST, args.port)
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, server.close)
        await server.serve_forever()


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
