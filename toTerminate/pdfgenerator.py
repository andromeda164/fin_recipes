# -*- coding: cp1252 -*-
from reportlab.pdfgen import *
from reportlab.lib.units import inch,cm
from reportlab.lib import colors
from reportlab.platypus import *
import dblib

class Datum:
    def __init__(self,year,month,day):
        self.year=year
        self.month=month
        self.day=day
        pass
    def __str__(self):
        return str(self.day)+'.'+str(self.month)+'.'+str(self.year)
    def SQLDate(self):
        return str(self.month)+'/'+str(self.day)+'/'+str(self.year)

def StructuredPerformance_ReportHeader(c, datum):
    c.drawInlineImage(r'S:\Trading\Condivisione\logo.gif', 17.0*cm,28.1*cm,2.7*cm,1.1*cm)
    c.drawInlineImage(r'S:\Trading Batch\app\FA\other\other\img_home_4.jpg', 1.0*cm,22.8*cm,19*cm,4.0*cm)
    textobject = c.beginText()
    textobject.setTextOrigin(1*cm, 28.5*cm) # oben links
    textobject.setFont("Helvetica-Bold", 20)
    textobject.textLines('''Structured Products''')
    # Linien oben
    c.setLineWidth(1.0)
    c.line(1.0*cm,27.95*cm,20.0*cm,27.95*cm)
    c.setLineWidth(0.5)
    c.line(1.0*cm,27.8*cm,20.0*cm,27.8*cm)
    c.setLineWidth(1.0)
    c.line(1.0*cm,27.0*cm,20.0*cm,27.0*cm)
    c.setFillColor(colors.grey)
    c.rect(1.0*cm,27.05*cm,19.0*cm,0.7*cm, stroke=0.0,fill=1.0)
    c.setFillColor(colors.gainsboro)
    c.setStrokeColor(colors.white)
    c.rect(1.0*cm,21.5*cm,19.0*cm,1.3*cm, stroke=0.0,fill=1.0)
    c.rect(1.0*cm,20.1*cm,19.0*cm,0.9*cm, stroke=0.0,fill=1.0)
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.black)
    c.drawText(textobject)

    c.setFillColor(colors.blue)
    c.setStrokeColor(colors.blue)
    c.setFont('Helvetica-Bold',10)
    line = 'Monthly Structured Products Performance as of %s.' % str(datum)
    c.drawString(1.3*cm,20.3*cm,line)
    pass

def StructuredPerformance_ReportHeader_DearInvestor(c, comment):
    # Ab 'Dear Investor'...
    textobject = c.beginText()
    textobject.setTextOrigin(1.3*cm, 19.2*cm) # oben links
    textobject.setCharSpace(0.5)
    textobject.setStrokeColor(colors.grey)
    textobject.setFillColor(colors.grey)
    textobject.setFont("Helvetica-Bold", 8)
    textobject.textLines('''Dear Investor''')
    textobject.textLines(''' ''')
    textobject.setFont("Helvetica", 8)
    intro = """
    
In this "Monthly Structured Products Performance Report" you can detect and evaluate the current performances year-to-
date (YTD) of selected Gottardo's structured products. The list is divided into a section of equity-linked and a section
of fixed income -, forex - linked products. All Alternative products are grouped into a new section as well.  

The calculation of the performance is based on the Security Back Office Date System (CIPRO) using secondary market's Bid
Prices of every Product. It provides you with a concise analysis of short and medium term past performances at a glance.
If you should require more information or would like to speak about trade ideas please do not hesitate to call your
sales contact at Gottardo or the Sales Department Tel. +41-91-808'10'70."""
    textobject.setLeading(10.0)
    textobject.textLines(intro)
    textobject.setStrokeColor(colors.grey)
    textobject.setFillColor(colors.grey)
    textobject.setFont("Helvetica-Bold", 8)
    textobject.textLines(''' ''')
    textobject.textLines(''' ''')
    textobject.textLines('''Monthly comment''')
    textobject.textLines(''' ''')
    textobject.setFont("Helvetica", 8)
    textobject.setLeading(10.0)
    textobject.textLines(comment)
    height = textobject.getY()
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.black)
    c.drawText(textobject)
    return height

