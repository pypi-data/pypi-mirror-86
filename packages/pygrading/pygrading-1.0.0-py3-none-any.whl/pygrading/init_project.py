"""
    Name: init_project.py
    Author: Charles Zhang <694556046@qq.com>
    Propose: Initialize a pygrading project
    Coding: UTF-8
"""


import os
import pkgutil
from pygrading.utils import makedirs, writefile


def init(path=os.getcwd(), name="cg-kernel"):
    """ Initialize a pygrading project """

    print("Create project folder", end="")
    new_project_path = os.path.join(path, name)
    new_project_kernel_path = os.path.join(new_project_path, "kernel")
    makedirs(new_project_kernel_path, exist_ok=True)
    print("\rCreate project folder | success")

    print("Copy files", end="")
    data = pkgutil.get_data(__package__, 'static/.gitignore').decode()
    writefile(os.path.join(new_project_path, ".gitignore"), str(data))

    data = pkgutil.get_data(__package__, 'static/README.md').decode()
    writefile(os.path.join(new_project_path, "README.md"), str(data))

    data = pkgutil.get_data(__package__, 'static/Makefile').decode()
    writefile(os.path.join(new_project_path, "Makefile"), str(data))

    data = pkgutil.get_data(__package__, 'static/kernel/__main__.py').decode()
    writefile(os.path.join(new_project_kernel_path, "__main__.py"), str(data))

    data = pkgutil.get_data(__package__, 'static/kernel/prework.py').decode()
    writefile(os.path.join(new_project_kernel_path, "prework.py"), str(data))

    data = pkgutil.get_data(__package__, 'static/kernel/run.py').decode()
    writefile(os.path.join(new_project_kernel_path, "run.py"), str(data))

    data = pkgutil.get_data(__package__, 'static/kernel/postwork.py').decode()
    writefile(os.path.join(new_project_kernel_path, "postwork.py"), str(data))
    print("\rCopy files | success")

    print("Initialization Completed!")
