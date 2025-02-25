import logging
import platform
import re
import subprocess
from enum import Enum, auto


class Platform(Enum):
    WINDOWS = auto()
    MACOS = auto()
    LINUX = auto()
    UNKNOWN = auto()


def _get_current_platform() -> Platform:
    """Determine the current operating system platform."""
    system = platform.system()
    match system:
        case "Windows":
            return Platform.WINDOWS
        case "Darwin":
            return Platform.MACOS
        case "Linux":
            return Platform.LINUX
        case _:
            return Platform.UNKNOWN


def _sanitize_process_name(process_name: str) -> str:
    # Only allow alphanumeric characters, dots, and hyphens
    sanitized = re.sub(r"[^a-zA-Z0-9.\-_]", "", process_name)

    # Check if empty string
    if not sanitized:
        raise ValueError(
            f"Invalid process name: '{process_name}' contains no valid characters"
        )

    # If sanitization changed the string, it contained invalid characters
    if sanitized != process_name:
        raise ValueError(f"Process name contains invalid characters: '{process_name}'")

    return sanitized


def _kill_processes(process_name: str) -> None:
    safe_process_name = _sanitize_process_name(process_name)
    current_platform = _get_current_platform()
    cmd_args = []

    try:
        match current_platform:
            case Platform.WINDOWS:
                cmd_args = ["taskkill", "/f", "/im", safe_process_name]
            case Platform.MACOS:
                cmd_args = ["killall", safe_process_name]
            case Platform.LINUX:
                cmd_args = ["pkill", safe_process_name]
            case Platform.UNKNOWN:
                raise RuntimeError(f"Unsupported operating system: {platform.system()}")

        logging.info(f"Killing {safe_process_name} process")
        subprocess.run(
            cmd_args,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except ValueError as e:
        logging.error(f"Input validation error: {e}")
    except subprocess.SubprocessError as e:
        logging.warning(f"Error killing process {process_name}: {e}")


def kill_zoom_processes() -> None:
    current_platform = _get_current_platform()

    if current_platform != Platform.UNKNOWN:
        process_name = {
            Platform.WINDOWS: "Zoom.exe",
            Platform.MACOS: "zoom.us",
            Platform.LINUX: "zoom",
        }.get(current_platform)

        if process_name:
            _kill_processes(process_name)
        else:
            logging.error(f"Attempted to kill unauthorized process: {process_name}")
