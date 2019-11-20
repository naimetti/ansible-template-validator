import os

from ansible_template_validator import AnsibleTemplateValidator, main
import pytest
import errno


def test_run_false_command(mocked_folder_both_files):
    conf_file, new_config = mocked_folder_both_files
    result = AnsibleTemplateValidator(
        str(conf_file),
        str(new_config),
        validation_command='/bin/false'
    ).validate()
    assert result == 1


def test_file_content_replacement(mocked_folder_both_files, mocker, new_config_content, config_content):
    conf_file, new_config = mocked_folder_both_files

    def validate_config(self):
        with open(conf_file) as config:
            assert config.read() == new_config_content
        return 56

    mocker.patch.object(AnsibleTemplateValidator, 'validate_config', validate_config)
    config_validator = AnsibleTemplateValidator(
        conf_file,
        new_config,
    )
    return_code = config_validator.validate()
    with open(conf_file) as conf:
        assert conf.read() == config_content
    assert return_code == 56


def test_exception(mocked_folder_both_files, mocker, new_config_content, config_content):
    """
    Tests if original file is restored after exception
    """
    conf_file, new_config = mocked_folder_both_files

    mocker.patch.object(AnsibleTemplateValidator, 'validate_config', side_effect=ValueError)
    config_validator = AnsibleTemplateValidator(
        conf_file,
        new_config,
    )
    with pytest.raises(ValueError):
        return_code = config_validator.validate()
    with open(conf_file) as conf:
        assert conf.read() == config_content


def test_empty_folder(mocked_empty_folder):
    conf_file, new_config = mocked_empty_folder
    config_validator = AnsibleTemplateValidator(
        conf_file,
        new_config,
    )
    with pytest.raises(IOError) as e:
        config_validator.validate()
    assert e.value.errno == errno.ENOENT


def test_new_file_only(mocked_folder_new_file, mocker, new_config_content):
    conf_file, new_config = mocked_folder_new_file
    assert not os.path.exists(conf_file)

    def validate_config(self):
        with open(conf_file) as config:
            assert config.read() == new_config_content
        return 56

    mocker.patch.object(AnsibleTemplateValidator, 'validate_config', validate_config)
    config_validator = AnsibleTemplateValidator(
        conf_file,
        new_config,
        validation_command='/bin/true'
    )
    return_code = config_validator.validate()
    assert return_code == 56
    assert not os.path.exists(conf_file)


def test_no_command_specified(mocked_folder_both_files):
    conf_file, new_config = mocked_folder_both_files

    config_validator = AnsibleTemplateValidator(
        conf_file,
        new_config,
    )
    with pytest.raises(ValueError) as e:
        config_validator.validate()
    assert e.value.args[0] == 'validation_command must be specified'


def test_main(mocker, mocked_folder_both_files):
    conf_file, new_config = mocked_folder_both_files
    mocker.patch('sys.argv', ['ansible-template-validator', new_config, conf_file, '/bin/true'])
    main()
