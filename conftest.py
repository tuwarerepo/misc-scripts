import os
import tempfile


def check_temp_dir_case_sensitive():
    with tempfile.NamedTemporaryFile(prefix='TmP') as f:
        return not os.path.exists(f.name.swapcase())


TEMP_DIR_CASE_SENSITIVE = check_temp_dir_case_sensitive()
