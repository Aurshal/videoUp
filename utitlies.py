def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'mp4', 'mkv'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS