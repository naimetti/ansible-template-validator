# ansible-config-validator

A helper script to use with the validate option from ansible 
[template](https://docs.ansible.com/ansible/latest/modules/template_module.html) module

The module provides a command line tool to validate configuration templates in cases where the validation depends
on more than one file, and there is no clear way to sandboxing the validation process.

So, for example, if you want to validate an *NGINX* config file that contains a server block configuration you will have
to validate the entire configuration tree of *NGINX* files, therefore what this script does is to replace 
the original config file with the new one, runs the validation command, and then restores all to the previous state 
independently of the validation command result.

# Install

```shell script
pip install ansible-config-validator
```

# Usage

```bash
usage: ansible-template-validator [-h] [-l SYMLINK]
                                  new_file original_file validation_command

Command to be used as helper with ansible template validate. Replaces
original_file with new_file, and then run validation_command. After this,
returns validation_command return code and original_file is restored.If a
symlink is specified, in case it doesn't exists, it is created pointing to
original_file and then is deleted.

positional arguments:
  new_file              File used to replace original_file
  original_file         Original file that is going to be validated
  validation_command    Command to be executed to validate the config files

optional arguments:
  -h, --help            show this help message and exit
  -l SYMLINK, --create-sym-link SYMLINK
                        Creates an ephemeral symbolic link pointing to
                        original_file, just in case it doesn't exists.

```

# Example 

```yaml
- name: Update nginx {{website_config}} file
  template:
    src: "website.conf"
    dest: "{{website_config}}"
    validate: "ansible-template-validator %s {{website_config}} {{nginx_validation_command|quote}}"
  vars:
    website_config: "/etc/nginx/sites-enabled/website.conf"
    nginx_validation_command: /usr/sbin/nginx -t -q -g 'daemon on; master_process on;
```

**Note**: _The script must have been previously installed on the target node._

  

