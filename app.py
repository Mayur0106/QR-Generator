from flask import Flask, render_template, request
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    qr_img_url = None
    qr_name = None

    if request.method == "POST":
        data = request.form.get("url", "").strip()
        qr_name = request.form.get("qr_name", "").strip()
        fg_color = request.form.get("color", "black")
        bg_color = "white"

        if data:
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color=fg_color, back_color=bg_color)

            # Convert image to base64 string for HTML
            buf = BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            qr_img_url = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")

    return render_template("index.html", qr_img_url=qr_img_url, qr_name=qr_name)

if __name__ == "__main__":
    app.run(debug=True)
