import os
import datetime
import re
import toml
import urllib.parse

from app import app


def list_all_files(content_path, is_new_file = False):
    '''Lists all files and directories within a path, with params encoded and 
    matching the path name for easy url params.
    '''
    struct = []    
    for root, dirs, files in os.walk(content_path):
        for f in files:
            file_name = root + os.path.sep + f
            params = {'q': file_name, 'isnewfile': is_new_file}
            encoded_params = urllib.parse.urlencode(params)
            struct.append({
                'file_path': f'{root + os.path.sep + f}',
                'encoded_params': encoded_params,
                'file_name': f,
                'category': root,
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
    clean_string = clean_string.replace(".", '-')
    clean_string = clean_string.replace("&", '-')
    clean_string = clean_string.replace("$", '-')
    clean_string = clean_string.replace("@", '-')
    clean_string = clean_string.replace("#", '-')
    clean_string = clean_string.replace("=", '-')
    
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
    '''parse input fields from a list of strings
    returns a dict.
    '''
    full_file = []
    key_val_number = 0
    for line in header_str:
        each_line_dict = {}
        line.strip()
        pos_of_equal = line.find('=')
        # is the line an input key value field and NOT a comment ?
        if pos_of_equal != -1 and line[0] != '#':
            # key_val = line.split('=')
            key_val_number += 1
            key = line[:pos_of_equal].strip()
            val = line[pos_of_equal + 1:].strip().strip('"')
            each_line_dict = {
                'input_field': True,
                'key': str(key_val_number) + '_' + key,
                'value': val,
                'structure': app.config['PARAMETERS'][key]
            }
            full_file.append(each_line_dict)
        # the line is a comment, or anything but an input field
        else:
            if len(line) > 1:
                each_line_dict = {
                    'input_field': False,
                    'key': None,
                    'value': line,
                }
                full_file.append(each_line_dict)

    return full_file


def get_toml_header(str_file_content):
    '''toml function'''
    header = re.search(r'\+\+\+(.*)\+\+\+', str_file_content, re.DOTALL).group(1)
    parsed_toml = toml.loads(header)
    new_toml_string = toml.dumps(parsed_toml)
    return new_toml_string


def parse_toml_string(toml_string):
    '''toml function'''
    parsed_toml = toml.loads(toml_string)
    return parsed_toml


def allowed_file(filename):
    '''Check file upload extension.'''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def get_current_time():
    '''Return a time in the format 2022-01-04T15:43:56 to plug in easily as
    creation date in Hugo.
    '''
    return datetime.datetime.utcnow().isoformat(timespec='seconds')

