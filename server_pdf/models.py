from django.db import models
import pymupdf
from io import BytesIO
from django.core.files.base import ContentFile
import os
# Create your models here.

def optimize_pdf(pdf_file, target_mb=1):

    try:
        if pdf_file.size / (1024 * 1024) <= target_mb:
          print("PDF is already within the size limit. No optimization needed.")
          return None
        
        print("Pdf is larger than 1MB, Starting optimization...")

        pdf_file.seek(0)  # Reset file pointer to the beginning
        pdf_stream = pdf_file.read()
        doc = pymupdf.open(stream=pdf_stream, filetype="pdf")
        
        buffer = BytesIO()
        doc.save(buffer, garbage=4, deflate=True)
        doc.close()

        print(f"PDF optimization complete. New size: {len(buffer.getvalue()) / (1024*1024):.2f}MB")
        return ContentFile(buffer.getvalue(), name=pdf_file.name)
    
    except Exception as e:
        print(f"Error optimizing PDF: {e}")
        return None

class PDFDocument(models.Model):
  title = models.CharField(max_length=255, null=True, blank=True)
  pdf_file = models.FileField(upload_to='pdfs/')
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.pdf_file.name
  
  def save(self, *args, **kwargs):
    old_instance = None
    if self.pk:
      try:
        old_instance = PDFDocument.objects.get(pk=self.pk)
      except PDFDocument.DoesNotExist:
        pass # This is a new instance

    # Determine if the file has actually changed
    file_changed = True
    if old_instance and old_instance.pdf_file == self.pdf_file:
      file_changed = False

        # Only process if there is a new or changed file
    if self.pdf_file and file_changed:
      try:
                # Read the file content into memory ONCE
        self.pdf_file.seek(0)
        original_content = self.pdf_file.read()
        original_size_mb = len(original_content) / (1024 * 1024)
        
        if original_size_mb > 3:
          print(f"PDF is over 3MB ({original_size_mb:.2f}MB). Starting optimization...")
          doc = pymupdf.open(stream=original_content, filetype="pdf")
          buffer = BytesIO()
          doc.save(buffer, garbage=4, deflate=True)
          doc.close()
          
          new_content = buffer.getvalue()
          print(f"PDF optimization complete. New size: {len(new_content) / (1024*1024):.2f}MB")
          
          self.pdf_file = ContentFile(new_content, name=self.pdf_file.name)
        else:
          print("PDF is already under the size limit. No optimization needed.")
          self.pdf_file = ContentFile(original_content, name=self.pdf_file.name)

      except Exception as e:
        print(f"An error occurred during PDF processing: {e}")
        self.pdf_file = ContentFile(original_content, name=self.pdf_file.name)
    
    if not self.title:
      # Set title based on the file name if not provided
      self.title = self.pdf_file.name.split('/')[-1].split('.')[0] if not self.title else self.title

    super().save(*args, **kwargs)

    if old_instance and file_changed and old_instance.pdf_file:
       if old_instance.pdf_file.path != self.pdf_file.path:
          if os.path.isfile(old_instance.pdf_file.path):
            old_instance.pdf_file.delete(save=False)
