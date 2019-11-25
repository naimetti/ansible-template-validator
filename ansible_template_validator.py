import argparse
import os
import shutil
import subprocess
import shlex
from os.path import dirname, basename, join

__version__ = '0.1.4'

DESCRIPTION = 'Command to be used as helper with ansible template validate. ' \
              'Replaces original_file with new_file, and then run validation_command. After this,' \
              ' returns validation_command return code and original_file is restored.' \
              'If a symlink is specified, in case it doesn\'t exists, it is created pointing' \
              ' to original_file and then is deleted.'


class AnsibleTemplateValidator:

    validation_command = ''

    def __init__(self, conf_file, new_conf_file, validation_command=None, create_sym_link=None):
        self.conf_file = os.path.abspath(conf_file)
        self.new_conf_file = os.path.abspath(new_conf_file)
        if validation_command is not None:
            self.validation_command = validation_command
        self.sym_link = create_sym_link

    def validate(self):
        tmp_filename = "_{basename}~{pid}".format(basename=basename(self.conf_file), pid=os.getpid())
        conf_file_bak = join(dirname(self.conf_file), tmp_filename)
        config_exists = os.path.exists(self.conf_file)
        create_sym_link = self.sym_link and not os.path.exists(self.sym_link)
        try:
            if config_exists:
                shutil.move(self.conf_file, conf_file_bak)
            shutil.copy(self.new_conf_file, self.conf_file)
            if create_sym_link:
                sym_link_dirname = os.path.dirname(self.sym_link)
                if not os.path.exists(sym_link_dirname):
                    os.makedirs(sym_link_dirname)
                os.symlink(self.conf_file, self.sym_link)
            return self.validate_config()
        finally:
            if config_exists:
                shutil.move(conf_file_bak, self.conf_file)
            elif os.path.exists(self.conf_file):
                os.unlink(self.conf_file)
            if create_sym_link and os.path.exists(self.sym_link):
                os.unlink(self.sym_link)

    def validate_config(self):
        if not self.validation_command:
            raise ValueError('validation_command must be specified')
        return subprocess.call(shlex.split(self.validation_command))


def main():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION
    )
    parser.add_argument('new_file', help='File used to replace original_file')
    parser.add_argument('original_file', help='Original file that is going to be validated')
    parser.add_argument('validation_command', help='Command to be executed to validate the config files')
    parser.add_argument('-l', '--create-sym-link',
                        dest='symlink',
                        help='Creates an ephemeral symbolic link pointing to original_file, just in case it '
                             'doesn\'t exists.')
    args = parser.parse_args()
    validator = AnsibleTemplateValidator(
        conf_file=args.original_file,
        new_conf_file=args.new_file,
        validation_command=args.validation_command,
    )
    return validator.validate()
