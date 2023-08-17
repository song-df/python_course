from flask import Flask, render_template, send_from_directory

app = Flask(__name__,template_folder='.')

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

@app.route('/')
def index():
    # Assuming you have a list of image filenames in the 'images' variable
    images = ['tiger1.jpg', 'tiger2.jpg', 'tiger3.jpg', 'tiger4.jpg', 'tiger5.jpg']  # Replace with your actual image filenames
    return render_template('index.html', images=images)


if __name__ == '__main__':
    app.run(debug=True,port=8000)
