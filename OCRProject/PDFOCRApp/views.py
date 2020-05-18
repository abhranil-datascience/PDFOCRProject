from django.shortcuts import render

# Create your views here.
######################################## Home Page View ######################################################
from django.views.generic import TemplateView
class IndexView(TemplateView):
    template_name = "PDFOCRApp/HomePage.html"

######################################### OCR Converted Page #################################################
from pdf2image import convert_from_path
import os
import numpy as np
import cv2
import pytesseract as pt
import re
import io
class OCRIndexView(TemplateView):
    ################### Define Constants #########################
    input_directory="./media/PDFFiles/InputFiles/"
    output_directory="./media/PDFFiles/OutputFiles/"
    input_file = input_directory+"GeorgiaCertificate.pdf"
    output_file = output_directory+"GeorgiaCertificate.txt"
    ############### Create Image Of PDF Files ##################
    pages = convert_from_path(input_file,500)
    CurrentImage=pages[0]
    Image_File = output_directory+"GeorgiaCertificate.png"
    CurrentImage.save(Image_File)
    ################## Image Preprocessing #####################
    ModifiedImage=cv2.imread(Image_File)
    ModifiedImage=cv2.cvtColor(ModifiedImage, cv2.COLOR_BGR2GRAY)
    ModifiedImage = cv2.threshold(ModifiedImage, 142, 255, cv2.THRESH_TOZERO)[1]
    cv2.imwrite(Image_File,ModifiedImage)
    ################# Run OCR to get Text ######################
    CurrentImage=cv2.imread(Image_File)
    content = pt.image_to_string(CurrentImage)
    ################ Text Preprocessing ########################
    final = [re.sub(r"[^a-zA-Z0-9./-]+", ' ', k) for k in content.split("\n")]
    content="\n".join(final)
    content = re.sub(r'\n\s*\n', '\n', content)
    ############# Write Contents To Text File ##################
    with io.open(output_file, 'w') as f:
        f.write(str(content))
    ############# Remove Unwanted Lines ########################
    LineList=[]
    with io.open(output_file,'r') as f:
        for lines in f:
            if len(lines.strip()) > 7:
                LineList.append(lines.lstrip())
    FinalContent="\n".join(LineList)
    with io.open(output_file, 'w') as f:
        f.write(str(FinalContent))
    template_name = "PDFOCRApp/OCRPage.html"
