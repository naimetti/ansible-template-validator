import pytest


@pytest.fixture
def config_content():
    return u"CONFIG"


@pytest.fixture
def new_config_content():
    return u"NEW CONFIG"


@pytest.fixture
def mocked_folder_both_files(tmp_path, config_content, new_config_content):
    conf_file = tmp_path / "config.txt"
    conf_file.write_text(config_content)
    new_config = tmp_path / "new_config.txt"
    new_config.write_text(new_config_content)
    return str(conf_file), str(new_config)


@pytest.fixture
def mocked_empty_folder(tmp_path):
    conf_file = tmp_path / "config.txt"
    new_config = tmp_path / "new_config.txt"
    return str(conf_file), str(new_config)


@pytest.fixture
def mocked_folder_new_file(tmp_path, new_config_content):
    conf_file = tmp_path / "config.txt"
    new_config = tmp_path / "new_config.txt"
    new_config.write_text(new_config_content)
    return str(conf_file), str(new_config)
