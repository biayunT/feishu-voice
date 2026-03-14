#!/usr/bin/env python3
"""
Convert audio files to opus format for Feishu voice messages.

Usage:
    python convert_to_opus.py <input_file> [output_file]

Examples:
    python convert_to_opus.py voice.mp3
    python convert_to_opus.py voice.mp3 voice.opus
    python convert_to_opus.py C:/path/to/voice.mp3
"""

import subprocess
import sys
import os
from pathlib import Path


def convert_to_opus(input_file: str, output_file: str = None, bitrate: str = "32k") -> str:
    """
    Convert audio file to opus format for Feishu voice messages.
    
    Args:
        input_file: Path to input audio file (mp3, wav, etc.)
        output_file: Path to output opus file (optional, defaults to same name with .opus)
        bitrate: Audio bitrate (default: 32k, good for voice)
    
    Returns:
        Path to the output opus file
    
    Raises:
        RuntimeError: If ffmpeg conversion fails
    """
    input_path = Path(input_file)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Default output file: same directory, same name, .opus extension
    if output_file is None:
        output_path = input_path.with_suffix(".opus")
    else:
        output_path = Path(output_file)
    
    # Build ffmpeg command
    cmd = [
        "ffmpeg",
        "-y",  # Overwrite output file
        "-i", str(input_path),
        "-c:a", "libopus",
        "-b:a", bitrate,
        str(output_path)
    ]
    
    # Run conversion
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg conversion failed: {result.stderr}")
    
    if not output_path.exists():
        raise RuntimeError(f"Output file not created: {output_path}")
    
    return str(output_path)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        output_path = convert_to_opus(input_file, output_file)
        print(f"Successfully converted to: {output_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()