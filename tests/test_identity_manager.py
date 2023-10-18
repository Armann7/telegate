import pytest

from identity_manager import IdentityManager


@pytest.mark.parametrize('test_data', [{'@username1': '111', '@username2': '222', 'Channel 1': '001', 'Channel 2': '002'}])
def test_identity_manager(test_data, tmp_path):
    db_file = tmp_path / 'db_test.db'
    im = IdentityManager(db_file)
    for key, value in test_data.items():
        im[key] = value
    im.save()
    im2 = IdentityManager(db_file)
    for key, value in test_data.items():
        assert key in im2 and value == im2[key]
    for key, value in im2.items():
        assert key in test_data and value == test_data[key]
