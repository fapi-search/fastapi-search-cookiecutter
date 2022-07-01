import os

commit_msg = """{{ cookiecutter.initial_git_commit_message }}"""
print("*** git init && git add . && git commit ***")
os.system(f"git init && git add . && git commit -m '{commit_msg}'")

print("*** poetry install ***")
os.system("poetry install")
print("*** git add poetry.lock && git commit -m 'Add poetry.lock' ***")
os.system("git add poetry.lock && git commit -m 'Add poetry.lock'")

use_precommit = "{{ cookiecutter.use_precommit }}".lower().startswith("y")
if use_precommit:
    print("*** pre-commit install ***")
    os.system("poetry run pre-commit install")
else:
    os.unlink(".pre-commit-config.yaml")
