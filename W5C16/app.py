import os
from flask import Flask
import json

def remove_comments(filename1,filename2):
    """Remove all comments beginning with # from filename1 and writes the result to filename2"""
    with open(filename1,'r') as f:
        lines = f.readlines()
    with open(filename2,'w') as f:
        for line in lines:
            # Keep the Shebang line
            if line[0:2] == '#!':
                f.writelines(line)
            # Also keep existing empty lines
            elif not line.strip():
                f.writelines(line)
            # But remove comments from other lines
            else:
                line = line.split('#')
                stripped_string = line[0].rstrip()
                # Write the line only if the comment was after the code.
                # Discard lines that only contain comments.
                if stripped_string:
                    f.writelines(stripped_string)
                    f.writelines('\n')

def create_app():
    app = Flask('rmon')
    file = os.environ.get('RMON_CONFIG')
#    file_path = os.path.join(os.getcwd(),file).replace('\\','/')
    remove_comments(file,'file2')
    with open('file2','r') as config:
        config_dict = json.loads(config.read())
    for key in config_dict:
        app.config[key.upper()] = config_dict[key]
#    app.config.from_json('file2')
    return app
