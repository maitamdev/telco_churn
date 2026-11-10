"""Verify the final Word document against its template, tables and rendered pages."""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from collections import Counter
import hashlib
import json
import re
from tools.report_tables import load_tables

ROOT = Path(__file__).resolve().parents[1]
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = '{' + NS['w'] + '}'


def text(e):
    return ''.join(e.xpath('.//w:t/text()', namespaces=NS))


def normalize(s):
    return re.sub(r'\s+', '', s.replace('\u200b', '')).casefold()


def signature(e):
    return e.tag, sorted(e.attrib.items()), e.text or '', [signature(c) for c in e]


def verify():
    report = ROOT / 'reports/BAOCAO-TTNT.docx'
    template = ROOT / 'reports/templates/MAU_BAO_CAO_GOC.docx'
    source = template  # The bundled original is verified by its fixed SHA-256.
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    expected_sha = 'd48a769fe78a38063f9985502c1ee35b8822a055a6cf74e99c49c4555d2b7cab'
    assert sha(source) == sha(template) == expected_sha, 'Source template changed'
    pages = json.loads((ROOT / 'tmp/report_upgrade/rendered/pages.json').read_text(encoding='utf-8'))
    build = json.loads((ROOT / 'reports/evidence/report_build.json').read_text(encoding='utf-8'))
    reviewed = json.loads((ROOT / 'tmp/report_upgrade/visual_review.json').read_text(encoding='utf-8'))
    assert reviewed['pages'] == list(range(1, len(pages)+1))
    assert 0 < len(pages) < 100
    assert reviewed['document_sha256'] == sha(report), 'Visual review is stale'
    figures, tables, references = len(build['figures']), len(build['tables']), len(build['reference_order'])
    with ZipFile(report) as z, ZipFile(template) as original:
        assert z.testzip() is None
        document = E.fromstring(z.read('word/document.xml'))
        source_document = E.fromstring(original.read('word/document.xml'))
        preserved = {}
        for name in ['word/styles.xml', 'word/numbering.xml', 'word/fontTable.xml', 'word/theme/theme1.xml']:
            before, after = original.read(name), z.read(name)
            same = signature(E.fromstring(before)) == signature(E.fromstring(after))
            assert same, 'Formatting part changed: ' + name
            preserved[name] = {'semantic_match': same, 'byte_match': before == after}
        geometry = lambda d: [[signature(c) for c in s if E.QName(c).localname in ['pgSz', 'pgMar', 'pgNumType', 'type']] for s in d.findall('.//w:sectPr', NS)]
        assert geometry(document) == geometry(source_document)
        assert not any('comment' in name.lower() for name in z.namelist())
        assert not document.xpath('//w:ins|//w:del|//w:commentRangeStart|//w:commentReference', namespaces=NS)

        body_text = text(document)
        for bad in ['PHỤ LỤC', 'Mai Trần Thiện Tâm', 'MAI TRẦN THIỆN TÂM', 'NGUYỄN THANH TIẾN', 'CT07PM', 'TODO', 'Error!', 'POS BÁN HÀNG', 'Ghi chú AI']:
            assert bad not in body_text, 'Unexpected report content: ' + bad
        for removed in ['LỜI CAM ĐOAN', 'Phạm vi hỗ trợ của công cụ AI', 'OpenAI Codex', 'docs/AI_USAGE.md', 'Bảng đóng góp', 'hồ sơ đóng góp riêng']:
            assert removed.casefold() not in body_text.casefold(), 'Removed section remains: ' + removed

        # Cached page references must point to a real bookmark and matching PDF page.
        bookmarks = {b.get(W+'name'): b for b in document.findall('.//w:bookmarkStart', NS)}
        page_labels = {page['text'].split()[0]: i + 1 for i, page in enumerate(pages[2:], start=2)}
        checked = []
        for link in document.findall('.//w:hyperlink', NS):
            instr = ''.join(link.xpath('.//w:instrText/text()', namespaces=NS))
            if 'PAGEREF' not in instr:
                continue
            name = re.search(r'PAGEREF\s+(\S+)', instr).group(1)
            assert name in bookmarks, 'Broken page reference ' + name
            label = link.xpath('.//w:t/text()', namespaces=NS)[-1]
            physical = page_labels[label]
            target = bookmarks[name].getparent()
            while target.tag != W+'p':
                target = target.getparent()
            assert normalize(text(target)) in normalize(pages[physical-1]['text']), (label, text(target))
            checked.append({'target': text(target), 'page_label': label, 'physical_page': physical})
        assert len(checked) >= len(build['headings']) + figures + tables

        captions = document.xpath('//w:body/w:p[w:pPr/w:pStyle[@w:val="Chuthich"]]', namespaces=NS)
        assert sum(text(p).startswith('Hình ') for p in captions) == figures
        assert sum(text(p).startswith('Bảng ') for p in captions) == tables
        actual_tables = document.findall('w:body/w:tbl', NS)[1:]
        source_text = (ROOT/'tools/report_content.md').read_text(encoding='utf-8')
        keys = [line[7:].split('|',1)[0] for line in source_text.splitlines() if line.startswith('@table ')]
        expected_tables = load_tables()
        assert len(actual_tables) == len(keys) == tables
        for key, table in zip(keys, actual_tables):
            cells = [[text(c) for c in row.findall('w:tc', NS)] for row in table.findall('w:tr', NS)]
            expected = [expected_tables[key]['headers']] + expected_tables[key]['rows']
            assert cells == [[str(x) for x in row] for row in expected], key

        citations = Counter(link.get(W+'anchor') for link in document.findall('.//w:hyperlink', NS) if (link.get(W+'anchor') or '').startswith('Reference_'))
        assert set(citations) == {f'Reference_{i}' for i in range(1,references+1)}
        assert all(name in bookmarks for name in citations)
        instructions = ' '.join(document.xpath('//w:instrText/text()', namespaces=NS))
        assert instructions.count(' TOC ') == 3
        assert len(document.xpath('//w:body/w:p[w:pPr/w:pStyle[@w:val="u1"]]', namespaces=NS)) == 12
        headings = document.xpath('//w:body/w:p[w:pPr/w:pStyle[@w:val="u1"]]', namespaces=NS)
        assert text(headings[-1]) == 'DANH MỤC TÀI LIỆU THAM KHẢO'
        assert f'[{references}]' in pages[-1]['text']

    qa = {
        'status':'passed', 'output':str(report), 'document_sha256':sha(report),
        'source_sha256':sha(source), 'source_unchanged':True,
        'pages':len(pages), 'chapters':build['chapters'], 'figures':figures, 'captioned_tables':tables,
        'glossary_tables':1, 'references':references,
        'automatic_tables_of_contents':3, 'page_references_checked':len(checked),
        'all_reference_bookmarks_resolve':True, 'all_tables_match_saved_artifacts':True,
        'format_parts':preserved, 'section_geometry_matches_template':True,
        'personal_fields_blank':True, 'no_appendix':True, 'references_are_last':True,
        'no_comments_or_tracked_changes':True,
        'visual_qa_complete':True, 'visually_reviewed_pages':reviewed['pages'],
        'visual_review_method':reviewed.get('note', 'All rendered pages visually inspected.'),
        'renderer':'Microsoft Word PDF export + bundled pypdfium2 at 1.35 scale',
        'render_fallback_reason':'render_docx.py unavailable because soffice.exe is not installed',
        'qa_pdf':'tmp/report_upgrade/BAO_CAO_QA.pdf',
        'qa_pdf_sha256':sha(ROOT/'tmp/report_upgrade/BAO_CAO_QA.pdf'),
        'page_references':checked,
        'declaration_section_present':False,
        'ai_assistance_section_present':False,
        'contribution_table_present':False,
        'remaining_user_input':'Personal/class/instructor information intentionally blank.'
    }
    (ROOT/'reports/evidence/report_qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    build.update(fields_refreshed=True,visual_qa_complete=True,pages=len(pages),final_sha256=sha(report))
    (ROOT/'reports/evidence/report_build.json').write_text(json.dumps(build,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:qa[k] for k in ['status','pages','chapters','figures','captioned_tables','references','page_references_checked','document_sha256']},ensure_ascii=False))


if __name__ == '__main__':
    verify()
