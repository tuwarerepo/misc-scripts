from pathlib import Path

import pytest
from faker import Factory

from conftest import TEMP_DIR_CASE_SENSITIVE
from safe_delete_pyc.safe_delete_pyc import safe_delete_pyc


fake = Factory.create()


def test_multiple_subdirectories_and_files(tmpdir):
    tmp_path = Path(tmpdir)

    dir_0 = (tmp_path / 'dir_0')
    dir_0_0 = (dir_0 / 'dir_0')
    dir_1 = (tmp_path / 'dir_1')
    dir_1_1 = (dir_1 / 'dir_1')

    dir_0.mkdir()
    dir_0_0.mkdir()
    dir_1.mkdir()
    dir_1_1.mkdir()

    root_py_0 = tmp_path / 'script_0.py'
    root_pyc_0 = tmp_path / 'script_0.pyc'
    root_py_1 = tmp_path / 'script_1.py'
    root_pyc_1 = tmp_path / 'script_1.pyc'
    dir_0_py_0 = dir_0 / 'script_0.py'
    dir_0_pyc_0 = dir_0 / 'script_0.pyc'
    dir_0_py_1 = dir_0 / 'script_1.py'
    dir_0_pyc_1 = dir_0 / 'script_1.pyc'
    dir_0_0_py_0 = dir_0_0 / 'script_0.py'
    dir_0_0_pyc_0 = dir_0_0 / 'script_0.pyc'
    dir_0_0_py_1 = dir_0_0 / 'script_1.py'
    dir_0_0_pyc_1 = dir_0_0 / 'script_1.pyc'
    dir_1_py_0 = dir_1 / 'script_0.py'
    dir_1_pyc_0 = dir_1 / 'script_0.pyc'
    dir_1_py_1 = dir_1 / 'script_1.py'
    dir_1_pyc_1 = dir_1 / 'script_1.pyc'
    dir_1_1_py_0 = dir_1_1 / 'script_0.py'
    dir_1_1_pyc_0 = dir_1_1 / 'script_0.pyc'
    dir_1_1_py_1 = dir_1_1 / 'script_1.py'
    dir_1_1_pyc_1 = dir_1_1 / 'script_1.pyc'

    root_py_0.write_bytes(b'')
    root_pyc_0.write_bytes(b'')
    root_py_1.write_bytes(b'')
    root_pyc_1.write_bytes(b'')
    dir_0_py_0.write_bytes(b'')
    dir_0_pyc_0.write_bytes(b'')
    dir_0_py_1.write_bytes(b'')
    dir_0_pyc_1.write_bytes(b'')
    dir_0_0_py_0.write_bytes(b'')
    dir_0_0_pyc_0.write_bytes(b'')
    dir_0_0_py_1.write_bytes(b'')
    dir_0_0_pyc_1.write_bytes(b'')
    dir_1_py_0.write_bytes(b'')
    dir_1_pyc_0.write_bytes(b'')
    dir_1_py_1.write_bytes(b'')
    dir_1_pyc_1.write_bytes(b'')
    dir_1_1_py_0.write_bytes(b'')
    dir_1_1_pyc_0.write_bytes(b'')
    dir_1_1_py_1.write_bytes(b'')
    dir_1_1_pyc_1.write_bytes(b'')

    safe_delete_pyc(tmp_path)

    assert root_py_0.is_file()
    assert not root_pyc_0.exists()

    assert root_py_1.is_file()
    assert not root_pyc_1.exists()

    assert dir_0_py_0.is_file()
    assert not dir_0_pyc_0.exists()

    assert dir_0_py_1.is_file()
    assert not dir_0_pyc_1.exists()

    assert dir_0_0_py_0.is_file()
    assert not dir_0_0_pyc_0.exists()

    assert dir_0_0_py_1.is_file()
    assert not dir_0_0_pyc_1.exists()

    assert dir_1_py_0.is_file()
    assert not dir_1_pyc_0.exists()

    assert dir_1_py_1.is_file()
    assert not dir_1_pyc_1.exists()

    assert dir_1_1_py_0.is_file()
    assert not dir_1_1_pyc_0.exists()

    assert dir_1_1_py_1.is_file()
    assert not dir_1_1_pyc_1.exists()


