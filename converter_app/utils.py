from pdf2docx import Converter
from docx import Document
from docx.shared import Inches
import os
import tempfile
import fitz
import io
from PIL import Image
import speech_recognition as sr
from pydub import AudioSegment

# Set the path to the ffmpeg and ffprobe executables
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

def preprocess_pdf(input_pdf_path, output_pdf_path):
    """
    Preprocess the PDF by converting PNG images to JPEG and replacing them.
    Handles unsupported colorspaces and invalid image metadata.
    """
    doc = fitz.open(input_pdf_path)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)

        for img in image_list:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"].lower()

            # Skip unsupported images
            if not image_bytes or image_ext not in ["png", "jpeg", "jpg"]:
                print(f"Skipping unsupported image format: {image_ext}")
                continue  

            try:
                # Convert PNG to JPEG if needed
                if image_ext == "png":
                    image = Image.open(io.BytesIO(image_bytes))

                    # Ensure PNG is in RGB mode (fixing unsupported colorspaces)
                    if image.mode in ("P", "RGBA", "LA") or "transparency" in image.info:
                        image = image.convert("RGB")

                    img_buffer = io.BytesIO()
                    image.save(img_buffer, format="JPEG")
                    img_bytes = img_buffer.getvalue()
                    img_buffer.close()
                else:
                    img_bytes = image_bytes  # Keep original if it's already JPEG

                # Validate and extract coordinates
                try:
                    rect = fitz.Rect(float(img[2]), float(img[3]), float(img[4]), float(img[5]))
                except (ValueError, TypeError, IndexError):
                    print(f"Skipping image with invalid coordinates: {img[2:6]}")
                    continue  

                # Insert new image into the PDF
                page.insert_image(rect, stream=img_bytes, filename="converted.jpg")

            except Exception as e:
                print(f"Error processing image: {e}")
                continue  

    # Save the modified PDF
    doc.save(output_pdf_path)
    doc.close()



def pdf_to_word(input_pdf_path, output_docx_path):
    """
    Converts a PDF to a Word document using pdf2docx.
    """
    cv = Converter(input_pdf_path)
    cv.convert(output_docx_path, start=0, end=None)
    cv.close()


def audio_to_text(audio_path):
    r = sr.Recognizer()

    # record 
    # Initialize an empty string to store the recognized text
    recognized_text = ""

    # Convert audio to WAV format if needed
    audio_format = audio_path.split('.')[-1]
    if audio_format != 'wav':
        sound = AudioSegment.from_file(audio_path)
        audio_path_wav = audio_path.replace(f'.{audio_format}', '.wav')
        sound.export(audio_path_wav, format='wav')
        audio_path = audio_path_wav
        
    with sr.AudioFile(audio_path) as source:
        # Calculate the duration of the audio file
        audio_duration = source.DURATION

        # Process the audio in chunks of 60 seconds
        for i in range(0, int(audio_duration), 60):
            audio = r.record(source, duration=60, offset=i)
            try:
                text = r.recognize_google(audio)
                recognized_text += text + " "
            except sr.UnknownValueError:
                # Skip unintelligible chunks
                recognized_text += "*"

    return recognized_text.strip()

