#!/usr/bin/python

import csv
import qrcode
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import os

# Fix for newer qrcode versions
from qrcode.image.svg import SvgPathFillImage

def csv_reader(filename):
    """Read a CSV or TXT file and return a list of entries (one per line)."""
    ap_list = []
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row:
                ap_list.append(row[0])
    return ap_list

def make_qr_code_drawing(data, size):
    """Create a ReportLab drawing from QR code SVG."""
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=size,
        border=4
    )
    qr.add_data(data)
    qr_image = qr.make_image(image_factory=SvgPathFillImage)
    
    # Save temporary SVG file
    svg_file = tempfile.NamedTemporaryFile(delete=False, suffix=".svg")
    qr_image.save(svg_file)
    svg_file.flush()
    
    # Convert SVG to ReportLab drawing
    qrcode_rl = svg2rlg(svg_file.name)
    
    svg_file.close()
    os.unlink(svg_file.name)  # Remove temp file
    return qrcode_rl

def get_axis(lwidth, lheight, spacing, pagesize):
    """Generator to provide X,Y coordinates for QR placement on page."""
    pagesize_width, pagesize_height = pagesize
    lheight_total = lheight + spacing
    lwidth_total = lwidth + spacing
    height_limit = int(pagesize_height / lheight_total)
    width_limit = int(pagesize_width / lwidth_total)

    for h in range(height_limit):
        for w in range(width_limit):
            x = w * lwidth_total
            y = h * lheight_total
            yield x, y

def get_pdf(name, pagesize, font='Helvetica-Bold', font_size=14):
    """Return a new ReportLab canvas."""
    c = canvas.Canvas(name, pagesize=pagesize)
    c.setFont(font, font_size)
    return c

def generate_pdf(input_file, output_file=None):
    """Generate QR PDF from input CSV/TXT file."""
    data = csv_reader(input_file)
    if output_file is None:
        output_file = "qr_output.pdf"

    # QR label configuration
    label_width = 2.5 * inch
    label_height = 2.5 * inch
    spacing = 0.4 * inch
    pagesize = (14 * inch, 16 * inch)  # Can also use A4

    axis = get_axis(label_width, label_height, spacing, pagesize)
    pdf = get_pdf(output_file, pagesize)
    index = 0

    while index < len(data):
        try:
            x1, y1 = next(axis)
            qrcode_img = make_qr_code_drawing(data[index], 26)
            renderPDF.draw(qrcode_img, pdf, x1, y1)
            pdf.drawString(x1 + (0.4 * inch), y1 + (0.2 * inch), data[index])
        except StopIteration:
            pdf.showPage()  # Finish current page and start a new one
            axis = get_axis(label_width, label_height, spacing, pagesize)
            continue
        index += 1

    pdf.save()
    return output_file

if __name__ == '__main__':
    import sys
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "qr_output.pdf"
    generate_pdf(input_file, output_file)
    print(f"PDF generated: {output_file}")