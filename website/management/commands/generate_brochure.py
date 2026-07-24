from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, Frame, Image, PageTemplate, Paragraph, PageBreak, Spacer, Table, TableStyle
from website.models import Brochure, Service, SiteSettings, Statistic

class Command(BaseCommand):
    help = "Generate the editable CMS-linked Webfix company brochure PDF."
    def handle(self,*args,**options):
        out=settings.MEDIA_ROOT/"brochures"/"the-webfix-company-profile.pdf"; out.parent.mkdir(parents=True,exist_ok=True)
        navy=HexColor("#080705"); blue=HexColor("#D4AF37"); muted=HexColor("#9aa8c4")
        def page(canvas,doc):
            canvas.saveState(); canvas.setFillColor(navy); canvas.rect(0,0,A4[0],A4[1],fill=1,stroke=0); canvas.setStrokeColor(HexColor("#17203b"));
            for x in range(0,220,22): canvas.line(x*mm,0,x*mm,A4[1])
            canvas.setFillColor(muted); canvas.setFont("Helvetica",7); canvas.drawString(18*mm,12*mm,"THE WEBFIX · COMPANY PROFILE"); canvas.drawRightString(192*mm,12*mm,str(doc.page)); canvas.restoreState()
        doc=BaseDocTemplate(str(out),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=20*mm,bottomMargin=20*mm)
        doc.addPageTemplates(PageTemplate(id="brand",frames=Frame(doc.leftMargin,doc.bottomMargin,doc.width,doc.height,id="body"),onPage=page))
        h1=ParagraphStyle("h1",fontName="Helvetica-Bold",fontSize=42,leading=43,textColor=white,spaceAfter=10*mm)
        h2=ParagraphStyle("h2",fontName="Helvetica-Bold",fontSize=26,leading=29,textColor=white,spaceAfter=7*mm)
        body=ParagraphStyle("body",fontName="Helvetica",fontSize=11,leading=18,textColor=muted,spaceAfter=5*mm)
        label=ParagraphStyle("label",fontName="Helvetica-Bold",fontSize=8,leading=10,textColor=blue,spaceAfter=8*mm)
        site=SiteSettings.objects.first(); story=[]
        logo=settings.MEDIA_ROOT/"branding"/"the-webfix-logo.jpg"
        if logo.exists(): story += [Spacer(1,12*mm),Image(str(logo),width=48*mm,height=48*mm),Spacer(1,18*mm)]
        story += [Paragraph("STRATEGY · DESIGN · TECHNOLOGY · GROWTH",label),Paragraph("We turn bold ideas into<br/>digital momentum.",h1),Paragraph(site.hero_subtitle,body),Spacer(1,18*mm),Paragraph(f"{site.email}  ·  {site.phone}",label),PageBreak()]
        story += [Paragraph("01 · THE COMPANY",label),Paragraph("One senior team.<br/>Every digital lever.",h1),Paragraph(site.about_body,body),Spacer(1,10*mm),Paragraph("Our mission",h2),Paragraph("Make world-class digital capability accessible to ambitious businesses ready to lead.",body),Paragraph("Our standard",h2),Paragraph("Clear strategy, distinctive craft, secure technology and measurable progress—without layers of agency theatre.",body),PageBreak()]
        story += [Paragraph("02 · CAPABILITIES",label),Paragraph("Built around the<br/>real business problem.",h1)]
        rows=[]
        for i,s in enumerate(Service.objects.filter(is_active=True)[:18],1): rows.append([Paragraph(f"{i:02d}",label),Paragraph(s.title,body)])
        table=Table(rows,colWidths=[18*mm,135*mm]); table.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LINEBELOW",(0,0),(-1,-1),.25,HexColor("#28324f")),("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)])); story += [table,PageBreak()]
        story += [Paragraph("03 · HOW WE WORK",label),Paragraph("Momentum,<br/>by design.",h1)]
        for title,text in [("Discover","Align on ambition, audience and the commercial problem worth solving."),("Define","Build the strategic system, experience principles and success measures."),("Design","Create the story, identity and interactions that make people care."),("Develop","Engineer a fast, resilient product with considered details throughout."),("Grow","Launch, learn and compound performance through focused iteration.")]: story += [Paragraph(title,h2),Paragraph(text,body)]
        story += [PageBreak(),Paragraph("04 · WHY THE WEBFIX",label),Paragraph("Independent thinking.<br/>Relentless execution.",h1),Paragraph("Senior by default",h2),Paragraph("The people in the room are the people doing the thinking and making.",body),Paragraph("Clarity before craft",h2),Paragraph("We find the sharpest commercial truth before a single pixel moves.",body),Paragraph("Built to perform",h2),Paragraph("Beauty earns attention. Strategy, speed and iteration turn it into growth.",body),PageBreak(),Paragraph("LET’S BUILD WHAT’S NEXT",label),Paragraph("Your next move should<br/>be impossible to ignore.",h1),Paragraph("Tell us where you want to go. We will bring clarity, creative firepower and a practical route to get there.",body),Spacer(1,20*mm),Paragraph(site.email,h2),Paragraph(f"{site.phone} · {site.secondary_phone}<br/>{site.address}<br/>{site.office_hours}",body)]
        doc.build(story)
        Brochure.objects.update_or_create(title="The Webfix Company Profile",defaults={"file":"brochures/the-webfix-company-profile.pdf","is_active":True})
        self.stdout.write(self.style.SUCCESS(f"Brochure generated: {out}"))