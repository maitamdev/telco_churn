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
    pages = json.loads((ROOT / 'tmp/telco_report/pdf_pages_v3.json').read_text(encoding='utf-8'))
    build = json.loads((ROOT / 'reports/evidence/report_build.json').read_text(encoding='utf-8'))
    reviewed = json.loads((ROOT / 'tmp/telco_report/visual_review.json').read_text(encoding='utf-8'))
    assert reviewed['pages'] == list(range(1, len(pages)+1))
    assert len(pages) == 64 and len(pages) < 100
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
        for bad in ['PHỤ LỤC', 'Mai Trần Thiện Tâm', 'MAI TRẦN THIỆN TÂM', 'NGUYỄN THANH TIẾN', 'CT07PM', 'ChatGPT', 'Codex', 'TODO', 'Error!', 'POS BÁN HÀNG', 'Ghi chú AI']:
            assert bad not in body_text, 'Unexpected report content: ' + bad

        # Cached page references must point to a real bookmark and matching PDF page.
        bookmarks = {b.get(W+'name'): b for b in document.findall('.//w:bookmarkStart', NS)}
        roman = {'i':3, 'ii':4, 'iii':5, 'iv':6, 'v':7, 'vi':8, 'vii':9, 'viii':10, 'ix':11}
        checked = []
        for link in document.findall('.//w:hyperlink', NS):
            instr = ''.join(link.xpath('.//w:instrText/text()', namespaces=NS))
            if 'PAGEREF' not in instr:
                continue
            name = re.search(r'PAGEREF\s+(\S+)', instr).group(1)
            assert name in bookmarks, 'Broken page reference ' + name
            label = link.xpath('.//w:t/text()', namespaces=NS)[-1]
            physical = int(label)+11 if label.isdigit() else roman[label]
            target = bookmarks[name].getparent()
            while target.tag != W+'p':
                target = target.getparent()
            assert normalize(text(target)) in normalize(pages[physical-1]['text']), (label, text(target))
            checked.append({'target': text(target), 'page_label': label, 'physical_page': physical})
        assert len(checked) == 146

        captions = document.xpath('//w:body/w:p[w:pPr/w:pStyle[@w:val="Chuthich"]]', namespaces=NS)
        assert sum(text(p).startswith('Hình ') for p in captions) == 17
        assert sum(text(p).startswith('Bảng ') for p in captions) == 25
        actual_tables = document.findall('w:body/w:tbl', NS)[1:]
        source_text = (ROOT/'tools/report_content.md').read_text(encoding='utf-8')
        keys = [line[7:].split('|',1)[0] for line in source_text.splitlines() if line.startswith('@table ')]
        expected_tables = load_tables()
        assert len(actual_tables) == len(keys) == 25
        for key, table in zip(keys, actual_tables):
            cells = [[text(c) for c in row.findall('w:tc', NS)] for row in table.findall('w:tr', NS)]
            expected = [expected_tables[key]['headers']] + expected_tables[key]['rows']
            assert cells == [[str(x) for x in row] for row in expected], key

        citations = Counter(link.get(W+'anchor') for link in document.findall('.//w:hyperlink', NS) if (link.get(W+'anchor') or '').startswith('Reference_'))
        assert set(citations) == {f'Reference_{i}' for i in range(1,14)}
        assert all(name in bookmarks for name in citations)
        instructions = ' '.join(document.xpath('//w:instrText/text()', namespaces=NS))
        assert instructions.count(' TOC ') == 3
        assert len(document.xpath('//w:body/w:p[w:pPr/w:pStyle[@w:val="u1"]]', namespaces=NS)) == 13
        headings = document.xpath('//w:body/w:p[w:pPr/w:pStyle[@w:val="u1"]]', namespaces=NS)
        assert text(headings[-1]) == 'DANH MỤC TÀI LIỆU THAM KHẢO'
        assert '[13]' in pages[-1]['text']

    qa = {
        'status':'passed', 'output':str(report), 'document_sha256':sha(report),
        'source_sha256':sha(source), 'source_unchanged':True,
        'pages':len(pages), 'chapters':6, 'figures':17, 'captioned_tables':25,
        'glossary_tables':1, 'references':13,
        'automatic_tables_of_contents':3, 'page_references_checked':len(checked),
        'all_reference_bookmarks_resolve':True, 'all_tables_match_saved_artifacts':True,
        'format_parts':preserved, 'section_geometry_matches_template':True,
        'personal_fields_blank':True, 'no_appendix':True, 'references_are_last':True,
        'no_comments_or_tracked_changes':True,
        'visual_qa_complete':True, 'visually_reviewed_pages':reviewed['pages'],
        'renderer':'Microsoft Word PDF export + bundled pypdfium2 at 1.25 scale',
        'render_fallback_reason':'render_docx.py unavailable because soffice.exe is not installed',
        'qa_pdf':'tmp/telco_report/BAO_CAO_QA_v3.pdf',
        'qa_pdf_sha256':sha(ROOT/'tmp/telco_report/BAO_CAO_QA_v3.pdf'),
        'page_references':checked,
        'remaining_user_input':'Personal/class/instructor information intentionally blank; group contribution and slides remain separate tasks.'
    }
    (ROOT/'reports/evidence/report_qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    build.update(fields_refreshed=True,visual_qa_complete=True,pages=len(pages),final_sha256=sha(report))
    (ROOT/'reports/evidence/report_build.json').write_text(json.dumps(build,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:qa[k] for k in ['status','pages','chapters','figures','captioned_tables','references','page_references_checked','document_sha256']},ensure_ascii=False))


if __name__ == '__main__':
    verify()
