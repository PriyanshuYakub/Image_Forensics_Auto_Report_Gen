import datetime
from posixpath import splitext
import cv2 as cv
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from shutil import copy
from fpdf import FPDF
import progressbar
from utilities.exif.exif import ExifTool
from utilities.clone_detect.clone import CloneDetector
from utilities.error_level_analysis.ela import ela
from utilities.noise_analysis.plane_level import PlanesAnalysis
from utilities.noise_analysis.min_max import minmax_noise_analysis
from utilities.noise_analysis.signal_separation import analyze_signal_noise
from utilities.noise_analysis.median_noise import median_noise_inconsistencies

import os
from os.path import basename

def initiaste_paths():
    current_path = os.environ['PATH']

    #adding exiftool.exe to path
    os.environ['PATH'] = 'utilities/exif/' + os.pathsep + current_path



class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Image Forgery Detection Report", 0, 1, "C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, "Page %s" % self.page_no(), 0, 0, "C")


class ImageForgeryDetection:
    def __init__(self, image_path, image_name, current_time):
        self.image_path = image_path
        self.sec_list = []

        self.bar = progressbar.ProgressBar(maxval=20, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

        self.pdf = PDFReport()
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)

        self.pdf.cell(0, 10, f"Report of {image_name} ({current_time})", ln=True)
        self.pdf.image(self.image_path, x=10, y=50, w=180)
        self.pdf.ln(5)

    def get_exif(self):
        # print(self.image_path)
        exif = ExifTool(self.image_path)
        data = ""
        for tag, value in exif.metadata.items():
            data += f"{tag}: {value}\n"
        self.bar.update(15)
        dict = {
            "head": "EXIF Meta Data",
            "image_path": None,
            "data": data
        }
        self.document_add_info(dict)

    def get_clones(self):
        clone = CloneDetector(self.image_path)
        path = clone.detect_cloning()
        self.bar.update(15)
        dict = {
            "head": "Clone Check",
            "image_path": path,
            "data": None
        }
        self.document_add_info(dict)

    def get_bit_wise_planes_noise(self):
        tool = PlanesAnalysis(self.image_path)
        tool.preprocess()
        planes_path = tool.process()
        self.bar.update(10)
        dict = {
            "head": "Bit Wise Plane level Noise Analysis",
            "image_path": planes_path,
            "data": None
        }
        self.document_add_info(dict)

    def get_median_noise(self):
        path = median_noise_inconsistencies(self.image_path)

        self.bar.update(10)
        dict = {
            "head": "Median noise inconsistencies",
            "image_path": path,
            "data": None
        }
        self.document_add_info(dict)

    def get_min_max_noise(self):
        path = minmax_noise_analysis(self.image_path)
        self.bar.update(10)
        dict = {
            "head": "Min Max Noise Analysis",
            "image_path": path,
            "data": None
        }
        self.document_add_info(dict)

    def get_ela(self):
        path = ela(self.image_path)
        self.bar.update(15)
        dict = {
            "head": "Error Level Analysis",
            "image_path": path,
            "data": None
        }
        self.document_add_info(dict)

    def document_add_info(self, data):
        self.pdf.add_page()

        self.pdf.set_font("Arial", size=14, style="B")
        self.pdf.cell(0, 10, data["head"], ln=True)
        self.pdf.ln(5)

        if data["image_path"] is not None:
            self.pdf.image(data["image_path"], x=10, y=50, w=180)
        if data["data"] is not None:
            self.pdf.set_font("Arial", size=12)
            self.pdf.multi_cell(0, 10, data["data"])
        self.bar.update(5)

    def export_document(self):
        self.pdf.output(self.image_path.split('.')[0] + '_report.pdf')
        self.bar.finish()


if __name__ == '__main__':
    initiaste_paths()
    img_path = askopenfilename()

    file_name_ext = os.path.basename(img_path).split('/')[-1]
    file_name = file_name_ext.split('.')[0]

    # move image to current export folder
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    move_path = os.path.abspath("exports")
    move_path += f"/{file_name}_{current_time.split('_')[0]}"
    isExist = os.path.exists(move_path)
    if not isExist:
        os.makedirs(move_path)
    move_path += "/" + file_name_ext
    # print(move_path)
    copy(img_path, move_path)

    tool = ImageForgeryDetection(move_path, file_name, current_time)

    
    tool.get_clones()
    tool.get_ela()

    tool.get_bit_wise_planes_noise()
    tool.get_median_noise()
    tool.get_min_max_noise()
    tool.get_exif()
    tool.export_document()
