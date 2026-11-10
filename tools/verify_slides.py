"""Record QA only after finalization, native PowerPoint rendering and visual review."""
from pathlib import Path
from zipfile import ZipFile
import hashlib
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / 'tmp/slides_upgrade'
NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify():
    output = ROOT / 'reports/BAO_VE_TELCO_CHURN.pptx'
    receipt = read(BUILD / 'validation.json')
    review = read(BUILD / 'visual_review.json')
    native = read(BUILD / 'native/native_inventory.json')
    assert receipt['finalSha256'] == review['presentation_sha256'] == sha(output)
    assert review['slides'] == list(range(1, 22))
    assert len(native) == 21
    assert receipt['firstPartyImport']['passed']
    assert receipt['packageIntegrity']['findingCount'] == 0
    assert receipt['presentationLayout']['findingCount'] == 0
    assert receipt['fontSelection']['passed']
    assert sum(x['charts'] for x in native) == 3
    images = {f'slide-{i:02}.png': sha(BUILD / f'native/slide-{i:02}.png') for i in range(1, 22)}
    assert review['rendered_sha256'] == images, 'Visual review is stale'
    with ZipFile(output) as archive:
        assert archive.testzip() is None
        for i in range(1, 22):
            notes = ET.fromstring(archive.read(f'ppt/notesSlides/notesSlide{i}.xml'))
            assert 'https://github.com/maitamdev/telco_churn' in ''.join(notes.itertext())
        # The screenshot must be embedded; a path-only linked image fails in Office.
        media = [name for name in archive.namelist() if name.startswith('ppt/media/')]
        assert media and any(archive.read(name).startswith(b'\xff\xd8') for name in media)
        metrics = read(ROOT / 'artifacts/final_run/test_metrics.json')['metrics']
        page = ET.fromstring(archive.read('ppt/slides/slide9.xml'))
        rows = page.findall('.//a:tbl/a:tr', NS)
        assert len(rows) == 6
        for row, metric in zip(rows[1:], metrics):
            values = [''.join(cell.itertext()) for cell in row.findall('a:tc', NS)]
            expected = [f'{metric[k]:.3f}'.replace('.', ',') for k in
                        ['precision_churn', 'recall_churn', 'f1_churn', 'average_precision']]
            assert values[1:] == expected, (values, expected)
    qa = {'status': 'passed', 'presentation_sha256': sha(output), 'slides': 21,
          'output': 'reports/BAO_VE_TELCO_CHURN.pptx', 'visual_qa_complete': True,
          'visually_reviewed_slides': review['slides'], 'renderer': 'Microsoft PowerPoint PNG export, 1280x720',
          'native_inventory': native, 'rendered_sha256': images,
          'package_integrity_passed': True, 'layout_and_font_checks_passed': True,
          'first_party_import_passed': True, 'notes_with_sources': 21,
          'test_metrics_table_matches_artifact': True, 'screenshot_embedded': True,
          'native_chart_workbooks_verified': receipt['chartDataPackaging']['portable_chart_validation_passed'],
          'sources': {name: sha(ROOT / name) for name in
                      ['artifacts/final_run/metadata.json', 'artifacts/final_run/test_metrics.json',
                       'artifacts/diagnostics/summary.json', 'tools/build_slides.mjs']},
          'resolved_findings': ['Arial encoded explicitly', 'Demo screenshot embedded as JPEG bytes and rechecked in PowerPoint'],
          'remaining_user_input': 'Actual member identities, contributions and rehearsal; speaker notes are a guide.'}
    (ROOT / 'reports/evidence/slides_qa.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('Slides passed: 21 rendered and visually reviewed, native tables/charts, sources, metric parity and embedded screenshot.')


if __name__ == '__main__':
    verify()
