"""Fill a copy of the supplied DOCX package while retaining its formatting parts."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from copy import deepcopy
from collections import defaultdict
import hashlib, json, re
from lxml import etree as E
from PIL import Image
from tools.report_tables import load_tables, REFERENCES

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'reports/templates/MAU_BAO_CAO_GOC.docx'
OUT=ROOT/'reports/BAOCAO-TTNT.docx'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
    'wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'pic':'http://schemas.openxmlformats.org/drawingml/2006/picture',
    'm':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
REL='http://schemas.openxmlformats.org/package/2006/relationships'
CT='http://schemas.openxmlformats.org/package/2006/content-types'

def tag(s):
    a,b=s.split(':');return '{'+NS[a]+'}'+b
def node(s, text=None, **attrs):
    e=E.Element(tag(s))
    for k,v in attrs.items():e.set(tag(k) if ':' in k else k,str(v))
    if text is not None:e.text=str(text)
    return e
def prop(e, name, **attrs):
    old=e.find(tag(name))
    if old is not None:e.remove(old)
    e.append(node(name,**attrs))
def xml(e):return E.tostring(e,encoding='UTF-8',xml_declaration=True,standalone=True)

class Report:
    def __init__(self):
        with ZipFile(SOURCE) as z:self.parts={n:z.read(n) for n in z.namelist()}
        self.doc=E.fromstring(self.parts['word/document.xml'])
        self.body=self.doc.find('w:body',NS)
        self.original=list(deepcopy(self.body))
        self.tables=self.body.findall('w:tbl',NS)
        self.rels=E.fromstring(self.parts['word/_rels/document.xml.rels'])
        self.ct=E.fromstring(self.parts['[Content_Types].xml'])
        self.bookmark=20000;self.relid=20000;self.drawingid=20000
        self.chapter=0;self.count=defaultdict(int);self.heading_counts=[0,0,0]
        self.headings=[];self.figures=[];self.tablelist=[]
        self.content=(ROOT/'tools/report_content.md').read_text(encoding='utf-8')
        cited=list(dict.fromkeys(int(x) for x in re.findall(r'\[(\d+)\]',self.content)))
        self.citemap={old:i+1 for i,old in enumerate(cited)}
        self.references=[REFERENCES[i-1] for i in cited]
        for e in list(self.body):self.body.remove(e)

    def run(self,text, rpr=None):
        r=node('w:r')
        if rpr is not None:r.append(deepcopy(rpr))
        t=node('w:t',text);t.set('{http://www.w3.org/XML/1998/namespace}space','preserve');r.append(t)
        return r

    def text(self,p,text,rpr=None,citations=True):
        for token in re.split(r'(\[\d+\])',str(text)):
            m=re.fullmatch(r'\[(\d+)\]',token)
            if m and citations:
                i=self.citemap[int(m.group(1))]
                link=node('w:hyperlink',**{'w:anchor':f'Reference_{i}','w:history':'1'})
                link.append(self.run(f'[{i}]',rpr));p.append(link)
            else:p.append(self.run(token,rpr))

    def p(self,text='',style=None,base=14,append=True,citations=True):
        p=node('w:p');old=self.original[base]
        pp=old.find('w:pPr',NS)
        if pp is not None:p.append(deepcopy(pp))
        else:p.append(node('w:pPr'))
        pp=p.find('w:pPr',NS)
        for x in list(pp):
            if E.QName(x).localname in ['sectPr','numPr']:pp.remove(x)
        if style:prop(pp,'w:pStyle',**{'w:val':style})
        rpr=old.find('w:r/w:rPr',NS)
        self.text(p,text,rpr,citations)
        if append:self.body.append(p)
        return p

    def bookmark_wrap(self,p,name):
        self.bookmark+=1;i=self.bookmark
        p.insert(1,node('w:bookmarkStart',**{'w:id':i,'w:name':name}))
        p.append(node('w:bookmarkEnd',**{'w:id':i}))

    def heading(self,text,level=1,front=False,newpage=False):
        p=self.p(text,style=f'u{level}',base=9 if front else 690, citations=False)
        pp=p.find('w:pPr',NS)
        if level>1:
            for x in list(pp):
                if E.QName(x).localname=='jc':pp.remove(x)
        prop(pp,'w:keepNext')
        if newpage:prop(pp,'w:pageBreakBefore')
        if front:
            np=node('w:numPr');np.append(node('w:ilvl',**{'w:val':0}));np.append(node('w:numId',**{'w:val':0}));pp.append(np)
            num=''
        else:
            if level==1:
                self.chapter+=1;self.heading_counts=[self.chapter,0,0]
            elif level==2:self.heading_counts[1]+=1;self.heading_counts[2]=0
            else:self.heading_counts[2]+=1
            num='.'.join(map(str,self.heading_counts[:level]))
        name='Heading_'+str(len(self.headings)+1);self.bookmark_wrap(p,name)
        self.headings.append(dict(text=text,level=level,number=num,bookmark=name))
        return p

    def field(self,parent,instruction,cached=''):
        f=node('w:fldSimple',**{'w:instr':' '+instruction+' '})
        f.append(self.run(cached));parent.append(f)

    def toc(self,instruction):
        p=self.p('',base=14)
        pp=p.find('w:pPr',NS);prop(pp,'w:ind',**{'w:firstLine':0})
        for typ in ['begin','separate','end']:
            r=node('w:r');r.append(node('w:fldChar',**{'w:fldCharType':typ}));p.append(r)
            if typ=='begin':
                rr=node('w:r');it=node('w:instrText',' '+instruction+' ');it.set('{http://www.w3.org/XML/1998/namespace}space','preserve');rr.append(it);p.append(rr)

    def cover(self):
        changes={
            'THỰC TẬP NGHỀ NGHIỆP 1':'BÁO CÁO ĐỒ ÁN CUỐI KỲ',
            'POS BÁN HÀNG TÍCH HỢP QUẢN LÝ KHO HÀNG VÀ CẢNH BÁO TỒN KHO THẤP':'DỰ ĐOÁN KHÁCH HÀNG RỜI DỊCH VỤ VIỄN THÔNG BẰNG HỌC MÁY',
            'Người hướng dẫn: ThS. NGUYỄN THANH TIẾN':'Người hướng dẫn: ',
            'Người thực hiện: MAI TRẦN THIỆN TÂM':'Nhóm thực hiện: ',
            'Lớp: CT07PM':'Lớp: ',
            'Khóa: 2023 – 2027':'Khóa: ',
        }
        for e in self.original[:9]:
            e=deepcopy(e)
            for p in e.xpath('.//w:txbxContent/w:p',namespaces=NS):
                ts=p.xpath('.//w:t',namespaces=NS);s=''.join(x.text or '' for x in ts)
                if s in changes:
                    ts[0].text=changes[s]
                    for x in ts[1:]:x.text=''
            for e2 in e.xpath('.//w:bookmarkStart|.//w:bookmarkEnd',namespaces=NS):e2.getparent().remove(e2)
            self.body.append(e)

    def front(self):
        self.heading('LỜI CẢM ƠN',front=True)
        self.p('Trong quá trình học tập và thực hiện đồ án môn Trí tuệ nhân tạo, nhóm đã có cơ hội vận dụng kiến thức về dữ liệu, thuật toán và đánh giá mô hình vào một bài toán cụ thể. Nhóm xin gửi lời cảm ơn đến quý thầy cô Trường Đại học Hùng Vương Thành phố Hồ Chí Minh đã truyền đạt kiến thức và tạo điều kiện học tập trong suốt thời gian qua.')
        self.p('Nhóm xin chân thành cảm ơn giảng viên phụ trách học phần đã hướng dẫn các nội dung chuyên môn và yêu cầu thực hiện đồ án. Những kiến thức về cách xác định bài toán, chuẩn bị dữ liệu và kiểm chứng kết quả là cơ sở để nhóm xây dựng báo cáo về dự đoán khách hàng rời dịch vụ viễn thông.')
        self.p('Báo cáo tập trung trình bày quy trình thực hiện, các kết quả đạt được và những giới hạn còn tồn tại. Do kinh nghiệm và phạm vi dữ liệu còn hạn chế, nhóm mong nhận được ý kiến góp ý của quý thầy cô để tiếp tục hoàn thiện kiến thức và phương pháp thực hiện.')
        self.p('Nhóm xin chân thành cảm ơn!')
        self.heading('LỜI CAM ĐOAN',front=True,newpage=True)
        self.p('Nhóm xin cam đoan các số liệu thực nghiệm được trình bày trong báo cáo “Dự đoán khách hàng rời dịch vụ viễn thông bằng học máy” được lấy từ bộ dữ liệu và các kết quả lưu trong dự án. Các bảng đánh giá, biểu đồ và trường hợp dự đoán sai được đối chiếu với tệp kết quả tương ứng; không thay thế bằng số liệu giả định để trình bày thành kết quả thực nghiệm.')
        self.p('Nguồn dữ liệu và tài liệu được sử dụng để trình bày cơ sở lý thuyết được trích dẫn trong nội dung và liệt kê ở cuối báo cáo. Những nhận định về hiệu quả mô hình được giới hạn trong phạm vi dữ liệu và quy trình đánh giá đã thực hiện. Các kết quả này không được trình bày như bằng chứng về hiệu quả kinh doanh hoặc khả năng dự báo sớm chưa được kiểm chứng.')
        p=self.p('Thành phố Hồ Chí Minh, ngày      tháng      năm 2026');prop(p.find('w:pPr',NS),'w:jc',**{'w:val':'right'})
        p=self.p('Nhóm thực hiện');prop(p.find('w:pPr',NS),'w:jc',**{'w:val':'right'})
        self.heading('MỤC LỤC',front=True,newpage=True);self.toc(r'TOC \o "1-3" \h \z \u')
        self.heading('DANH MỤC CÁC HÌNH VẼ',front=True,newpage=True);self.toc(r'TOC \h \z \c "Hình"')
        self.heading('DANH MỤC CÁC BẢNG',front=True,newpage=True);self.toc(r'TOC \h \z \c "Bảng"')
        self.heading('DANH MỤC CÁC KÝ HIỆU VÀ TỪ VIẾT TẮT',front=True,newpage=True)
        glossary=[('AP','Average Precision – Độ đo tổng hợp precision theo recall'),('AUC','Area Under the Curve – Diện tích dưới đường cong'),('CSV','Comma-Separated Values – Dữ liệu phân tách bằng dấu phẩy'),('CV','Cross-validation – Kiểm định chéo'),('EDA','Exploratory Data Analysis – Phân tích khám phá dữ liệu'),('FN','False Negative – Trường hợp bỏ sót'),('FP','False Positive – Trường hợp báo động nhầm'),('IQR','Interquartile Range – Khoảng tứ phân vị'),('LR','Logistic Regression – Hồi quy logistic'),('PR','Precision–Recall – Đường precision–recall'),('RF','Random Forest – Rừng ngẫu nhiên'),('ROC','Receiver Operating Characteristic – Đường đặc trưng hoạt động của bộ phân loại'),('TN','True Negative – Dự đoán đúng lớp âm'),('TP','True Positive – Dự đoán đúng lớp dương'),('CRM','Customer Relationship Management – Quản lý quan hệ khách hàng'),('p(x), t','Điểm churn của hồ sơ x và ngưỡng phân loại')]
        self.table(dict(headers=['TT','TỪ VIẾT TẮT','GIẢI NGHĨA'],rows=[[str(i),a,b] for i,(a,b) in enumerate(glossary,1)],widths=[563,2039,6459]),glossary=True)
        p=self.p('');p.find('w:pPr',NS).append(deepcopy(self.original[92].find('w:pPr/w:sectPr',NS)))

    def caption(self,label,title):
        key=(self.chapter,label);self.count[key]+=1;idx=self.count[key]
        p=self.p('',style='Chuthich',base=159,citations=False)
        self.text(p,label+' ',citations=False);self.field(p,r'STYLEREF 1 \s',str(self.chapter));self.text(p,'.',citations=False)
        self.field(p,f'SEQ {label} \\* ARABIC \\s 1',str(idx));self.text(p,'. '+title,citations=False)
        self.bookmark_wrap(p,f'Caption_{label}_{self.chapter}_{idx}')
        record=dict(chapter=self.chapter,number=idx,title=title)
        (self.figures if label=='Hình' else self.tablelist).append(record)
        if label=='Bảng':prop(p.find('w:pPr',NS),'w:keepNext')
        return p

    def table(self,data,glossary=False):
        n=len(data['headers']);old=self.tables[0 if glossary else 17 if n==4 else 9]
        t=node('w:tbl');t.append(deepcopy(old.find('w:tblPr',NS)))
        widths=data['widths'] or [9061//n]*n
        prop(t.find('w:tblPr',NS),'w:tblW',**{'w:w':sum(widths),'w:type':'dxa'})
        grid=node('w:tblGrid')
        for w in widths:grid.append(node('w:gridCol',**{'w:w':w}))
        t.append(grid)
        source_rows=old.findall('w:tr',NS)
        for rowi,values in enumerate([data['headers']]+data['rows']):
            source=source_rows[0 if rowi==0 else 1];tr=node('w:tr');trpr=node('w:trPr');trpr.append(node('w:cantSplit'))
            if rowi==0:trpr.append(node('w:tblHeader'))
            tr.append(trpr)
            for i,value in enumerate(values):
                sc=source.findall('w:tc',NS)[min(i,len(source.findall('w:tc',NS))-1)]
                tc=node('w:tc');cp=deepcopy(sc.find('w:tcPr',NS))
                if cp is None:cp=node('w:tcPr')
                prop(cp,'w:tcW',**{'w:w':widths[i],'w:type':'dxa'});tc.append(cp)
                sp=sc.find('w:p',NS);p=node('w:p');pp=deepcopy(sp.find('w:pPr',NS))
                if pp is None:pp=node('w:pPr')
                for x in list(pp):
                    if E.QName(x).localname in ['numPr','keepNext','pageBreakBefore']:pp.remove(x)
                if rowi==0 or (len(data['rows'])<=8 and rowi<len(data['rows'])):
                    prop(pp,'w:keepNext')
                prop(pp,'w:jc',**{'w:val':'center' if rowi==0 else 'left'})
                p.append(pp)
                rp=deepcopy(sp.find('w:r/w:rPr',NS))
                if rp is None:rp=node('w:rPr')
                if rowi==0:prop(rp,'w:b')
                else:
                    for x in list(rp):
                        if E.QName(x).localname in ['b','bCs']:rp.remove(x)
                self.text(p,value,rp,citations=False);tc.append(p);tr.append(tc)
            t.append(tr)
        self.body.append(t)

    def image(self,path,title):
        data=(ROOT/path).read_bytes();im=Image.open(ROOT/path);w,h=im.size
        cx=round(15.5*360000);cy=round(cx*h/w)
        if cy>14.0*360000:cy=round(14.0*360000);cx=round(cy*w/h)
        self.relid+=1;self.drawingid+=1;rid=f'rId{self.relid}'
        ext=(ROOT/path).suffix.lower().lstrip('.');ext='jpeg' if ext=='jpg' else ext
        name=f'telco_report_{self.drawingid}.{ext}'
        self.parts['word/media/'+name]=data
        E.SubElement(self.rels,'{'+REL+'}Relationship',Id=rid,Type=NS['r']+'/image',Target='media/'+name)
        if not any(x.get('Extension')==ext for x in self.ct):E.SubElement(self.ct,'{'+CT+'}Default',Extension=ext,ContentType='image/'+ext)
        p=self.p('',citations=False);pp=p.find('w:pPr',NS)
        prop(pp,'w:jc',**{'w:val':'center'});prop(pp,'w:ind',**{'w:firstLine':'0'});prop(pp,'w:spacing',**{'w:line':'240','w:after':'0'});prop(pp,'w:keepNext')
        r=node('w:r');draw=node('w:drawing');inline=node('wp:inline',distT='0',distB='0',distL='0',distR='0')
        inline.append(node('wp:extent',cx=cx,cy=cy));inline.append(node('wp:docPr',id=self.drawingid,name=title,descr=title))
        nf=node('wp:cNvGraphicFramePr');nf.append(node('a:graphicFrameLocks',noChangeAspect='1'));inline.append(nf)
        graphic=node('a:graphic');gd=node('a:graphicData',uri=NS['pic']);pic=node('pic:pic')
        nv=node('pic:nvPicPr');nv.append(node('pic:cNvPr',id=self.drawingid,name=name));nv.append(node('pic:cNvPicPr'));pic.append(nv)
        bf=node('pic:blipFill');bf.append(node('a:blip',**{'r:embed':rid}));stretch=node('a:stretch');stretch.append(node('a:fillRect'));bf.append(stretch);pic.append(bf)
        sp=node('pic:spPr');xf=node('a:xfrm');xf.append(node('a:off',x='0',y='0'));xf.append(node('a:ext',cx=cx,cy=cy));sp.append(xf)
        geom=node('a:prstGeom',prst='rect');geom.append(node('a:avLst'));sp.append(geom);pic.append(sp)
        gd.append(pic);graphic.append(gd);inline.append(graphic);draw.append(inline);r.append(draw);p.append(r)
        self.caption('Hình',title)

    def equation(self,text):
        # Editable native Office Math, using the template's centered equation treatment.
        self.count[(self.chapter,'equation')]+=1
        p=self.p('',citations=False);pp=p.find('w:pPr',NS);prop(pp,'w:jc',**{'w:val':'center'});prop(pp,'w:ind',**{'w:firstLine':0})
        om=node('m:oMath');mr=node('m:r');mr.append(node('m:t',text));om.append(mr);p.append(om)
        self.text(p,f'   ({self.chapter}.{self.count[(self.chapter,"equation")]})',citations=False)

    def refs(self):
        for i,(author,title,url) in enumerate(self.references,1):
            p=self.p(f'[{i}] {author}, “{title}”. [Trực tuyến]. Địa chỉ: ',citations=False)
            self.bookmark_wrap(p,f'Reference_{i}')
            pp=p.find('w:pPr',NS);prop(pp,'w:ind',**{'w:left':567,'w:hanging':567});prop(pp,'w:spacing',**{'w:after':120,'w:line':360})
            self.relid+=1;rid=f'rId{self.relid}'
            E.SubElement(self.rels,'{'+REL+'}Relationship',Id=rid,Type=NS['r']+'/hyperlink',Target=url,TargetMode='External')
            display_url=re.sub(r'([/._-])',lambda m:m.group(0)+'\u200b',url)
            h=node('w:hyperlink',**{'r:id':rid,'w:history':'1'});h.append(self.run(display_url));p.append(h)
            self.text(p,'. [Truy cập ngày 10/11/2026].',citations=False)

    def build(self):
        self.cover();self.front();tables=load_tables()
        for line in self.content.splitlines():
            s=line.strip()
            if not s:continue
            if s.startswith('#'):
                hashes,title=s.split(' ',1);level=len(hashes)
                refs=title=='DANH MỤC TÀI LIỆU THAM KHẢO'
                self.heading(title,level,front=refs,newpage=level==1 and (self.chapter>0 or refs))
            elif s.startswith('@table '):
                key,title=s[7:].split('|',1);self.caption('Bảng',title);self.table(tables[key])
            elif s.startswith('@figure '):
                path,title=s[8:].split('|',1);self.image(path,title)
            elif s.startswith('@equation '):self.equation(s[10:])
            elif s=='@references':self.refs()
            else:self.p(s)
        self.body.append(deepcopy(self.original[-1]))
        self.parts['word/document.xml']=xml(self.doc)
        self.parts['word/_rels/document.xml.rels']=xml(self.rels)
        self.parts['[Content_Types].xml']=xml(self.ct)
        settings=E.fromstring(self.parts['word/settings.xml']);prop(settings,'w:updateFields',**{'w:val':'true'});self.parts['word/settings.xml']=xml(settings)
        core=E.fromstring(self.parts['docProps/core.xml'])
        for e in core:
            local=E.QName(e).localname
            if local=='title':e.text='Dự đoán khách hàng rời dịch vụ viễn thông bằng học máy'
            elif local=='subject':e.text='Báo cáo đồ án cuối kỳ môn Trí tuệ nhân tạo'
            elif local in ['creator','lastModifiedBy','keywords','description','category']:e.text=''
        self.parts['docProps/core.xml']=xml(core)
        app=E.fromstring(self.parts['docProps/app.xml'])
        for e in list(app):
            if E.QName(e).localname in ['HeadingPairs','TitlesOfParts','Company','Manager']:app.remove(e)
        self.parts['docProps/app.xml']=xml(app)
        rootrels=E.fromstring(self.parts['_rels/.rels'])
        for e in list(rootrels):
            if e.get('Type','').endswith('/metadata/thumbnail'):
                target=e.get('Target');self.parts.pop(target,None);rootrels.remove(e)
        self.parts['_rels/.rels']=xml(rootrels)
        with ZipFile(OUT,'w',ZIP_DEFLATED) as z:
            for name,data in self.parts.items():z.writestr(name,data)
        audit=dict(output=str(OUT),source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),chapters=self.chapter,
                   figures=self.figures,tables=self.tablelist,headings=self.headings,reference_order=self.citemap,
                   preserved_parts=['word/styles.xml','word/numbering.xml','word/fontTable.xml','word/theme/theme1.xml'],
                   content_words=len(self.content.split()),fields_refreshed=False,visual_qa_complete=False)
        (ROOT/'reports/evidence/report_build.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
        (ROOT/'reports/evidence/report_references.json').write_text(json.dumps([dict(number=i,author=a,title=t,url=u,accessed='2026-11-10') for i,(a,t,u) in enumerate(self.references,1)],ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps({k:audit[k] for k in ['output','chapters','content_words']},ensure_ascii=False))
        print('Figures:',len(self.figures),'Tables:',len(self.tablelist),'References:',len(self.references))

if __name__=='__main__':Report().build()
