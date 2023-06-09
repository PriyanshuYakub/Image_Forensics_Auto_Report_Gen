# Image Forgery Detection and Auto Report Generation

This is a project for detecting image forgery using various techniques, including clone detection, error level analysis, noise analysis, and EXIF metadata extraction and documenting them automatically in a PDF format for ease of use and efficiency.


## Requirements

- Python 3.x
- OpenCV (`cv2`)
- Tkinter
- shutil
- fpdf
- progressbar
- exiftool
- matplotlib
- numpy
- scikit-image

## Usage
1. Clone the repository:
```git clone https://github.com/your-username/image-forgery-detection.git```

2. Navigate to the cloned directory:
```cd image-forgery-detection```

3. Install the required dependencies using pip:
```pip install -r requirements.txt```

4. Run the `main.py` script:
```python main.py```

5. A file dialog will appear, allowing you to select an image for forgery detection.

6. After selecting the image, the script will perform various forgery detection techniques, generate a PDF report, and save it in the export directory of the project with the selected iamge name current date as its name.

7. The generated PDF report will provide information about the image's EXIF metadata, clone detection results, error level analysis, bit-wise plane noise analysis, median noise inconsistencies, and min-max noise analysis.


## Project Structure

The project has the following structure:

- `main.py`: The main script for image forgery detection. It uses various utility modules to perform forgery detection techniques and generate a PDF report.
- `utilities\error_level_analysis\ela.py`: Module for error level analysis (ELA) technique. It resaves the image with a lower quality to highlight regions with different error levels.
- `utilities\noise_analysis\plainlevel.py`: Module for bit-wise plane noise analysis. It preprocesses the image and analyzes noise at each bit-wise plane level.
- `utilities\noise_analysis\minmax.py`: Module for min-max noise analysis. It detects inconsistencies in pixel intensities by comparing each pixel with its local neighborhood.
- `utilities\noise_analysis\median_noise.py`: Module for median noise inconsistencies analysis. It calculates the median noise by subtracting the image from its median-filtered version.
- `utilities\exif\exif.py`: Module for extracting EXIF metadata from the image.
- `utilities\clone_detect\clone_detect.py`: Module for clone detection technique. It detects regions in the image that are visually similar or cloned.

## Need for the Tool and its Uses in Image Forensics

In the digital age, image manipulation has become increasingly prevalent, leading to a rise in image forgery cases. Image forensics is the field dedicated to detecting and analyzing such forgeries, ensuring the integrity and authenticity of digital images.

The Image Forgery Detection tool aims to assist image forensics experts and researchers in the detection of image forgeries. It provides a comprehensive set of techniques to uncover different types of manipulations and analyze suspicious images.

### Key Uses of the Tool:

1. **Forgery Detection**: The tool incorporates various forgery detection techniques such as clone detection, error level analysis, noise analysis, and EXIF metadata extraction. These techniques help identify signs of tampering, including cloning, retouching, splicing, and more.

<p align="center">
  <img src="testfiles/4.jpeg" alt="Image 1" width="400" height="300">
  <img src="testfiles/4_output.jpg" alt="Image 2" width="400" height="300">
</p>

2. **Error Level Analysis (ELA)**: ELA is a powerful technique that detects regions in an image with different error levels, indicating potential manipulations. The tool performs ELA by resaving the image with a lower quality, highlighting areas of interest.

<p align="center">
  <img src="testfiles/img2.jpg" alt="Image 1" width="400" height="300">
  <img src="testfiles/img2ELA_output.jpg" alt="Image 2" width="400" height="300">
</p>

3. **Bit-wise Plane Noise Analysis**: By analyzing noise at different bit-wise planes, the tool can identify subtle alterations made to an image. This analysis helps in detecting copy-move forgeries, where parts of an image are duplicated and pasted elsewhere.

<p align="center">
  <img src="testfiles/img2_Noise_bit_plane_output.jpg" alt="Image 1" width="800" >
</p>

4. **Min-Max Noise Analysis**: The tool detects inconsistencies in pixel intensities by comparing each pixel with its local neighborhood. This technique is effective in revealing artifacts left behind by image tampering, such as splicing or retouching.

<p align="center">
  <img src="testfiles/img2_Noise_min_max_output.jpg" alt="Image 1" width="400" >
</p>

5. **Median Noise Inconsistencies**: By calculating the median noise, which is the difference between an image and its median-filtered version, the tool can detect manipulation techniques like median filtering to hide alterations.

<p align="center">
  <img src="testfiles/img2_Noise_median_output.jpg" alt="Image 1" width="400" >
</p>

6. **EXIF Metadata Extraction**: Extracting metadata embedded in the image, such as camera make, model, and timestamps, can provide valuable information about the image's origin and potential manipulations.

6. **Auto PDF report generation**: All the info collected from the techniques used above is documented in a PDF for ease of access and future use.
<p align="center">
  <img src="testfiles/report_sample.gif" alt="Gif 1" width="400">
</p>




## Future of this Project
The Image Forgery Detection tool acts as a valuable aid to image forensics experts, investigators, and researchers, facilitating the identification and analysis of image forgeries and quick documentation of the findings. It can contribute to the overall improvement of image forensics practices, ensure the trustworthiness of digital images and proper report preperation for official usecases.

Currently it is a simple script based tool where you select the image and it analyses the image to generate a report with the available features. This will be further developed to work as an opensource web application free to use for everyone, with many more features and document customization.

## Contributing
Contributions to the Image Forensics Auto Report Generator are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

### Current Contributors:
- [Priyanshu Yakub](https://github.com/PriyanshuYakub)
- [Vinayak Sai](https://github.com/vinayaksai2711)
- [Sibi Chakkaravarthy S](https://github.com/sibichakkaravarthy)

## Attribution

This project includes the following resources:

- [imageforensics](https://github.com/pakkunandy/imageforensics) by [Anh Duy Tran](https://github.com/pakkunandy)
- [sherloq](https://github.com/GuidoBartoli/sherloq) by [Guido Bartoli](https://github.com/GuidoBartoli)



# Thank you and have fun testing out the tool!!