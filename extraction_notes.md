# Extraction Notes (digital PDFs, PyMuPDF)

Date checked: 22 Oct 2026

## OPERATIONAL GUIDELINES.pdf (PM-KISAN, 10 pages)
- Overall quality: mostly clean 
- Repeated headers or page numbers: Headers and pagenumbers are not repeated
- Broken lines in sentences: Not much
- Tables: there are no tables but there is a flowchart and the contents of the flowchart is visible line by line one  after  the other

## RevisedFAQ.pdf (PM-KISAN FAQ, 9 pages)
- Overall quality: slightly messy
- Repeated headers or page numbers: Headers and page numbers are not repeated
- Broken lines in sentences: Many
eg: frequently = frequentl v
    1st = 1't
    India = Ind ia

## WorldDevelopmentKMUT.pdf (academic paper, 11 pages)
- Overall quality: Slightly messy
- Repeated headers or page numbers: page number is repeated twice in header and footer
- Broken lines in sentences: Many
- Tables and figures: No figures and tables
- References section: it is  in the same order

## G.O.16_0.pdf (scanned, Tamil, 7 pages) - OCR with Gemini
- Checked pages 1, 4 and 7 against the PDF: Tamil text matches
- All table content present, but table layout not exact
- Plan: keep tables together when chunking 

## G.O.56.pdf (scanned, English and Tamil, 14 pages) - OCR with Gemini
- Checked 3 pages against the PDF: English text correct, Tamil text complete
- 5 numbers checked (G.O. number, date, amount): all correct
- [illegible] count: 0
- Tables: all content present, layout not exact

## Limitations found
- Gemini blocked a screenshot of a widely published document (RECITATION filter)
- Free-tier quota stopped the run several times; per-page caching made it resumable
- Used Gemini for OCR instead of Mistral; Mistral can be compared later