def StructuredPerformance_ReportFooter(c, height):
    textobject = c.beginText()
    textobject.setTextOrigin(1.3*cm, height) # oben links
    textobject.setCharSpace(0.5)
    textobject.setStrokeColor(colors.grey)
    textobject.setFillColor(colors.grey)
    textobject.setFont("Helvetica-Bold", 10)
    textobject.textLines('''Gottardo Sales Department''')
    textobject.textLines(''' ''')
    textobject.textLines('''Disclaimer''')
    textobject.textLines(''' ''')
    textobject.setFont("Helvetica-Bold", 8)
    textobject.textLines('''Important legal Information:''')
    textobject.textLines(''' ''')
    textobject.setFont("Helvetica", 6)
    intro = '''
Some of the mentioned products are not registered in Switzerland and therefore the document can not be publicly distributed
in Switzerland. It is dedicated for information of the bank's advisors only. The distribution of this document may also be
restricted by local law or regulation in other jurisdictions than Switzerland. It is not intended for distribution to, or
for the use by any person or entity in any such jurisdiction. Selling the Products the advisors must ensure that the
specific legal requirements or information duties of the different Products or Product classes are respected. Past performance
is no guarantee of future returns.
'''
    textobject.setLeading(8.0)
    textobject.textLines(intro)
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.black)
    c.drawText(textobject)
    pass


def StructuredPerformance_tabella(c, titolo, tabella, y_start):
    # costruzione Header Tabella
    # Quadro grigio 'for internal use only'
    y = y_start
    c.setFillColor(colors.gainsboro)
    c.setStrokeColor(colors.white)
    c.rect(1.0*cm,y,19.0*cm,0.5*cm, stroke=0.0,fill=1.0)
    c.setFont("Helvetica", 8)
    c.setStrokeColor(colors.grey)
    c.setFillColor(colors.grey)
    c.drawRightString(19.5*cm, y+0.15*cm, 'for internal use only')
    c.setFillColor(colors.gainsboro)
    c.setStrokeColor(colors.white)
    c.rect(1.3*cm,y-1.3*cm,18.7*cm,0.5*cm, stroke=0.0,fill=1.0)
    c.setFont("Helvetica-Bold", 8)
    c.setStrokeColor(colors.grey)
    c.setFillColor(colors.grey)
    c.drawString(1.3*cm, y-0.6*cm, 'Performance of all %s' % titolo)
    c.drawString(1.4*cm, y-1.2*cm, 'Valor')
    c.drawString(3.4*cm, y-1.2*cm, 'Description')
    c.drawString(10.1*cm, y-1.2*cm, 'Mat.')
    c.drawString(11.7*cm, y-1.2*cm, 'Curr')
    c.drawString(13.0*cm, y-1.2*cm, 'Price')
    c.drawString(14.8*cm, y-1.2*cm, 'Yield YtD')
    c.drawString(16.5*cm, y-1.2*cm, 'Info')

    # costruzione Tabella
    odd = 0
    c.setFont("Helvetica", 8)
    colWidths = (2.1*cm,6.7*cm,1.6*cm,1.3*cm,1.8*cm,2.2*cm)
    rowWidth = 0.5*cm
    height = y-1.8*cm
    for line in tabella:
        height -= rowWidth
        if height< 2.2*cm:
            # new page
            StructuredPerformance_PageFooter(c)
            c.showPage()
            StructuredPerformance_PageHeader(c)
            height = 25.75*cm
            c.setFont("Helvetica", 8)
            c.setFillColor(colors.gainsboro)
            c.setStrokeColor(colors.white)
            c.rect(1.3*cm,26.35*cm,18.7*cm,0.5*cm, stroke=0.0,fill=1.0)
            c.setFont("Helvetica-Bold", 8)
            c.setStrokeColor(colors.grey)
            c.setFillColor(colors.grey)
            c.drawString(1.35*cm, 26.5*cm, 'Valor')
            c.drawString(3.4*cm, 26.5*cm, 'Description')
            c.drawString(10.1*cm, 26.5*cm, 'Maturity')
            c.drawString(11.7*cm, 26.5*cm, 'Curr')
            c.drawString(13.0*cm, 26.5*cm, 'Price')
            c.drawString(14.8*cm, 26.5*cm, 'Yield YtD')
            c.drawString(16.5*cm, 26.5*cm, 'Direction')
            c.setFont("Helvetica", 8)
        if odd:
            c.setFillColor(colors.ivory)
            c.setStrokeColor(colors.white)
            c.rect(1.3*cm,height-0.1*cm,18.7*cm,0.4*cm, stroke=0.0,fill=1.0)
            odd = 0
        else:
            odd = 1
        width = 1.3*cm
        for index in range(len(colWidths)):
            if index in (0,5):
                c.setFillColor(colors.blue)
            else:
                c.setFillColor(colors.grey)
            if index not in (4,5):
                c.drawString(width, height, str(line[index]))
            else:
                outstring = ('%8.2f' % float(line[index]))
                c.drawString(width, height, outstring)
            if float(line[4])==0.0:
                c.drawInlineImage(r'S:\Trading\Condivisione\expired_2.bmp', 16.5*cm,height-0.05*cm,0.3*cm,0.3*cm)
            else:
                if float(line[5])<0.0:
                    c.drawInlineImage(r'S:\Trading\Condivisione\redarrowsmall.gif', 16.5*cm,height-0.05*cm,0.3*cm,0.3*cm)
                else:
                    c.drawInlineImage(r'S:\Trading\Condivisione\greenarrowsmall.gif', 16.5*cm,height-0.05*cm,0.3*cm,0.3*cm)
            width += colWidths[index]
    return height
            
