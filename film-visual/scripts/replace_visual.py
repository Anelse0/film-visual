#!/usr/bin/env python3
"""Exact, fail-closed byte replacement. Semantics and authorization stay with the user/agent."""
import argparse
import hashlib
import json
from pathlib import Path


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def apply_patch_bytes(original, plan):
    if not isinstance(plan, dict) or set(plan) != {"sha256", "edits"}:
        raise ValueError("expected sha256 and edits only")
    if plan["sha256"] != sha256(original):
        raise ValueError("input changed: SHA-256 mismatch")
    edits = plan["edits"]
    if not isinstance(edits, list) or not edits:
        raise ValueError("edits must be a nonempty list")
    normalized = []
    for item in edits:
        if not isinstance(item, dict) or set(item) != {"start", "end", "old_hex", "new_hex"}:
            raise ValueError("invalid edit fields")
        start, end = item["start"], item["end"]
        if type(start) is not int or type(end) is not int:
            raise ValueError("offsets must be integers")
        if not 0 <= start < end <= len(original):
            raise ValueError("empty or out-of-bounds range")
        if not isinstance(item["old_hex"], str) or not isinstance(item["new_hex"], str):
            raise ValueError("hex values must be strings")
        try:
            old, new = bytes.fromhex(item["old_hex"]), bytes.fromhex(item["new_hex"])
        except ValueError as exc:
            raise ValueError("invalid hexadecimal bytes") from exc
        if original[start:end] != old:
            raise ValueError("selected original bytes do not match")
        normalized.append((start, end, new))
    normalized.sort(key=lambda item: item[0])
    cursor = 0
    chunks = []
    checks = []
    out_offset = 0
    for start, end, new in normalized:
        if start < cursor:
            raise ValueError("overlapping edit ranges")
        unchanged = original[cursor:start]
        chunks.extend((unchanged, new))
        checks.append((cursor, start, out_offset))
        out_offset += len(unchanged) + len(new)
        cursor = end
    chunks.append(original[cursor:])
    checks.append((cursor, len(original), out_offset))
    result = b"".join(chunks)
    for start, end, offset in checks:
        if result[offset:offset + end - start] != original[start:end]:
            raise AssertionError("unauthorized bytes changed")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--patch", required=True, type=Path)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        original = args.input.read_bytes()
        plan = json.loads(args.patch.read_text(encoding="utf-8"))
        result = apply_patch_bytes(original, plan)
        if args.output is not None:
            # x refuses existing files and symlinks; no source overwrite or implicit dirs.
            if args.output.resolve() == args.input.resolve():
                raise ValueError("output must be a new file, preserving the original")
            if args.input.read_bytes() != original:
                raise ValueError("input changed while preparing output")
            with args.output.open("xb") as stream:
                stream.write(result)
        print(json.dumps({"mode": "check" if args.check else "written",
                          "input_sha256": sha256(original), "output_sha256": sha256(result),
                          "edits": len(plan["edits"]), "outside_bytes_unchanged": True},
                         ensure_ascii=False))
    except (OSError, ValueError, TypeError) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    main()
