from posixpath import abspath
from flask import Flask, session, render_template, flash, request, redirect, url_for, \
    send_from_directory
# from markupsafe import escape
import os, sys
# from pathlib import Path, PurePath
import re
import urllib.parse
from werkzeug.utils import secure_filename  #, send_from_directory
import subprocess
# from subprocess import call

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
    '''
    List all files from the home page.
    '''
    list_of_files = list_all_files(app.config['CONTENT_PATH'])

    return render_template(
        'index.html', 
        utc_dt=get_current_time(),
        list_of_files=list_of_files,
        custom_title='Home - List all content',
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
        custom_title='Edit file',
    )

  
@app.route('/receiveedit', methods=['POST'])
def receive_edit():
    '''Receives and treats edits and new file creation.
    Here we put special treatment to the ontent file, line by line.
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
    
    for current_line in usable_dict['header']:
        # print(current_line)  # debug
        # First, check first if it's only a template display field
        if current_line['key'] == 'template_display_only_raw_html':
            continue
            
        # then check if it's a normal line or key value field
        elif current_line['is_input_field'] is False:
            recontructed_file.append(current_line['value'])
        
        # current_line is an input field
        else:
            key = current_line['key']

            # clean the key, remove prefix "1_"... added for html uniqueness input name
            clean_key = re.search(r'_(.*)', key, re.DOTALL).group(1)
            
            # get new value passed to data
            val = data[key]
            
            # special treatment for booleans
            if current_line['structure']['type'] == "bool":
                # put here code... NO -> d it in template
                pass

            # check if need quotes
            if current_line['structure']['is_in_quotes']:
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
        cleaned_file_name = cleaned_file_name.lower()
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
        custom_title='Upload a new image or file',
    )


@app.route('/new')
def select_archetypes():

    struct = list_all_files(app.config['ARCHETYPES_PATH'], True)

    return render_template(
        'index.html', 
        utc_dt=get_current_time(),
        list_of_files=struct,
        is_new_file=True,
        custom_title='New Page - Choose the type',
    )


@app.route('/list_images')
def list_images():

    list_of_files = list_all_files(app.config['IMG_UPLOAD_FOLDER'])

    return render_template(
        'list_images.html', 
        utc_dt=get_current_time(),
        list_of_files=list_of_files,
        custom_title='List all images',
    )


@app.route('/show_image')
def show_image():
    '''Links to images in a different folder than static. 
    Uses send_from_directory.
    '''
    
    encoded_file_path = request.args.get('q')
    decoded_file_path = urllib.parse.unquote(encoded_file_path)
    hugo_backend_dir = os.getcwd()
    absolute_image_path = hugo_backend_dir + os.path.sep + decoded_file_path
    rel_img_path = request.args.get('rel_img_path')
    
    '''https://flask.palletsprojects.com/en/1.0.x/api/#flask.send_from_directory'''
    
    # pass jusqu'a la solution
    # pass
    
    # external_img = send_from_directory(
    #     directory=app.config['app.config[LOCATION_OF_STATIC_DIR]'], 
    #     # directory='../',
    #     path=name,
    #     # environ='', 
    #     as_attachment=True
    # )
    
    # file:///home/paul/public_html/alice/alicelavBE/WEBSITE/static/img/agenda/bubbles-wide-agenda.jpg
    
    # https://stackoverflow.com/questions/26971491/how-do-i-link-to-images-not-in-static-folder-in-flask/26972238#26972238
    # MEDIA_FOLDER = os.path.join(
    #     os.path.dirname(
    #         os.path.dirname(
    #             os.path.dirname(
    #                 os.path.abspath(__file__)
    #             )
    #         )
    #     ),
    #     'data'
    # )
    
    # return send_from_directory(MEDIA_FOLDER, name, as_attachment=True)

    return render_template(
        'show_image.html', 
        utc_dt=get_current_time(),
        external_img="external_img",
        custom_title='Show 1 image',
        decoded_file_path=decoded_file_path,
        hugo_backend_dir=hugo_backend_dir,
        absolute_image_path=absolute_image_path,
        rel_img_path=rel_img_path,
        full_path_to_img=os.path.join('static/img', rel_img_path)
    )

@app.route('/deploy')
def send_to_prod():
    '''Launch script to git pull / push and rsync to prod, and display result to template.'''

    hugo_backend_dir = os.getcwd()
    project_root_dir = os.path.abspath(hugo_backend_dir + "/../")
    
    print('hugo_backend_dir=' + hugo_backend_dir)
    print('project_root_dir=' + project_root_dir)
    print('sys.executable=' + sys.executable)

    rc = subprocess.run(
        [
          app.config['ABS_PATH_DEPLOY_SCRIPT'],  # command or script to execute
          "/dev/null"  # arg1, output to stdout
        ],
        capture_output=True,  # capture_output est vrai, la sortie et l'erreur standard (stdout et stderr) sont capturées
        shell=True,
        text=True,
        # encoding='utf-8',
        encoding = "ISO-8859-1",
        cwd=project_root_dir
    )

    return render_template(
        'deploy.html',
        tpl_title='Deploy to Prod',
        utc_dt=get_current_time(),
        rc=rc,
        stdout_as_list_of_lines=rc.stdout.splitlines(),  # because stdout comes out as byte str with no eol
    )

@app.route('/import-updates')
def import_updates():
    '''Launch script to git pull / push but NOT rsync to prod. Display result to template.'''

    hugo_backend_dir = os.getcwd()
    project_root_dir = os.path.abspath(hugo_backend_dir + "/../")
    
    print('hugo_backend_dir=' + hugo_backend_dir)
    print('project_root_dir=' + project_root_dir)
    print('sys.executable=' + sys.executable)

    rc = subprocess.run(
        [
          app.config['ABS_PATH_IMPORT_UPDATES_NO_DEPLOY_SCRIPT'],  # command or script to execute
          "/dev/null"  # arg1, output to stdout
        ],
        capture_output=True,  # capture_output est vrai, la sortie et l'erreur standard (stdout et stderr) sont capturées
        shell=True,
        text=True,
        # encoding='utf-8',
        encoding = "ISO-8859-1",
        cwd=project_root_dir
    )

    return render_template(
        'deploy.html',
        tpl_title='Import Updates',
        utc_dt=get_current_time(),
        rc=rc,
        stdout_as_list_of_lines=rc.stdout.splitlines(),  # because stdout comes out as byte str with no eol
    )
