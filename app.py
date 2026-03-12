import os
import glob
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from webtoapklib import APKConverter

app = Flask(__name__)

# Folders to temporarily store uploaded images and the final APK
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/build', methods=['POST'])
def build_apk():
    try:
        # 1. Grab text inputs from the form
        app_name = request.form.get('app_name')
        app_url = request.form.get('app_url')
        splash_time = int(request.form.get('splash_time', 3))

        # 2. Grab uploaded image files
        app_logo = request.files['app_logo']
        splash_logo = request.files['splash_logo']
        splash_bg = request.files['splash_bg']

        # 3. Secure filenames and save them temporarily
        app_logo_path = os.path.join(UPLOAD_FOLDER, secure_filename(app_logo.filename))
        splash_logo_path = os.path.join(UPLOAD_FOLDER, secure_filename(splash_logo.filename))
        splash_bg_path = os.path.join(UPLOAD_FOLDER, secure_filename(splash_bg.filename))

        app_logo.save(app_logo_path)
        splash_logo.save(splash_logo_path)
        splash_bg.save(splash_bg_path)

        # 4. Initialize your library and build the APK
        converter = APKConverter()
        converter.convert(
            url=app_url,
            app_name=app_name,
            icon_path=app_logo_path,
            splash_logo_path=splash_logo_path,
            splash_bg_path=splash_bg_path,
            output_dir=OUTPUT_FOLDER,
            splash_time_sec=splash_time
        )

        # 5. Dynamically find the generated APK
        # Search for files that start with the app_name and end with .apk
        search_pattern = os.path.join(OUTPUT_FOLDER, f"{app_name}_*.apk")
        found_apks = glob.glob(search_pattern)

        # If it doesn't use the underscore format, just grab any newly generated APK
        if not found_apks:
            found_apks = glob.glob(os.path.join(OUTPUT_FOLDER, "*.apk"))

        if not found_apks:
            return "Error: The APK was not generated correctly.", 500

        # Get the most recently created APK in case there are older ones left over
        apk_path = max(found_apks, key=os.path.getctime)

        # 6. Send the file to the user for automatic download
        return send_file(apk_path, as_attachment=True)

    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    # Render provides the PORT as an environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
