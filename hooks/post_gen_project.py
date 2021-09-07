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
        """Git 初始化操作"""
        subprocess.call(["git", "init"])
        subprocess.call(["git", "add", "."])

    @staticmethod
    def cleanup_cookiecutter_flags():
        """替换文件内残留的 cookiecutter_flag"""
        for root, dirs, files in os.walk('{{cookiecutter.project_path}}'):
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
        for root, dirs, files in os.walk('{{cookiecutter.project_path}}'):
            for file in files:
                if file.endswith(".pyc") or len(open(os.path.join(root, file), "r", encoding="utf8").read()) == 0:
                    os.remove(os.path.join(root, file))
            if not files or root.endswith("__pycache__"):
                os.rmdir(os.path.join(root))

    @staticmethod
    def generate_environment():
        """创建 Python 虚拟环境, 目前仅支持 virtualenv—wrappers 和 virtualenv"""
        workon_home = subprocess.getoutput("echo $WORKON_HOME")
        default_workon_home = os.path.join(os.environ["HOME"], ".virtualenvs")
        now_path = "{{cookiecutter.now_path}}"
        project_path = "{{cookiecutter.project_path}}"
        env_name = "{{cookiecutter.env_name}}"
        if not workon_home:
            subprocess.call(["mkdir", default_workon_home])
            workon_home = default_workon_home
        os.chdir(workon_home)
        subprocess.call(["python3", "-m", "venv", env_name])
        os.chdir(now_path)
        env_python_path = os.path.join(os.path.join(os.path.join(default_workon_home, env_name), "bin"), "python3")
        subprocess.call([env_python_path, "-m", "pip", "install", "-r", os.path.join(project_path, "requirements.txt")])

    @classmethod
    def run(cls):
        cls.cleanup_cookiecutter_flags()
        cls.cleanup_temporary_files()
        cls.git_init()
        cls.generate_environment()


AfterProjectCreated.run()

if __name__ == '__main__':
    pass
