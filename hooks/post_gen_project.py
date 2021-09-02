"""
CookieCutter 钩子，用于创建完项目后进行操作
"""

import os
import subprocess


class AfterProjectCreated:
    """
    AfterProjectCreated 类, 用于执行多项操作
    """

    def __init__(self):
        pass

    @staticmethod
    def git_init():
        """
        Git 初始化操作
        """
        subprocess.call(["git", "init"])
        # subprocess.call(["git", "add", ".gitignore"])
        # subprocess.call(["git", "commit", "-m", "'add .gitignore file'"])
        subprocess.call(["git", "add", "."])

    @staticmethod
    def cleanup_cookiecutter_flags():
        """替换文件内残留的 cookiecutter_flag"""
        for root, dirs, files in os.walk(''):
            for file in files:
                if file.endswith(".py"):
                    f = open(os.path.join(root, file), 'r+', encoding='utf8')
                    lines = f.readlines()
                    f.seek(0)
                    f.truncate()
                    for line in lines:
                        if line.strip().startswith('# cookiecutter_flag'):
                            continue
                        f.write(line)

    @staticmethod
    def cleanup_temporary_files():
        """清除临时文件"""
        for root, dirs, files in os.walk(''):
            for file in files:
                if file.endswith(".pyc") or len(open(os.path.join(root, file), "r", encoding="utf8").read()) == 0:
                    os.remove(os.path.join(root, file))
            if not files or root.endswith("__pycache__"):
                os.rmdir(os.path.join(root))

    @classmethod
    def run(cls):
        cls.cleanup_cookiecutter_flags()
        cls.cleanup_temporary_files()
        cls.git_init()


AfterProjectCreated.run()
