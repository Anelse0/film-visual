#!/usr/bin/env python3
"""Build or verify the self-contained Skill ZIP using Python's standard library."""
import argparse
import hashlib
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'film-visual'


def source_files():
    files = {}
    for path in sorted(SOURCE.rglob('*')):
        if path.is_symlink():
            raise ValueError(f'symlink in skill: {path}')
        if not path.is_file() or '__pycache__' in path.parts or path.name == '.DS_Store' or path.suffix == '.pyc':
            continue
        files[path.relative_to(ROOT).as_posix()] = path.read_bytes()
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    version = (SOURCE / 'VERSION').read_text().strip()
    archive = ROOT / 'dist' / f'film-visual-{version}.zip'
    checksums = archive.parent / 'SHA256SUMS'
    expected = source_files()
    if not args.check:
        archive.parent.mkdir(exist_ok=True)
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for name, data in expected.items():
                info = zipfile.ZipInfo(name, (2020, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                z.writestr(info, data)
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        checksums.write_text(f'{digest}  {archive.name}\n')
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:
            raise ValueError('ZIP CRC check failed')
        actual = {name: z.read(name) for name in z.namelist()}
        if len(z.namelist()) != len(actual) or actual != expected:
            raise ValueError('ZIP contents differ from source')
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if checksums.read_text() != f'{digest}  {archive.name}\n':
        raise ValueError('SHA256SUMS mismatch')
    print(f'{archive.name}: {len(expected)} files, source match, CRC and SHA256 verified')


if __name__ == '__main__':
    main()
