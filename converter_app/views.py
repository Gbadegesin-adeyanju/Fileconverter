# from datetime import timedelta
from django.shortcuts import render
from django.http import HttpResponse
import os
import tempfile
from PIL import Image
import pytesseract
from .utils import pdf_to_word, preprocess_pdf, audio_to_text
from django.conf import settings
import re
from .forms import EmailUsersForm
from django.core.mail import send_mail
from rest_framework.decorators import api_view



# Create your views here.

def index(request):
    if request.method == 'POST' and 'pdf' in request.FILES:
        pdf_file = request.FILES['pdf']

        # Create temporary paths
        temp_dir = tempfile.gettempdir()
        temp_pdf_path = os.path.join(temp_dir, pdf_file.name)
        preprocessed_pdf_path = temp_pdf_path.replace('.pdf', '_processed.pdf')
        docx_path = temp_pdf_path.replace('.pdf', '.docx')

        # Save uploaded PDF to temp location
        with open(temp_pdf_path, 'wb+') as temp_file:
            for chunk in pdf_file.chunks():
                temp_file.write(chunk)

        try:
            # Preprocess PDF to handle PNG images
            preprocess_pdf(temp_pdf_path, preprocessed_pdf_path)

            # Convert preprocessed PDF to DOCX
            pdf_to_word(preprocessed_pdf_path, docx_path)

            # Read converted DOCX
            with open(docx_path, 'rb') as docx_file:
                response = HttpResponse(
                    docx_file.read(),
                    content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                )
                response['Content-Disposition'] = f'attachment; filename={os.path.basename(docx_path)}'

            return response

        except Exception as e:
            errorp_message = f'Error converting PDF: {e}'
            return render(request, 'converter_app/index.html', {'errorp_message': errorp_message})

        finally:
            # Clean up temporary files
            for file_path in [temp_pdf_path, preprocessed_pdf_path, docx_path]:
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except PermissionError:
                        pass  # Ignore if file is still in use

    elif request.method == 'POST' and 'image' in request.FILES:
        image = request.FILES['image']
        
        # Ensure system temporary directory is used
        temp_dir = tempfile.gettempdir()
        temp_local_path = os.path.join(temp_dir, image.name)
        
        with open(temp_local_path, 'wb+') as temp_file:
                for chunk in image.chunks():
                    temp_file.write(chunk)
                    file_path = temp_file.name

        # pytesseract cmd
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        #process image
        with Image.open(file_path) as img:
            image_text = pytesseract.image_to_string(img)
        
        # remove file path
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # if text is empty
        if not image_text.strip():
            errori_message = 'No text found in the image or low quality image'
            return render(request, 'converter_app/index.html', {'errori_message': errori_message})
        
        # Remove unwanted characters using regular expression
        image_text = re.sub(r'[^A-Za-z0-9\s]+', '', image_text)

        return render(request, 'converter_app/index.html', {'image_text': image_text})
        
    
    elif request.method == 'POST' and 'audio' in request.FILES:
        audio = request.FILES['audio']
        
        #temperary directory
        temp_dir = tempfile.gettempdir()
        audio_path = os.path.join(temp_dir, audio.name)

        # Save audio to local temporary directory
        with open(audio_path, 'wb+') as destination:
            for chunk in audio.chunks():
                destination.write(chunk)
                audio_path = destination.name
                
                
        # Convert audio to text
        audio_text = audio_to_text(audio_path)
        
        # Clean up local audio file
        os.remove(audio_path)
        
        return render (request, 'converter_app/index.html', {'audio_text': audio_text})
        # return HttpResponse(text, content_type='text/plain')

    elif request.method == 'POST' and 'email' in request.POST:
        form  = EmailUsersForm(request.POST)

        # send email and save email once form is valid
        if form.is_valid():
            email = request.POST['email']
            subject = 'Welcome to our newsletter!'
            message = f'Hi {email}, welcome to our newsletter. You will be receiving updates on our products and services'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)
            form.save()  # Save the user to the database
            return render(request, 'converter_app/index.html', {'form': EmailUsersForm()})
        else:
            error_message = 'Invalid Email Address'
            return render(request, 'converter_app/index.html', {'error_message': error_message})

    else:
        form = EmailUsersForm()
        return render(request, 'converter_app/index.html', {'form': form})
    

    

