from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from .forms import MammogramExamForm
from exams.models import MammogramExam
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def eview(request):
    if request.user.is_authenticated:
     dados = MammogramExam.objects.all()
     return render(
        request,
        'list.html',
        {
            'dados':dados,
        }
     ) 
    return HttpResponse('Você precisa estar logado para acessar esta página.')
    

def ecreate(request):
 form = MammogramExamForm()
 if request.method == 'POST':
  form = MammogramExamForm(request.POST, request.FILES)
  if form.is_valid():
   exam = form.save(commit=False)
   exam.user_ip = get_client_ip(request)
   exam.save()
   return redirect('exams.eview') 
 return render(request, 'form.html', {'form': form})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def estore(request):
    if request.method == 'POST':
        form = MammogramExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.user_ip = get_client_ip(request)
            exam.save()
            return redirect('exams.view')

    return redirect('exams.ecreate')

def eedit(request, id):
   exams = get_object_or_404(MammogramExam, pk=id)
   form = MammogramExamForm(instance=exams)
   if request.method == "POST":
    form = MammogramExamForm(request.POST, request.FILES, instance=exams)
    if form.is_valid():
     form.save()
     return redirect('exams.eview')
   return render(request, 'edit.html', {'form': form, 'exams': exams})

def edelete(request, id):
    exams = get_object_or_404(MammogramExam, pk=id)
    exams.delete()
    return redirect('exams.eview')

def _wrap_text(text, font_name, font_size, max_width):
    words = (text or "").split()
    if not words:
        return [""]
    lines = []
    current = words[0]
    for word in words[1:]:
        test = f"{current} {word}"
        if pdfmetrics.stringWidth(test, font_name, font_size) <= max_width:
            current = test
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines

@login_required(login_url='/login/')
def exam_report_pdf(request, id):
    exam = get_object_or_404(MammogramExam, pk=id)
    patient = exam.patient
    institution = exam.local
    professional_name = request.user.get_full_name() or request.user.get_username()

    buffer = BytesIO()
    cnv = canvas.Canvas(buffer, pagesize=A4)
    page_w, page_h = A4

    margin = 16 * mm
    left_col_w = 30 * mm
    gap = 6 * mm
    x_left = margin
    x_content = margin + left_col_w + gap
    content_w = page_w - margin - x_content

    # Subtle page backdrop
    cnv.setFillColorRGB(0.97, 0.98, 0.99)
    cnv.rect(margin, margin, page_w - 2 * margin, page_h - 2 * margin, stroke=0, fill=1)
    cnv.setFillColorRGB(0, 0, 0)

    # Logo box
    logo_box_h = 40 * mm
    cnv.setLineWidth(0.8)
    cnv.setStrokeColorRGB(0.1, 0.15, 0.25)
    cnv.rect(x_left, page_h - margin - logo_box_h, left_col_w, logo_box_h)
    if institution and getattr(institution, "logo", None):
        try:
            cnv.drawImage(
                institution.logo.path,
                x_left + 2 * mm,
                page_h - margin - logo_box_h + 2 * mm,
                left_col_w - 4 * mm,
                logo_box_h - 4 * mm,
                preserveAspectRatio=True,
                anchor="c",
            )
        except Exception:
            cnv.setFont("Helvetica", 9)
            cnv.drawCentredString(
                x_left + left_col_w / 2,
                page_h - margin - logo_box_h / 2,
                "Logo indisponível",
            )
    else:
        cnv.setFont("Helvetica", 9)
        cnv.drawCentredString(
            x_left + left_col_w / 2,
            page_h - margin - logo_box_h / 2,
            "Sem logo",
        )

    y = page_h - margin
    cnv.setFillColorRGB(0.07, 0.1, 0.2)
    # Header - Institution + Professional
    cnv.setFont("Helvetica-Bold", 12)
    cnv.drawString(x_content, y - 2 * mm, institution.name if institution else "Instituição")
    cnv.setFont("Helvetica", 9)
    cnv.setFillColorRGB(0.25, 0.3, 0.4)
    y -= 8 * mm
    if institution and institution.endereco_fisico:
        cnv.drawString(x_content, y, str(institution.endereco_fisico))
        y -= 5 * mm
    if institution:
        cnv.drawString(x_content, y, f"{institution.email} | {institution.phone}")
        y -= 6 * mm

    cnv.setFillColorRGB(0.35, 0.4, 0.45)
    cnv.setFont("Helvetica", 9)
    cnv.drawRightString(page_w - margin, page_h - margin - 2 * mm, "Profissional")
    cnv.setFillColorRGB(0.07, 0.1, 0.2)
    cnv.setFont("Helvetica-Bold", 10)
    cnv.drawRightString(page_w - margin, page_h - margin - 8 * mm, professional_name)

    # Divider
    cnv.setStrokeColorRGB(0.07, 0.1, 0.2)
    cnv.setLineWidth(1)
    cnv.line(x_content, y - 2 * mm, page_w - margin, y - 2 * mm)
    y -= 10 * mm

    # Title
    cnv.setFillColorRGB(0.07, 0.1, 0.2)
    cnv.setFont("Helvetica-Bold", 13)
    cnv.drawCentredString(x_content + content_w / 2, y, "LAUDO DE MAMOGRAFIA DIGITAL")
    y -= 10 * mm

    # Info box
    box_h = 30 * mm
    cnv.setLineWidth(0.6)
    cnv.setStrokeColorRGB(0.86, 0.89, 0.93)
    cnv.setFillColorRGB(0.96, 0.97, 0.98)
    cnv.roundRect(x_content, y - box_h, content_w, box_h, 4 * mm, stroke=1, fill=1)
    cnv.setFont("Helvetica", 8)
    label_y = y - 4 * mm
    cnv.setFillColorRGB(0.33, 0.39, 0.5)
    cnv.drawString(x_content + 4 * mm, label_y, "PACIENTE")
    cnv.drawString(x_content + content_w / 2, label_y, "DATA DE NASCIMENTO")
    cnv.setFillColorRGB(0, 0, 0)
    cnv.setFont("Helvetica", 10)
    cnv.drawString(x_content + 4 * mm, label_y - 4 * mm, patient.full_name)
    cnv.drawString(x_content + content_w / 2, label_y - 4 * mm, patient.birth_date.strftime("%d/%m/%Y"))

    cnv.setFont("Helvetica", 8)
    cnv.setFillColorRGB(0.33, 0.39, 0.5)
    cnv.drawString(x_content + 4 * mm, label_y - 12 * mm, "DATA DO EXAME")
    cnv.drawString(x_content + content_w / 2, label_y - 12 * mm, "STATUS")
    cnv.setFillColorRGB(0, 0, 0)
    cnv.setFont("Helvetica", 10)
    cnv.drawString(x_content + 4 * mm, label_y - 16 * mm, exam.exam_date.strftime("%d/%m/%Y"))
    cnv.drawString(x_content + content_w / 2, label_y - 16 * mm, exam.itype)

    cnv.setFont("Helvetica", 8)
    cnv.setFillColorRGB(0.33, 0.39, 0.5)
    cnv.drawString(x_content + 4 * mm, label_y - 24 * mm, "IP DO USUÁRIO")
    cnv.drawString(x_content + content_w / 2, label_y - 24 * mm, "ACEITE")
    cnv.setFillColorRGB(0, 0, 0)
    cnv.setFont("Helvetica", 10)
    cnv.drawString(x_content + 4 * mm, label_y - 28 * mm, exam.user_ip or "-")
    cnv.drawString(x_content + content_w / 2, label_y - 28 * mm, "Sim" if exam.acceptance_term else "Não")

    y = y - box_h - 8 * mm

    # Description
    cnv.setFillColorRGB(0.07, 0.1, 0.2)
    cnv.setFont("Helvetica-Bold", 10)
    cnv.drawString(x_content, y, "DESCRIÇÃO")
    y -= 5 * mm
    cnv.setFillColorRGB(0, 0, 0)
    cnv.setFont("Helvetica", 10)
    for line in _wrap_text(exam.description or "-", "Helvetica", 10, content_w):
        cnv.drawString(x_content, y, line)
        y -= 4 * mm

    y -= 4 * mm
    # Result
    cnv.setFillColorRGB(0.07, 0.1, 0.2)
    cnv.setFont("Helvetica-Bold", 10)
    cnv.drawString(x_content, y, "RESULTADO")
    y -= 5 * mm
    cnv.setFillColorRGB(0, 0, 0)
    cnv.setFont("Helvetica", 10)
    cnv.drawString(x_content, y, exam.result)
    y -= 8 * mm

    # Exam image (below result)
    if exam.image:
        image_h = 55 * mm
        image_w = content_w * 0.7
        try:
            cnv.drawImage(
                exam.image.path,
                x_content,
                y - image_h,
                width=image_w,
                height=image_h,
                preserveAspectRatio=True,
                anchor="c",
            )
            y -= image_h + 6 * mm
        except Exception:
            cnv.setFont("Helvetica", 9)
            cnv.setFillColorRGB(0.45, 0.5, 0.6)
            cnv.drawString(x_content, y - 4 * mm, "Imagem do exame indisponível.")
            cnv.setFillColorRGB(0, 0, 0)
            y -= 10 * mm

    # Acceptance term
    cnv.setFillColorRGB(0.07, 0.1, 0.2)
    cnv.setFont("Helvetica-Bold", 10)
    cnv.drawString(x_content, y, "TERMO DE ACEITAÇÃO")
    y -= 5 * mm
    cnv.setFillColorRGB(0, 0, 0)
    cnv.setFont("Helvetica", 10)
    term_text = (
        "Análise realizada com apoio de Inteligência Artificial, sem substituição do "
        "julgamento médico. Resultado validado e responsabilidade assumida pelo médico responsável."
    )
    for line in _wrap_text(term_text, "Helvetica", 10, content_w):
        cnv.drawString(x_content, y, line)
        y -= 4 * mm

    # Signature line
    y -= 8 * mm
    cnv.setFont("Helvetica", 8)
    cnv.drawString(x_content, y, "Assinatura do responsável")
    y -= 10 * mm
    cnv.setLineWidth(0.8)
    cnv.line(x_content, y, x_content + content_w * 0.7, y)

    cnv.showPage()
    cnv.save()
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="laudo-{exam.id}.pdf"'
    return response