#    ts = TableStyle([('TEXTCOLOR', (0,0),(0,-1),colors.blue), \
#                     ('TEXTCOLOR', (5,0),(0,-1),colors.blue)])
#    t = Table(tabella, colWidths, rowHeights=None, style=ts)
#    t.drawOn(c,1.3*cm,9.2*cm)

def StructuredPerformance_PageHeader(c):
    c.drawInlineImage(r'S:\Trading\Condivisione\logo.gif', 17.0*cm,28.1*cm,2.7*cm,1.1*cm)
    textobject = c.beginText()
    textobject.setTextOrigin(1*cm, 28.5*cm) # oben links
    textobject.setFont("Helvetica-Bold", 20)
    textobject.textLines('''Structured Products''')
    # Linien oben
    c.setLineWidth(1.0)
    c.line(1.0*cm,27.95*cm,20.0*cm,27.95*cm)
    c.setLineWidth(0.5)
    c.line(1.0*cm,27.8*cm,20.0*cm,27.8*cm)
    c.setLineWidth(1.0)
    c.line(1.0*cm,27.0*cm,20.0*cm,27.0*cm)
    c.setFillColor(colors.grey)
    c.rect(1.0*cm,27.05*cm,19.0*cm,0.7*cm, stroke=0.0,fill=1.0)
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.black)
    c.drawText(textobject)

    pass

def StructuredPerformance_PageFooter(c):
    # costruzione Footer on page
    c.setFillColor(colors.gainsboro)
    c.setStrokeColor(colors.white)
    c.rect(1.3*cm,1.5*cm,18.7*cm,0.5*cm, stroke=0.0,fill=1.0)
    c.setFont("Helvetica-Bold", 8)
    c.setStrokeColor(colors.grey)
    c.setFillColor(colors.grey)
    c.drawString(9.0*cm, 1.7*cm, 'page %d' % c.getPageNumber())
    textobject = c.beginText()
    textobject.setTextOrigin(1.3*cm, 1.2*cm) # ganz unten
    textobject.setCharSpace(0.5)
    textobject.setStrokeColor(colors.grey)
    textobject.setFillColor(colors.grey)
    textobject.setFont("Helvetica", 6)
    footer = '''
Le informazioni qui riportate sono state ottenute da fonti ritenute valide; non è tuttavia possibile garantire per la loro completezza e correttezza.
Né gli autori né la Banca del Gottardo si assumono pertanto la responsabilità per eventuali perdite, dirette o indirette, legate a questa pubblicazione e ai suoi contenuti.
Banca del Gottardo, Viale S. Franscini 8, CH-6901 Lugano, Tel., +41 91 808 11 70, Fax +41 91 808 33 02, www.gottardo.com
'''
    textobject.setLeading(8.0)
    textobject.textLines(footer)
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.black)
    c.drawText(textobject)
    pass


