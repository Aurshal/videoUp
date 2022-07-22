import os
from flask import request, redirect, flash
from flask import render_template, jsonify
from app import  app
from database import db,UploadedVideo
from utitlies import allowed_file
@app.route('/upload', methods=['GET'])
def get_videos():
    videos = UploadedVideo.query.all()
    return render_template('form.html', videos = videos)


@app.route('/videos', methods=['GET'])
def get_videos_api():
    videos = UploadedVideo.query.all()
    return jsonify(videos)

@app.route('/videos_by_filter', methods=['GET'])
def get_videos_by_filter():
    min_size = request.form['min_size'] 
    max_size = request.form['max_size'] 
    min_duration = request.form['min_duration'] 
    max_duration = request.form['max_duration'] 
    if max_size == '0' or max_size == '':
        max_size = 1024
    if min_size == '':
        min_size = 0
    if max_duration == '0' or max_duration == '':
        max_size = 600
    if min_duration == '':
        min_duration = 0
    min_size = float(min_size)
    min_duration = float(min_duration)
    max_size = float(max_size)
    max_duration = float(max_duration)
    videos1 = UploadedVideo.query.filter(((UploadedVideo.size >= min_size) & (UploadedVideo.size <= max_size)) | ((UploadedVideo.duration >= min_duration) & (UploadedVideo.duration <= max_duration)))
    return jsonify(videos1.all())


@app.route('/charges', methods=['GET'])
def get_charges():
    vid_type = request.form['type']
    if allowed_file(vid_type):
        return {"message":"Video type not valid. Only mp4 and mkv available"}
    duration = request.form['duration']
    size = request.form['size']
    cutoff = 500
    cutoff_time = 378
    time_upperlimit = 600
    size_upperlimit = 1024
    if int(size) < cutoff:
        if int(duration)<cutoff_time:
            return {"charge":"17.5$"}
        elif int(duration)>cutoff_time and int(duration)<=time_upperlimit:
            return {"charge":"25$"}
    elif int(size) > cutoff and int(size)<=size_upperlimit:
        if int(duration)<cutoff_time:
            return {"charge":"25$"}
        elif int(duration)>cutoff_time and int(duration)<=time_upperlimit:
            return {"charge":"32.5$"}
    return {"message":"data out of range"}


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        duration = request.form['duration']
        size = request.form['size']
        if duration == '' and size == '':
            duration = 0
            size = 0
        if (float(duration) > 600):
            flash('File duration exceeded 10 min', 'error')
            return redirect(request.url)
        if(int(size) > 1073741824):
            flash('File size exceeded 1GB', 'error')
            return redirect(request.url)
        # check if the post request has the file part
        file = request.files['video']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        filename = file.filename
        if filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file and not allowed_file(filename):
            flash("Only mp4 and mkv files supported", 'error')
            return redirect(request.url)
        print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        v= UploadedVideo.query.filter_by(name = filename, size = size, duration = duration).first()
        if v:
            flash("Video already exist", 'error')
            return redirect(request.url)
        vid = UploadedVideo(name = filename, duration = duration, size = float(size)/10**6)
        db.session.add(vid)
        db.session.commit()
        flash("Uploaded Successfully", 'success')
        return redirect(request.url)

    return render_template('form.html')