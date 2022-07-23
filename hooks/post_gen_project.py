import os

commit_msg = """Initial commit from https://github.com/fapi-search/fastapi-search-cookiecutter template"""
print("\n*** git init && git add . && git commit ***")
os.system(f"git init && git add . && git commit -m '{commit_msg}'")

print("\n*** poetry install ***")
os.system("poetry install")
print("\n*** git add poetry.lock && git commit -m 'Add poetry.lock' ***")
os.system("git add poetry.lock && git commit -m 'Add poetry.lock'")

use_precommit = "{{ cookiecutter.use_precommit }}".lower().startswith("y")
if use_precommit:
    print("\n*** poetry run pre-commit install ***")
    os.system("poetry run pre-commit install")
    print("\n*** poetry run pre-commit run --all-files ***")
    status = os.system("poetry run pre-commit run --all-files")
    if status:
        print("\n*** git commit -a -m 'pre-commit cleanup' ***")
        os.system("git commit -a -m 'pre-commit cleanup'")
else:
    os.unlink(".pre-commit-config.yaml")
