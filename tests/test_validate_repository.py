import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import pypdfium2 as pdfium

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from validate_repository import validate


class RepositoryValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pack = self.root / 'references/patents'
        self.source = self.pack / 'US1A1'
        self.source.mkdir(parents=True)
        self.pdf = self.source / 'original.pdf'
        with pdfium.PdfDocument.new() as document:
            document.new_page(200, 200)
            document.save(self.pdf)
        self.md = self.source / 'mineru.md'
        self.md.write_text('# Fixture\n\n<a id="p0001"></a>\n\n[PDF](original.pdf#page=1)\n', encoding='utf-8')
        (self.root / 'README.md').write_text('# 测试资料库\n\n[资料](references/patents/README.md)\n', encoding='utf-8')
        (self.pack / 'README.md').write_text('# 资料\n\n[全文](US1A1/mineru.md#p0001)\n', encoding='utf-8')
        (self.pack / 'QUALITY.md').write_text('# 质量\n', encoding='utf-8')
        self.row = {'publication': 'US1A1', 'pages': 1, 'original_pdf': 'US1A1/original.pdf',
                    'markdown': 'US1A1/mineru.md', 'source_sha256': self.digest(self.pdf)['sha256'],
                    'figures': 0, 'artifacts': {}}
        self.manifest = {'publications': 1, 'physical_pages': 1, 'semantic_fidelity_certified': False,
                         'records': [self.row]}
        self.refresh()

    def digest(self, path):
        return {'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

    def save(self):
        (self.pack / 'manifest.json').write_text(json.dumps(self.manifest), encoding='utf-8')

    def refresh(self):
        self.row['artifacts'] = {p.relative_to(self.source).as_posix(): self.digest(p)
                                 for p in self.source.rglob('*') if p.is_file()}
        self.save()

    def errors(self, **kwargs):
        return [e['code'] for e in validate(self.root, **kwargs)['errors']]

    def test_valid_real_pdf(self):
        self.assertEqual(self.errors(), [])

    def test_modified_pdf(self):
        self.pdf.write_bytes(self.pdf.read_bytes() + b'changed')
        self.assertIn('source_hash', self.errors())

    def test_actual_pdf_page_count(self):
        self.row['pages'] = 2
        self.manifest['physical_pages'] = 2
        self.md.write_text('<a id="p0001"></a>\n<a id="p0002"></a>\n', encoding='utf-8')
        self.refresh()
        self.assertIn('pdf_pages', self.errors())

    def test_duplicate_page_anchor(self):
        self.md.write_text('<a id="p0001"></a>\n<a id="p0001"></a>\n', encoding='utf-8')
        self.refresh()
        self.assertIn('page_anchors', self.errors())

    def test_missing_page_anchor(self):
        self.md.write_text('# Missing page\n', encoding='utf-8')
        self.refresh()
        self.assertIn('page_anchors', self.errors())

    def test_missing_image(self):
        self.md.write_text(self.md.read_text('utf-8') + '\n![图](figures/missing.png)\n', encoding='utf-8')
        self.refresh()
        self.assertIn('missing_link', self.errors())

    def test_duplicate_publication(self):
        self.manifest['records'].append(self.row.copy())
        self.manifest['publications'] = 2
        self.manifest['physical_pages'] = 2
        self.save()
        self.assertIn('duplicate_publication', self.errors())

    def test_path_escape(self):
        self.row['artifacts']['../../outside.txt'] = {'bytes': 0, 'sha256': '0' * 64}
        self.save()
        self.assertIn('unsafe_path', self.errors())

    def test_artifact_hash(self):
        self.md.write_text(self.md.read_text('utf-8') + '\nchanged\n', encoding='utf-8')
        self.assertIn('artifact_hash', self.errors())

    def test_unregistered_file(self):
        (self.source / 'extra.txt').write_text('unlisted', encoding='utf-8')
        self.assertIn('unregistered_file', self.errors())

    def test_bad_manifest_counts(self):
        self.manifest['physical_pages'] = 200
        self.save()
        self.assertIn('manifest_totals', self.errors())

    def test_invalid_pdf_reports_error(self):
        self.pdf.write_bytes(b'not a PDF')
        self.row['source_sha256'] = self.digest(self.pdf)['sha256']
        self.refresh()
        self.assertIn('invalid_pdf', self.errors())

    def test_unknown_semantic_certification_rejected(self):
        self.manifest['semantic_fidelity_certified'] = True
        self.save()
        self.assertIn('semantic_certification', self.errors())

    def test_management_document_fragment(self):
        (self.root / 'README.md').write_text('# 首页\n\n[有效](docs/guide.md#使用方法)\n', encoding='utf-8')
        (self.root / 'docs').mkdir()
        guide = self.root / 'docs/guide.md'
        guide.write_text('# 指南\n\n## 使用方法\n', encoding='utf-8')
        self.assertEqual(self.errors(), [])
        guide.write_text('# 指南\n', encoding='utf-8')
        self.assertIn('missing_anchor', self.errors())

    def test_invalid_schema_and_empty_records(self):
        for value in [[], {'records': []}, {'records': 'bad'}]:
            (self.pack / 'manifest.json').write_text(json.dumps(value), encoding='utf-8')
            with self.subTest(value=value):
                self.assertIn('invalid_manifest', self.errors())

    def test_baseline_protects_pdf_even_if_manifest_updated(self):
        def git(*args):
            return subprocess.check_output(['git', '-C', str(self.root), *args], stderr=subprocess.DEVNULL).decode().strip()
        git('init', '-q')
        git('add', '.')
        git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'baseline')
        base = git('rev-parse', 'HEAD')
        self.pdf.write_bytes(self.pdf.read_bytes() + b'changed')
        self.row['source_sha256'] = self.digest(self.pdf)['sha256']
        self.refresh()
        self.assertIn('original_changed', self.errors(base=base))

    def test_cli_returns_failure_for_invalid_material(self):
        script = Path(__file__).resolve().parents[1] / 'tools/validate_repository.py'
        command = [sys.executable, str(script), '--root', str(self.root)]
        valid = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(valid.returncode, 0, valid.stderr)
        self.assertEqual(json.loads(valid.stdout)['publications'], 1)
        self.md.write_text('# Broken\n', encoding='utf-8')
        broken = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(broken.returncode, 1)
        self.assertIn('page_anchors', [e['code'] for e in json.loads(broken.stdout)['errors']])

    def test_document_symlink_cannot_read_outside_repository(self):
        with tempfile.TemporaryDirectory() as other:
            outside = Path(other) / 'outside.md'
            outside.write_text('# Outside fixture\n', encoding='utf-8')
            link = self.root / 'linked.md'
            try:
                link.symlink_to(outside)
            except OSError:
                # Windows may deny unprivileged symlink creation. Model only
                # OS path resolution there; Linux CI exercises the real link.
                link.write_text('# Link fixture\n', encoding='utf-8')
                original = Path.resolve
                def resolve(path, *args, **kwargs):
                    return outside if path == link else original(path, *args, **kwargs)
                with mock.patch.object(Path, 'resolve', resolve):
                    self.assertIn('unsafe_document', self.errors())
                return
            self.assertIn('unsafe_document', self.errors())

    def add_paper(self):
        self.paper_dir = self.root / 'references/papers/budget-design'
        self.paper_dir.mkdir(parents=True)
        self.paper_pdf = self.pack / 'Budget Design.pdf'
        self.paper_pdf.write_bytes(self.pdf.read_bytes())
        self.paper_md = self.paper_dir / 'mineru.md'
        self.paper_md.write_text('<a id="p0001"></a>\n\n[PDF](../../patents/Budget%20Design.pdf#page=1)\n', encoding='utf-8')
        (self.paper_dir.parent / 'README.md').write_text('# Papers\n', encoding='utf-8')
        self.paper_row = {'id': 'budget-design', 'pages': 1,
                          'original_pdf': 'references/patents/Budget Design.pdf',
                          'markdown': 'budget-design/mineru.md', 'figures': 0,
                          'source_sha256': self.digest(self.paper_pdf)['sha256'],
                          'artifacts': {p.relative_to(self.root).as_posix(): self.digest(p)
                                        for p in [self.paper_pdf, self.paper_md]}}
        self.papers = {'papers': 1, 'physical_pages': 1, 'semantic_fidelity_certified': False,
                       'records': [self.paper_row]}
        self.save_papers()

    def save_papers(self):
        (self.paper_dir.parent / 'manifest.json').write_text(json.dumps(self.papers), encoding='utf-8')

    def test_registered_paper_keeps_legacy_pdf_path(self):
        self.add_paper()
        report = validate(self.root)
        self.assertEqual(report['errors'], [])
        self.assertEqual(report.get('papers'), 1)
        self.assertEqual(report.get('paper_physical_pages'), 1)
        self.assertEqual(report['publications'], 1)

    def test_paper_missing_image_is_detected(self):
        self.add_paper()
        image_path = self.paper_dir / 'images/chart.png'
        image_path.parent.mkdir()
        image_path.write_bytes(b'image fixture')
        self.paper_row['artifacts'][image_path.relative_to(self.root).as_posix()] = self.digest(image_path)
        self.paper_row['figures'] = 1
        self.save_papers()
        image_path.unlink()
        self.assertIn('missing_artifact', self.errors())

    def test_paper_markdown_hash_is_checked(self):
        self.add_paper()
        self.paper_md.write_text(self.paper_md.read_text('utf-8') + 'changed', encoding='utf-8')
        self.assertIn('artifact_hash', self.errors())

    def test_paper_physical_pages_and_anchors_are_checked(self):
        self.add_paper()
        self.paper_row['pages'] = 2
        self.papers['physical_pages'] = 2
        self.save_papers()
        errors = self.errors()
        self.assertIn('pdf_pages', errors)
        self.assertIn('page_anchors', errors)

    def test_paper_unregistered_file_is_detected(self):
        self.add_paper()
        (self.paper_dir / 'extra.txt').write_text('not registered', encoding='utf-8')
        errors = validate(self.root)['errors']
        self.assertTrue(any(e['code'] == 'unregistered_file' and e['path'].endswith('extra.txt') for e in errors))

    def test_paper_unsafe_artifact_is_rejected(self):
        self.add_paper()
        self.paper_row['artifacts']['../outside.txt'] = {'bytes': 0, 'sha256': '0' * 64}
        self.save_papers()
        self.assertIn('unsafe_path', self.errors())

    def test_paper_duplicate_ids_and_totals_are_checked(self):
        self.add_paper()
        self.papers['records'].append(self.paper_row.copy())
        self.save_papers()
        self.assertIn('duplicate_paper', self.errors())
        self.assertIn('manifest_totals', self.errors())

    def test_paper_manifest_required_when_directory_exists(self):
        self.add_paper()
        (self.paper_dir.parent / 'manifest.json').unlink()
        self.assertIn('invalid_manifest', self.errors())

    def test_legacy_paper_pdf_cannot_be_modified_even_with_updated_hash(self):
        self.add_paper()
        def git(*args):
            return subprocess.check_output(['git', '-C', str(self.root), *args], stderr=subprocess.DEVNULL).decode().strip()
        git('init', '-q')
        git('add', '.')
        git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'baseline')
        base = git('rev-parse', 'HEAD')
        self.paper_pdf.write_bytes(self.paper_pdf.read_bytes() + b'changed')
        self.paper_row['source_sha256'] = self.digest(self.paper_pdf)['sha256']
        self.paper_row['artifacts'][self.paper_row['original_pdf']] = self.digest(self.paper_pdf)
        self.save_papers()
        self.assertIn('original_changed', self.errors(base=base))


if __name__ == '__main__':
    unittest.main()
