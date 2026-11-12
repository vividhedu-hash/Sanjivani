import pypdfium2 as pdfium

pdf = pdfium.PdfDocument('SANJIVANI_Senior_Bal_Vigyan_2026-27.pdf')
print("Total pages:", len(pdf))
for i in range(len(pdf)):
    text = pdf[i].get_textpage().get_text_range()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    content_lines = [l for l in lines if not ('SANJIVANI' in l and 'Cold-Chain' in l) and not ('G. D. Goenka Public School' in l and 'Gopal Kumar Roy' in l) and not l.startswith('Page ')]
    first_few = ' | '.join(content_lines[:3]) if content_lines else 'EMPTY'
    clean = first_few[:120].encode('ascii', errors='replace').decode('ascii')
    print(f"P{i+1:02d}: {clean}")
