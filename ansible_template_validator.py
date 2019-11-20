import argparse
import os
import shutil
import subprocess
import shlex
import sys
from os.path import dirname, basename, join


class AnsibleTemplateValidator:

    validation_command = ''

    def __init__(self, conf_file, new_conf_file, validation_command=None):
        self.conf_file = conf_file
        self.new_conf_file = new_conf_file
        if validation_command is not None:
            self.validation_command = validation_command

    def validate(self):
        tmp_filename = "_{basename}~{pid}".format(basename=basename(self.conf_file), pid=os.getpid())
        conf_file_bak = join(dirname(self.conf_file), tmp_filename)
        config_exists = os.path.exists(self.conf_file)
        try:
            if config_exists:
                shutil.move(self.conf_file, conf_file_bak)
            shutil.copy(self.new_conf_file, self.conf_file)
            return_code = self.validate_config()
        finally:
            if config_exists:
                shutil.move(conf_file_bak, self.conf_file)
            elif os.path.exists(self.conf_file):
                os.unlink(self.conf_file)
        return return_code

    def validate_config(self):
        if not self.validation_command:
            raise ValueError('validation_command must be specified')
        return subprocess.call(shlex.split(self.validation_command))


def main():
    parser = argparse.ArgumentParser(description='Command to be used with ansible template validate')
    parser.add_argument('new_file', help='')
    parser.add_argument('original_file',)
    parser.add_argument('validation_command', )
    args = parser.parse_args()
    validator = AnsibleTemplateValidator(
        conf_file=args.original_file,
        new_conf_file=args.new_file,
        validation_command=args.validation_command,
    )
    return validator.validate()
