import os
import datetime
import re
import urllib.parse

from flask import flash

from app import app


def list_all_files(content_path, is_new_file = False):
    '''Lists all files and directories within a path, with params encoded and 
    matching the path name for easy url params.
    '''
    print('content_path=' + content_path)
    hugo_backend_dir = os.getcwd()
    print('hugo_backend_dir=' + hugo_backend_dir)
    project_root_dir = os.path.abspath(hugo_backend_dir + "/../")
    print('project_root_dir=' + project_root_dir)
    struct = []
    
    for root, dirs, files in os.walk(content_path):
        for file_name in files:
            # skip '_index.en.md' & fr filenames
            if file_name[:6] == '_index' or file_name == 'default.md':
                continue
            # print(file_name)
            file_path = root + os.path.sep + file_name
            # print(file_name)
            img_path_relative_to_img_dir = re.search(r'([^/]+)/([^/]+)$', file_path, re.DOTALL).group(0)
            params = {'q': file_path, 'isnewfile': is_new_file,
                      'rel_img_path': img_path_relative_to_img_dir}
            encoded_params = urllib.parse.urlencode(params)
            # print('filepath=' + f'{root + os.path.sep + file_name}')
            struct.append({
                'file_path': file_path,  # f'{root + os.path.sep + file_name}',
                'encoded_params': encoded_params,
                'file_name': file_name,
                'category': root,
                'rel_img_path': img_path_relative_to_img_dir,
                # 'img_path_rel_to_local_symlink':
            })
    sorted_struct = sorted(struct, key=lambda d: d['file_path'].lower()) 

    return sorted_struct


def sanitize_string(original_string):
    '''transform unicode characters into ascii.
    Start with a manual transformation.
    Then automatic just to make sure nothing was forgotten. @TODO use https://pypi.org/project/Unidecode/
    '''
    clean_string = original_string.translate({
        ord("à"): "a",
        ord("è"): "e", ord("é"): "e",
        ord("ï"): "i",
        ord("ô"): "o",
        ord("ç"): "c",
        ord("ù"): "u",
    })
    
    '''strip and substitute special characters for hyphens'''
    clean_string = clean_string.strip()
    clean_string = clean_string.replace(' ', '-')
    clean_string = clean_string.replace('"', '-')
    clean_string = clean_string.replace("'", '-')
    # clean_string = clean_string.replace(".", '-') allows for file types and dots are not invalid in file names
    clean_string = clean_string.replace("&", '-')
    clean_string = clean_string.replace("$", '-')
    clean_string = clean_string.replace("@", '-')
    clean_string = clean_string.replace("#", '-')
    clean_string = clean_string.replace("=", '-')
    clean_string = clean_string.replace(":", '-')
    
    # replace all occurrences of multiple "-" like "---" by just "-"
    clean_string = re.sub(r'-+', '-', clean_string)
    
    return clean_string
  
  
def get_file_header_and_body(head_and_body_str):
    '''Get the file and split the header from the body.'''
    header_str = re.search(r'\+\+\+(.*)\+\+\+', head_and_body_str, re.DOTALL).group(1)
    header_as_list_of_strings = header_str.split('\n')
    header_dict = parse_header_content(header_as_list_of_strings)
    
    body_str = re.search(r'(^[^\+\+\+]+)|([^\+\+\+]+$)', head_and_body_str, re.DOTALL).group(0)
    
    return {
        'header': header_dict,
        'body': body_str,
    }
    

def parse_header_content(header_str):
    '''parse input fields from a list of strings.
    Determine if each line of header is an input field or anything else.
    If it is an input field, add a 1_, 2_, ... prefix to the value of 'key'.
    returns a dict.
    '''
    full_file = []
    key_val_number = 0
    field_separator = '<hr style="height: 20px; color: orange;">'
    previous_line_was_a_comment = False  # so as to not separate each line in case of multi line comments
    for line in header_str:
        current_line_dict = {}
        line.strip()
        pos_of_equal = line.find('=')
        
        # is the line an input key value field and NOT a comment ?
        if pos_of_equal != -1 and line[0] != '#':
            # key_val = line.split('=')
            key_val_number += 1
            key = line[:pos_of_equal].strip()
            val = line[pos_of_equal + 1:].strip().strip('"')
            current_line_dict = {
                'is_input_field': True,
                'key': str(key_val_number) + '_' + key,
                'value': val,
                'structure': app.config['PARAMETERS'][key]
            }
            full_file.append(current_line_dict)
            previous_line_was_a_comment = False
        
        # else, the line IS a COMMENT, or anything but an input field
        else:
            if len(line) > 1:
                # start by adding a separator if a comment
                if line[0] == '#' and previous_line_was_a_comment is False:
                    line_separator_dict = {
                        'is_input_field': False,
                        'key': 'template_display_only_raw_html',
                        'value': field_separator,
                    }
                    full_file.append(line_separator_dict)
                    previous_line_was_a_comment = True
                
                # get the field
                current_line_dict = {
                    'is_input_field': False,
                    'key': None,
                    'value': line,
                }
                full_file.append(current_line_dict)

    return full_file


def allowed_file(filename):
    '''Check file upload extension.'''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def get_current_time():
    '''Return a time in the format 2022-01-04T15:43:56 to plug in easily as
    creation date in Hugo.
    '''
    return datetime.datetime.now().isoformat(timespec='seconds')

def add_to_erazed_files_list(file_path):
    '''Add the file path of the file just erazed to keep track.'''
    try:
        erazed_files = open(app.config['LOCATION_OF_STATIC_DIR'] + app.config['LIST_OF_ERAZED_FILES'], "a")
        erazed_files.write(file_path + "\n")
    except:
        print("Error printing to erazed_file.txt: %s" % erazed_files)
        flash("Error printing to erazed_file.txt: %s" % erazed_files)