DATSTZ = Datum(2006,0o2,28)
conn = dblib.Connection('SDBDEVLU006102',db='SFA')
cu = conn.cursor       #create the cursor
filename = 'Structured Products Performance as of %s.pdf' % str(DATSTZ)
c = canvas.Canvas(filename)

comment = '''
Risks to more and earlier ECB hikes have increased in the last few weeks. We expect to see more volatility
on the EU market.
We remain modestly bearish on the EMU front end. UK money market at bottom of range and starting to price
rate hikes. We are cautious of the risk of higher yields due to global rate hike fever.
Still positive on our commodity product and our BRIC bond.  Negative on Steapener and CMS. Range accrual bonds
should still be stable in the future.


The 2006 started very well for the issuance of new equity structured products. Main drivers can be  categorized
as following: 1) friendly market 2) new "platforms" launched to increased collaboration inside the bank
(GP/Research/Front/Eq. Structured Products).

On the new issue side we can count: the Yield Units on Gold BUGS, the 90% Protected Unit on Nikkei 225, the
100% Plus Certificate on SMI and some new Baskets (US Staple, Daxplus Export Strategy and DJ Eurostoxx 50 Tot Return).
We would like to stress the success of our last initiative on the nuclear power theme (Basket > USD 11 Mio and a Cap.
Protected product will be issued shortly), the result of a joint effort of Front, GP, Research and IEFS.
'''

# Report Header
StructuredPerformance_ReportHeader(c, DATSTZ)
height = StructuredPerformance_ReportHeader_DearInvestor(c, comment)

# Fixed Income-, Forex-linked Products
sqlstring = "SELECT NUMVAL, TXTBRV, CONVERT(nvarchar(30),DATSCA,4) AS DATSCA, CODDIV_PPL, CRSULT_DVP, Rendimento*100 FROM SFA.dbo.tblPerformanceStorica WHERE DATSTZ = '%s' AND Emittente in ('IGDS','IGFE') ORDER BY Rendimento DESC;" % DATSTZ.SQLDate()
lst = cu.execute(sqlstring)
tabella = cu.fetchall()
print('Executing production of %s with %d records' % (filename, cu.rowcount))
height = StructuredPerformance_tabella(c, 'Fixed Income-, Forex-linked Products',tabella,height-0.5*cm)
height -= 1.0*cm
if height< 5.0*cm:
    # new page
    StructuredPerformance_PageFooter(c)
    c.showPage()
    StructuredPerformance_PageHeader(c)
    height = 26.25*cm

# Alternative Products
sqlstring = "SELECT NUMVAL, TXTBRV, CONVERT(nvarchar(30),DATSCA,4) AS DATSCA, CODDIV_PPL, CRSULT_DVP, Rendimento*100 FROM SFA.dbo.tblPerformanceStorica WHERE DATSTZ = '%s' AND Emittente in ('INDC') ORDER BY Rendimento DESC;" % DATSTZ.SQLDate()
lst = cu.execute(sqlstring)
tabella = cu.fetchall()
print('Executing production of %s with %d records' % (filename, cu.rowcount))
height = StructuredPerformance_tabella(c, 'Alternative Products',tabella,height)
height -= 1.0*cm
if height< 5.0*cm:
    # new page
    StructuredPerformance_PageFooter(c)
    c.showPage()
    StructuredPerformance_PageHeader(c)
    height = 26.25*cm

# Equity-linked Products
sqlstring = "SELECT NUMVAL, TXTBRV, CONVERT(nvarchar(30),DATSCA,4) AS DATSCA, CODDIV_PPL, CRSULT_DVP, Rendimento*100 FROM SFA.dbo.tblPerformanceStorica WHERE DATSTZ = '%s' AND Emittente in ('IETR','IEQU') ORDER BY Rendimento DESC;" % DATSTZ.SQLDate()
lst = cu.execute(sqlstring)
tabella = cu.fetchall()
print('Executing production of %s with %d records' % (filename, cu.rowcount))
height = StructuredPerformance_tabella(c, 'Equity-linked Products',tabella,height)
height -= 1.0*cm
if height< 5.0*cm:
    # new page
    StructuredPerformance_PageFooter(c)
    c.showPage()
    StructuredPerformance_PageHeader(c)
    height = 26.25*cm

# Report footer
StructuredPerformance_ReportFooter(c, height)
c.showPage()
c.save()
conn.close()
