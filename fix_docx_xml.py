import zipfile
import re
import io

def fix_openxml(xml_content):
    # 1. Fix start and end tags
    xml_content = re.sub(r'<w:start\b([^>]*)>', r'<w:left\1>', xml_content)
    xml_content = re.sub(r'</w:start>', r'</w:left>', xml_content)
    xml_content = re.sub(r'<w:end\b([^>]*)>', r'<w:right\1>', xml_content)
    xml_content = re.sub(r'</w:end>', r'</w:right>', xml_content)
    
    # 2. Fix w:color="#..." -> w:color="..."
    xml_content = re.sub(r'w:color="#([0-9a-fA-F]{6})"', r'w:color="\1"', xml_content)
    xml_content = re.sub(r'w:fill="#([0-9a-fA-F]{6})"', r'w:fill="\1"', xml_content)
    
    # 3. Fix float w:sz="9.600000381469727" -> w:sz="10"
    def round_sz(match):
        val = float(match.group(1))
        return f'w:sz="{int(round(val))}"'
    xml_content = re.sub(r'w:sz="([0-9]+\.[0-9]+)"', round_sz, xml_content)
    
    # 4. Fix float w:w="123.456" -> w:w="123"
    def round_w(match):
        val = float(match.group(1))
        return f'w:w="{int(round(val))}"'
    xml_content = re.sub(r'w:w="([0-9]+\.[0-9]+)"', round_w, xml_content)

    # 5. Fix float w:val="123.456" -> w:val="123"
    def round_val(match):
        val = float(match.group(1))
        return f'w:val="{int(round(val))}"'
    xml_content = re.sub(r'w:val="([0-9]+\.[0-9]+)"', round_val, xml_content)
    
    return xml_content

def sanitize_docx(in_path, out_path):
    with open(in_path, 'rb') as f:
        in_bytes = f.read()
    
    in_zip = zipfile.ZipFile(io.BytesIO(in_bytes))
    out_buf = io.BytesIO()
    out_zip = zipfile.ZipFile(out_buf, 'w', zipfile.ZIP_DEFLATED)
    
    for item in in_zip.infolist():
        data = in_zip.read(item.filename)
        if item.filename.endswith('.xml'):
            text = data.decode('utf-8')
            text = fix_openxml(text)
            data = text.encode('utf-8')
        out_zip.writestr(item, data)
        
    out_zip.close()
    with open(out_path, 'wb') as f:
        f.write(out_buf.getvalue())
    print(f"Sanitized: {out_path}")

if __name__ == '__main__':
    sanitize_docx('SANJIVANI_A3_SCIENCE_FAIR_POSTER_DirectReplica.docx', 'SANJIVANI_A3_POSTER_SANITIZED.docx')
    sanitize_docx('SANJIVANI_Senior_Bal_Vigyan_2026-27_DirectReplica.docx', 'SANJIVANI_REPORT_SANITIZED.docx')
