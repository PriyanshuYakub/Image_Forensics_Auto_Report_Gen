from flask import Flask, request, send_file
from PIL import Image
import datetime
import os
from main_pdf import start_process

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        # Check if the POST request contains a file named 'image'
        if "image" not in request.files:
            return "No image file provided"

        image_file = request.files["image"]

        # Check if the file is a valid image
        if not allowed_image_filetype(image_file.filename):
            return "Invalid image file"

        #make fle path
        file_name_ext = image_file.filename
        file_name = file_name_ext.split('.')[0]

        # move image to current export folder
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

        move_path = os.path.abspath("exports")
        move_path += f"/{file_name}_{current_time.split('_')[0]}"
        isExist = os.path.exists(move_path)
        if not isExist:
            os.makedirs(move_path)
        move_path += "/" + file_name_ext
        # Save the uploaded image to a temporary file
        image_path = "/path/to/temp/image.jpg"
        image_file.save(move_path)

        # Create a PDF document
        pdf_path = start_process(move_path,file_name,current_time)
        create_pdf(image_path, pdf_path)

        # Serve the PDF for download
        return send_file(pdf_path, as_attachment=True, attachment_filename="output.pdf")

    # Render the upload form
    return '''
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="image">
            <input type="submit" value="Upload and Generate PDF">
        </form>
    '''

def allowed_image_filetype(filename):
    allowed_extensions = {"jpg", "jpeg", "png", "gif"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions

def create_pdf(image_path, output_path):
    pdf = FPDF()
    pdf.add_page()

    # Add the image to the PDF
    pdf.image(image_path, x=10, y=10, w=100)

    # Save the PDF to the output path
    pdf.output(output_path)

if __name__ == "__main__":
    app.run(debug=True)
