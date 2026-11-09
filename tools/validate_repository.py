"""Validate local source integrity and documentation; never certify OCR semantics."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
from urllib.parse import unquote, urlsplit

import pypdfium2 as pdfium

PACK = Path('references/patents')
SKIP = {'.git', '.venv', '__pycache__', 'work', 'outputs', 'node_modules'}


def anchors(text):
    result = set(re.findall(r'\bid=["\x27]([^"\x27]+)["\x27]', text))
    counts = {}
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', text, re.M):
        slug = re.sub(r'[^\w\- ]', '', heading.lower(), flags=re.UNICODE).replace(' ', '-')
        n = counts.get(slug, 0)
        counts[slug] = n + 1
        result.add(slug if n == 0 else f'{slug}-{n}')
    return result


def validate(root, base=None):
    root = Path(root).resolve()
    pack = root / PACK
    result = {'scope': 'source bytes, actual PDF pages, Markdown anchors, local links and original preservation',
              'semantic_fidelity_certified': False, 'publications': 0, 'physical_pages': 0,
              'figures': 0, 'artifact_files': 0, 'markdown_files': 0, 'local_links': 0,
              'papers': 0, 'paper_physical_pages': 0, 'paper_figures': 0, 'paper_artifact_files': 0,
              'baseline_checked': False, 'errors': [],
              'warnings': ['Structural checks do not certify OCR accuracy, formulas, reading order or technical conclusions.']}

    def issue(code, path, detail):
        result['errors'].append({'code': code, 'path': str(path), 'detail': str(detail)})

    def relative(path):
        return path.relative_to(root).as_posix()

    def safe_path(parent, value):
        if not isinstance(value, str) or not value or '\\' in value or ':' in value:
            raise ValueError(f'Invalid relative path: {value!r}')
        parts = PurePosixPath(value)
        path = (parent / value).resolve()
        if parts.is_absolute() or '..' in parts.parts or not path.is_relative_to(parent.resolve()):
            raise ValueError(f'Path escapes source directory: {value}')
        return path

    def sha(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    pdf_counts = {}

    def pdf_pages(path):
        if path not in pdf_counts:
            with pdfium.PdfDocument(path) as doc:
                pdf_counts[path] = len(doc)
        return pdf_counts[path]

    # Papers have their own manifest. Existing uploaded originals keep their
    # repository path, even when they predate the papers directory.
    paper_pack = root / 'references/papers'
    paper_sources = set()
    if paper_pack.exists():
        try:
            paper_manifest = json.loads((paper_pack / 'manifest.json').read_text('utf-8'))
            if not isinstance(paper_manifest, dict) or not isinstance(paper_manifest.get('records'), list) or not paper_manifest['records']:
                raise ValueError('Expected a nonempty paper records list')
            if paper_manifest.get('semantic_fidelity_certified') is not False:
                issue('semantic_certification', 'references/papers', 'Automated checks must not certify semantic fidelity')
            paper_registered = {paper_pack / n for n in ['README.md', 'manifest.json']}
            paper_ids = set()
            for row in paper_manifest['records']:
                pid = row['id']
                if not isinstance(pid, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', pid):
                    raise ValueError(f'Invalid paper identifier: {pid!r}')
                if pid in paper_ids:
                    issue('duplicate_paper', 'references/papers', pid)
                paper_ids.add(pid)
                directory = safe_path(paper_pack, pid)
                source = safe_path(root, row['original_pdf'])
                markdown = safe_path(paper_pack, row['markdown'])
                if not source.is_relative_to(root / 'references') or source.suffix.lower() != '.pdf':
                    raise ValueError('Paper original must be a PDF under references/')
                if markdown != directory / 'mineru.md':
                    raise ValueError('Expected paper-id/mineru.md')
                count = row['pages']
                if type(count) is not int or count < 1:
                    raise ValueError(f'Invalid physical page count: {pid}')
                result['paper_physical_pages'] += count
                paper_sources.add(source)
                if not source.is_file():
                    issue('missing_source', pid, row['original_pdf'])
                else:
                    if sha(source) != row['source_sha256']:
                        issue('source_hash', pid, 'Original SHA-256 mismatch')
                    try:
                        if pdf_pages(source) != count:
                            issue('pdf_pages', pid, 'Actual PDF count differs from manifest')
                    except Exception as exc:
                        issue('invalid_pdf', pid, exc)
                if not markdown.is_file():
                    issue('missing_markdown', pid, row['markdown'])
                elif re.findall(r'<a id="p(\d{4})"></a>', markdown.read_text('utf-8')) != [f'{n:04d}' for n in range(1, count + 1)]:
                    issue('page_anchors', pid, 'Page anchors must occur exactly once in physical order')
                artifacts = row['artifacts']
                if not isinstance(artifacts, dict) or not {relative(source), relative(markdown)}.issubset(artifacts):
                    raise ValueError(f'Expected original and Markdown artifact records: {pid}')
                for name, expected in artifacts.items():
                    try:
                        path = safe_path(root, name)
                        if path != source and not path.is_relative_to(directory):
                            raise ValueError('Paper artifacts must belong to the paper directory')
                    except ValueError as exc:
                        issue('unsafe_path', pid, exc)
                        continue
                    paper_registered.add(path)
                    result['paper_artifact_files'] += 1
                    if not path.is_file():
                        issue('missing_artifact', relative(path), 'Registered artifact missing')
                    elif sha(path) != expected['sha256'] or path.stat().st_size != expected['bytes']:
                        issue('artifact_hash', relative(path), 'Artifact bytes/SHA-256 mismatch')
                figures = len([p for p in (directory / 'images').rglob('*')
                               if p.is_file() and p.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp', '.svg'}])
                result['paper_figures'] += figures
                if figures != row['figures']:
                    issue('figure_count', pid, 'Figure count differs from manifest')
            result['papers'] = len(paper_ids)
            if paper_manifest['papers'] != len(paper_ids) or paper_manifest['physical_pages'] != result['paper_physical_pages']:
                issue('manifest_totals', 'references/papers', 'Declared totals differ from records')
            for path in paper_pack.rglob('*'):
                if path.is_file() and path.resolve() not in paper_registered:
                    issue('unregistered_file', relative(path), 'File absent from paper manifest')
            for path in paper_registered:
                if not path.is_file():
                    issue('missing_artifact', relative(path), 'Required paper file missing')
        except (OSError, UnicodeError, ValueError, TypeError, KeyError) as exc:
            issue('invalid_manifest', 'references/papers/manifest.json', exc)

    try:
        manifest = json.loads((pack / 'manifest.json').read_text('utf-8'))
        if not isinstance(manifest, dict) or not isinstance(manifest.get('records'), list) or not manifest['records']:
            raise ValueError('Expected a nonempty records list')
        rows = manifest['records']
        if any(not isinstance(row, dict) for row in rows):
            raise ValueError('Every record must be an object')
        if manifest.get('semantic_fidelity_certified') is not False:
            issue('semantic_certification', PACK, 'Automated checks must not certify semantic fidelity')
        registered = {pack / n for n in ['README.md', 'QUALITY.md', 'manifest.json']} | paper_sources
        ids = set()
        for row in rows:
            pid = row['publication']
            if not isinstance(pid, str) or not re.fullmatch(r'(?:CN|DE|EP|JP|KR|US|WO)\d+[A-Z]\d?', pid):
                raise ValueError(f'Invalid publication identifier: {pid!r}')
            if pid in ids:
                issue('duplicate_publication', PACK, pid)
            ids.add(pid)
            directory = safe_path(pack, pid)
            count = row['pages']
            if type(count) is not int or count < 1:
                raise ValueError(f'Invalid physical page count: {pid}')
            result['physical_pages'] += count
            source = safe_path(pack, row['original_pdf'])
            markdown = safe_path(pack, row['markdown'])
            if source != directory / 'original.pdf' or markdown != directory / 'mineru.md':
                issue('source_layout', pid, 'Expected publication/original.pdf and publication/mineru.md')
            if not source.is_file():
                issue('missing_source', pid, row['original_pdf'])
            else:
                if sha(source) != row['source_sha256']:
                    issue('source_hash', pid, 'Original SHA-256 mismatch')
                try:
                    if pdf_pages(source) != count:
                        issue('pdf_pages', pid, 'Actual PDF count differs from manifest')
                except Exception as exc:
                    issue('invalid_pdf', pid, exc)
            if not markdown.is_file():
                issue('missing_markdown', pid, row['markdown'])
            else:
                text = markdown.read_text('utf-8')
                actual = re.findall(r'<a id="p(\d{4})"></a>', text)
                if actual != [f'{n:04d}' for n in range(1, count + 1)]:
                    issue('page_anchors', pid, 'Page anchors must occur exactly once in physical order')
            artifacts = row['artifacts']
            if not isinstance(artifacts, dict) or not {'original.pdf', 'mineru.md'}.issubset(artifacts):
                raise ValueError(f'Expected original and Markdown artifact records: {pid}')
            for name, expected in artifacts.items():
                try:
                    path = safe_path(directory, name)
                except ValueError as exc:
                    issue('unsafe_path', pid, exc)
                    continue
                registered.add(path)
                result['artifact_files'] += 1
                if not path.is_file():
                    issue('missing_artifact', relative(path), 'Registered artifact missing')
                elif sha(path) != expected['sha256'] or path.stat().st_size != expected['bytes']:
                    issue('artifact_hash', relative(path), 'Artifact bytes/SHA-256 mismatch')
            figures = len(list((directory / 'figures').glob('*.png')))
            result['figures'] += figures
            if figures != row['figures']:
                issue('figure_count', pid, 'Figure count differs from manifest')
        result['publications'] = len(ids)
        if manifest['publications'] != len(ids) or manifest['physical_pages'] != result['physical_pages']:
            issue('manifest_totals', PACK, 'Declared totals differ from records')
        for path in pack.rglob('*'):
            if path.is_file() and path.resolve() not in registered:
                issue('unregistered_file', relative(path), 'File absent from source manifest')
        for path in registered:
            if not path.is_file():
                issue('missing_artifact', relative(path), 'Required material file missing')
    except (OSError, UnicodeError, ValueError, TypeError, KeyError) as exc:
        issue('invalid_manifest', PACK / 'manifest.json', exc)

    for path in root.rglob('*.md'):
        if any(part in SKIP for part in path.relative_to(root).parts):
            continue
        if not path.resolve().is_relative_to(root):
            issue('unsafe_document', relative(path), 'Document resolves outside repository')
            continue
        result['markdown_files'] += 1
        try:
            text = path.read_text('utf-8')
            text = re.sub(r'^```.*?^```[^\n]*$', '', text, flags=re.M | re.S)
            for match in re.finditer(r'!?\[[^\]]*\]\((<[^>]+>|[^\s)]+)\)', text):
                target = match.group(1).strip('<>')
                url = urlsplit(target)
                if url.scheme or url.netloc:
                    continue
                destination = (path.parent / unquote(url.path)).resolve() if url.path else path
                result['local_links'] += 1
                if not destination.is_relative_to(root):
                    issue('unsafe_link', relative(path), target)
                elif not destination.is_file():
                    issue('missing_link', relative(path), target)
                elif url.fragment and destination.suffix == '.md':
                    if unquote(url.fragment) not in anchors(destination.read_text('utf-8')):
                        issue('missing_anchor', relative(path), target)
                elif url.fragment.startswith('page=') and destination.suffix.lower() == '.pdf':
                    try:
                        if not 1 <= int(url.fragment[5:]) <= pdf_pages(destination):
                            issue('pdf_page_link', relative(path), target)
                    except Exception as exc:
                        issue('pdf_page_link', relative(path), exc)
        except (OSError, UnicodeError, ValueError) as exc:
            issue('invalid_markdown', relative(path), exc)

    if base and set(base) != {'0'}:
        if not re.fullmatch(r'[0-9a-fA-F]{7,40}', base):
            issue('invalid_base', 'git', 'Expected commit SHA')
        else:
            try:
                fields = subprocess.check_output(['git', '-C', str(root), 'diff', '--no-renames', '--name-status',
                                                   '-z', base, '--', 'references'], stderr=subprocess.PIPE).decode('utf-8').split('\0')
                result['baseline_checked'] = True
                for status, name in zip(fields[::2], fields[1::2]):
                    if name.lower().endswith('.pdf') and status != 'A':
                        issue('original_changed', name, 'Existing originals are append-only; preserve prior bytes and use a new version path')
            except (OSError, subprocess.CalledProcessError) as exc:
                issue('baseline_failed', 'git', exc)
    else:
        result['warnings'].append('No nonzero baseline supplied; original immutability relative to Git history was not checked.')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--base', help='Commit SHA before the change, or PR base SHA')
    args = parser.parse_args()
    report = validate(args.root, args.base)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(bool(report['errors']))
