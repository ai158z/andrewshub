import re
from dataclasses import dataclass
from typing import List, Optional
import logging


@dataclass
class FileChange:
    path: str
    added_lines: List[str]
    removed_lines: List[str]
    line_num: Optional[int] = None
    original_content: str = ""
    new_content: str = ""

    def __post_init__(self):
        if self.added_lines is None:
            self.added_lines = []
        if self.removed_lines is None:
            self.removed_lines = []


def parse_patch(patch_content: str) -> List[FileChange]:
    if not isinstance(patch_content, str):
        raise TypeError("patch_content must be a string")
    
    file_changes = []
    current_file = None
    line_num = None
    
    lines = patch_content.splitlines(keepends=True)
    
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('--- '):
            if current_file:
                file_changes.append(current_file)
            
            file_path = line[4:].strip()
            if file_path.startswith('a/') or file_path.startswith('b/'):
                file_path = file_path[2:]
            current_file = FileChange(path=file_path, added_lines=[], removed_lines=[])
            current_file.line_num = None
        elif line.startswith('+++ '):
            pass
        elif line.startswith('@@ '):
            hunk_match = re.match(r'@@ -(\d+),\d+ \+(\d+),\d+ @@', line)
            if hunk_match:
                line_num = int(hunk_match.group(1))
        elif line.startswith('+') and not line.startswith('+++') and current_file:
            if current_file.line_num is None and line_num is not None:
                current_file.line_num = line_num
            current_file.added_lines.append(line[1:].rstrip('\n'))
        elif line.startswith('-') and not line.startswith('---') and current_file:
            if current_file.line_num is None and line_num is not None:
                current_file.line_num = line_num
            current_file.removed_lines.append(line[1:].rstrip('\n'))
        elif current_file and (line.startswith(' ') or line.startswith('\\')):
            current_file.original_content += line
            current_file.new_content += line
        i += 1
    
    if current_file:
        file_changes.append(current_file)
    
    return file_changes