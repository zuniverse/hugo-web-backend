from posixpath import abspath
from flask import Flask, session, render_template, flash, request, redirect, url_for
from markupsafe import escape
import os
import re
import urllib.parse
from werkzeug.utils import secure_filename, send_from_directory
import subprocess
import json

from .utils import sanitize_string, list_all_files, get_file_header_and_body, \
    allowed_file, get_current_time

from app import app  # app is declared in __init__.py
# app.secret_key = b'_9#y2L"F4Q8z\n\xec]/'
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000  # limit the maximum allowed payload to 16 megabytes
# app.config['UPLOAD_FOLDER'] = app.config['IMG_UPLOAD_FOLDER']
app.secret_key = app.config['SECRET_KEY']
app.config['MAX_CONTENT_LENGTH'] = app.config['MAX_SIZE_UPLOAD_MEGS']  # limit the maximum allowed payload to 16 megabytes
app.config['UPLOAD_FOLDER'] = app.config['IMG_UPLOAD_FOLDER']


@app.route('/')
def index():
    struct = list_all_files(app.config['CONTENT_PATH'])

    return render_template(
        'index.html', 
        utc_dt=get_current_time(),
        file_struct=struct,
    )
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/edit_file')
def edit_file():
    encoded_file_name = request.args.get('q')
    decoded_file_name = urllib.parse.unquote(encoded_file_name)

    if request.args.get('isnewfile') == 'True': 
        is_new_file = True 
    else: 
        is_new_file = False
    with open(decoded_file_name) as f:
        file_as_str = f.read()

    usable_dict = get_file_header_and_body(file_as_str)
    image_list = list_all_files(app.config['IMG_UPLOAD_FOLDER'])
    # return usable_dict  # returns json
    return render_template(
        'edit_file.html', 
        utc_dt=get_current_time(),
        file_as_dict=usable_dict,
        file_path=decoded_file_name,
        image_list=image_list,
        is_new_file=is_new_file,
    )

  
@app.route('/receiveedit', methods=['POST'])
def receive_edit():
    '''Receives and treats edits and new file creation.
    file_path is part of data as a hidden input.
    '''
    
    # Get POST data.
    data = request.form

    '''read original file again'''
    with open(data['file_path']) as f:
        file_as_str = f.read()
    usable_dict = get_file_header_and_body(file_as_str)
    
    '''start with toml header start'''
    recontructed_file = ['+++']
    
    for each_line in usable_dict['header']:
        '''check first if it's a normal line or key value field'''
        if each_line['input_field'] is False:
            recontructed_file.append(each_line['value'])
        else:
            key = each_line['key']

            '''clean the key, remove prefix "1_"... added for html uniqueness input name'''
            clean_key = re.search(r'_(.*)', key, re.DOTALL).group(1)
            
            '''get new value passed to data'''
            val = data[key]

            '''check if need quotes'''
            if each_line['structure']['is_in_quotes']:
                val = '"' + val + '"'
                
            recontructed_file.append(clean_key + ' = ' + val)
            
    '''then put header in between +++ and add body'''
    recontructed_file.append('+++')
    recontructed_file.append(data['body'])
    
    '''stringify the list and print to file'''
    final_text_file = '\n'.join(recontructed_file)

    if data['is_new_file'] == 'False':
        # update file
        with open(data['file_path'], 'w') as f:
            print(final_text_file, file=f)
        pass
    else:
        # OR create new file @TODO check dir exists, and create it if not.
        cleaned_file_name = sanitize_string(data['title_new_file'])
        # ^[^.]* match everything up to the first . 
        # \.(\w*$) match from last dot till end of str
        # /([^/]+)$ match last word of slug
        '''category is based on the fact that in Hugo archetype filename is the name of the category.'''
        category = re.search(r'/([^/]+).md$', data['file_path'], re.DOTALL).group(1)
        for each_lang in app.config['LANGUAGES_AVAILABLE']:
            with open(app.config['CONTENT_PATH'] + os.path.sep + category + os.path.sep + cleaned_file_name + '.' + each_lang + '.md', 'w') as f:
                print(final_text_file, file=f)

    '''redirect as PRG pattern'''
    return redirect(url_for('index'))


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = sanitize_string(filename)
            filename = request.form['content_type'] + os.path.sep + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file', filename=filename))
    return render_template(
        'upload.html', 
        utc_dt=get_current_time(),
        content_types=app.config['CONTENT_TYPES'],
    )


@app.route('/new')
def select_archetypes():

    struct = list_all_files(app.config['ARCHETYPES_PATH'], True)

    return render_template(
        'index.html', 
        utc_dt=get_current_time(),
        file_struct=struct,
        is_new_file=True,
    )


@app.route('/list_images')
def list_images():

    struct = list_all_files(app.config['IMG_UPLOAD_FOLDER'])

    return render_template(
        'list_images.html', 
        utc_dt=get_current_time(),
        file_struct=struct,
    )


@app.route("/uploads/<path:name>")
def download_file(name):
    '''Links to images in a different folder than static. 
    Uses send_from_directory.
    '''
    print(name)
    '''https://flask.palletsprojects.com/en/1.0.x/api/#flask.send_from_directory'''
    return send_from_directory(
        # directory=app.config['app.config['LOCATION_OF_STATIC_DIR']'], 
        directory='../',
        path=name,
        environ='', 
        # as_attachment=True
    )


@app.route('/deploy')
def send_to_prod():
    '''Launch script to git pull / push and rsync to prod.'''

    rc = subprocess.run(
        [
          app.config['ABS_PATH_DEPLOY_SCRIPT'],
          "/dev/null"
        ],
        capture_output=True,
        shell=True,
        text=True,
        encoding='utf-8',
        cwd=app.config['ABS_PATH_DEPLOY_DIR'],
    )

    # return json.dumps(rc.stdout.splitlines())

    return render_template(
        'deploy.html', 
        utc_dt=get_current_time(),
        rc=rc,
        stdout_as_list_of_lines=rc.stdout.splitlines(),  # because stdout comes out as byte str with no eol
    )
    