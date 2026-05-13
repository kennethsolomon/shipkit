"""Claude setup tools library."""

from .detect import ProjectConfig, detect_project
from .sidecar import (
    has_marker,
    is_custom_file,
    get_target_file,
    add_marker,
    format_output,
    count_lines,
    extract_sections,
)

__all__ = [
    "ProjectConfig",
    "detect_project",
    "has_marker",
    "is_custom_file",
    "get_target_file",
    "add_marker",
    "format_output",
    "count_lines",
    "extract_sections",
]