def test_directory_isolation(tmpdir):
    tmp_path = Path(tmpdir)

    dir_0 = tmp_path / 'dir_0'
    dir_0.mkdir()

    root_py_0 = tmp_path / 'script_0.py'
    root_pyc_0 = tmp_path / 'script_0.pyc'
    dir_0_py_0 = dir_0 / 'script_0.py'
    dir_0_pyc_0 = dir_0 / 'script_0.pyc'

    root_py_0.write_bytes(b'')
    root_pyc_0.write_bytes(b'')
    dir_0_py_0.write_bytes(b'')
    dir_0_pyc_0.write_bytes(b'')

    safe_delete_pyc(dir_0)

    assert root_py_0.is_file()
    assert root_pyc_0.is_file()

    assert dir_0_py_0.is_file()
    assert not dir_0_pyc_0.exists()


def test_py_with_no_pyc(tmpdir):
    tmp_path = Path(tmpdir)

    root_py_0 = tmp_path / 'script_0.py'
    root_pyc_0 = tmp_path / 'script_0.pyc'

    root_py_0.write_bytes(b'')

    safe_delete_pyc(tmp_path)

    assert root_py_0.is_file()
    assert not root_pyc_0.exists()


def test_pyc_with_no_py(tmpdir):
    tmp_path = Path(tmpdir)

    root_py_0 = tmp_path / 'script_0.py'
    root_pyc_0 = tmp_path / 'script_0.pyc'

    root_pyc_0.write_bytes(b'')

    safe_delete_pyc(tmp_path)

    assert not root_py_0.exists()
    assert root_pyc_0.is_file()


@pytest.mark.skipif(
    not TEMP_DIR_CASE_SENSITIVE,
    reason="Requires a case-sensitive file system",
)
def test_case_sensitivity(tmpdir):
    tmp_path = Path(tmpdir)

    py_path_and_pyc_path_seq = [
        (tmp_path / py_name, tmp_path / pyc_name)
        for py_name, pyc_name in [
            ('foo.py', 'foo.pyc'),
            ('FOO.py', 'FOO.pyc'),
            ('foo.PY', 'foo.PYC'),
        ]]

    exist_sample = fake.random_sample(
        (False, True),
        len(py_path_and_pyc_path_seq) * 2,
    )

    py_exist_and_pyc_exist_seq = zip(
        exist_sample[::2],
        exist_sample[1::2],
    )

    for path_seq, exist_seq in zip(
            py_path_and_pyc_path_seq,
            py_exist_and_pyc_exist_seq,
    ):
        for path, exist in zip(path_seq, exist_seq):
            if exist:
                path.write_bytes(b'')

    safe_delete_pyc(tmp_path)

    for (py_path, pyc_path), (py_exist, pyc_exist) in zip(
            py_path_and_pyc_path_seq,
            py_exist_and_pyc_exist_seq,
    ):
        if py_exist is True and pyc_exist is True:
            assert py_path.exists()
            assert not pyc_path.exists()
        else:
            assert py_path.exists() == py_exist
            assert pyc_path.exists() == pyc_exist


