import sys
sys.stdout.reconfigure(encoding='utf-8')
import win32com.client as win32

word = win32.Dispatch('Word.Application')
word.Visible = False

doc = word.Documents.Open(r'C:\Users\PC5\Downloads\Sanjivani\SANJIVANI_Senior_Bal_Vigyan_2026-27_Report.docx')
total_pages = doc.ComputeStatistics(2)
print(f'Total Pages in Word: {total_pages}')

# Check text at the beginning of each page
for p_num in range(1, total_pages + 1):
    rng = doc.GoTo(1, 1, p_num) # wdGoToPage, wdGoToAbsolute, p_num
    rng.Expand(4) # wdParagraph
    print(f'Page {p_num:02d} starts with: {repr(rng.Text.strip()[:60])}')

doc.Close(False)
word.Quit()