def test_ignore_symlink_dir(tmpdir_factory):
    tmp_path_0 = Path(tmpdir_factory.mktemp('tmp_0'))
    tmp_path_1 = Path(tmpdir_factory.mktemp('tmp_1'))

    dir_0 = (tmp_path_0 / 'dir_0')
    dir_1_link = (tmp_path_0 / 'dir_1')
    dir_1_target = (tmp_path_1 / 'dir_1')

    dir_0.mkdir()
    dir_1_target.mkdir()

    dir_1_link.symlink_to(dir_1_target, target_is_directory=True)

    dir_0_py_0 = dir_0 / 'script_0.py'
    dir_0_pyc_0 = dir_0 / 'script_0.pyc'
    dir_0_py_1 = dir_0 / 'script_1.py'
    dir_0_pyc_1 = dir_0 / 'script_1.pyc'
    dir_1_py_0 = dir_1_target / 'script_0.py'
    dir_1_pyc_0 = dir_1_target / 'script_0.pyc'
    dir_1_py_1 = dir_1_target / 'script_1.py'
    dir_1_pyc_1 = dir_1_target / 'script_1.pyc'

    dir_0_py_0.write_bytes(b'')
    dir_0_pyc_0.write_bytes(b'')
    dir_0_py_1.write_bytes(b'')
    dir_0_pyc_1.write_bytes(b'')
    dir_1_py_0.write_bytes(b'')
    dir_1_pyc_0.write_bytes(b'')
    dir_1_py_1.write_bytes(b'')
    dir_1_pyc_1.write_bytes(b'')

    safe_delete_pyc(tmp_path_0)

    assert dir_0_py_0.is_file()
    assert not dir_0_pyc_0.exists()

    assert dir_0_py_1.is_file()
    assert not dir_0_pyc_1.exists()

    assert dir_1_py_0.is_file()
    assert dir_1_pyc_0.exists()

    assert dir_1_py_1.is_file()
    assert dir_1_pyc_1.exists()


def test_follow_symlink_dir(tmpdir_factory):
    tmp_path_0 = Path(tmpdir_factory.mktemp('tmp_0'))
    tmp_path_1 = Path(tmpdir_factory.mktemp('tmp_1'))

    dir_0 = (tmp_path_0 / 'dir_0')
    dir_1_link = (tmp_path_0 / 'dir_1')
    dir_1_target = (tmp_path_1 / 'dir_1')

    dir_0.mkdir()
    dir_1_target.mkdir()

    dir_1_link.symlink_to(dir_1_target, target_is_directory=True)

    dir_0_py_0 = dir_0 / 'script_0.py'
    dir_0_pyc_0 = dir_0 / 'script_0.pyc'
    dir_0_py_1 = dir_0 / 'script_1.py'
    dir_0_pyc_1 = dir_0 / 'script_1.pyc'
    dir_1_py_0 = dir_1_target / 'script_0.py'
    dir_1_pyc_0 = dir_1_target / 'script_0.pyc'
    dir_1_py_1 = dir_1_target / 'script_1.py'
    dir_1_pyc_1 = dir_1_target / 'script_1.pyc'

    dir_0_py_0.write_bytes(b'')
    dir_0_pyc_0.write_bytes(b'')
    dir_0_py_1.write_bytes(b'')
    dir_0_pyc_1.write_bytes(b'')
    dir_1_py_0.write_bytes(b'')
    dir_1_pyc_0.write_bytes(b'')
    dir_1_py_1.write_bytes(b'')
    dir_1_pyc_1.write_bytes(b'')

    safe_delete_pyc(tmp_path_0, follow_symlinks=True)

    assert dir_0_py_0.is_file()
    assert not dir_0_pyc_0.exists()

    assert dir_0_py_1.is_file()
    assert not dir_0_pyc_1.exists()

    assert dir_1_py_0.is_file()
    assert not dir_1_pyc_0.exists()

    assert dir_1_py_1.is_file()
    assert not dir_1_pyc_1.exists()


def test_recursive_symlink_dir(tmpdir_factory):
    tmp_path_0 = Path(tmpdir_factory.mktemp('tmp_0'))

    dir_0 = (tmp_path_0 / 'dir_0')
    dir_1_link = (dir_0 / 'dir_1')

    dir_0.mkdir()
    dir_1_link.symlink_to(dir_0, target_is_directory=True)

    dir_0_py_0 = dir_0 / 'script_0.py'
    dir_0_pyc_0 = dir_0 / 'script_0.pyc'
    dir_0_py_1 = dir_0 / 'script_1.py'
    dir_0_pyc_1 = dir_0 / 'script_1.pyc'

    dir_0_py_0.write_bytes(b'')
    dir_0_pyc_0.write_bytes(b'')
    dir_0_py_1.write_bytes(b'')
    dir_0_pyc_1.write_bytes(b'')

    safe_delete_pyc(tmp_path_0, follow_symlinks=True)

    assert dir_0_py_0.is_file()
    assert not dir_0_pyc_0.exists()

    assert dir_0_py_1.is_file()
    assert not dir_0_pyc_1.exists()
