"""
Legacy Development Remnants
No need to delete; simply retain them.
"""
import os
import sys
import shutil

APP_NAME = "project_3"  # 可以改成更像产品的名字

def resource_path(relative_path: str) -> str:
    """
    获取打包内资源路径（兼容 PyInstaller）
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_user_data_dir() -> str:
    """
    返回用户数据目录，例如：
    C:\\Users\\xxx\\AppData\\Roaming\\project_3
    """
    base = os.environ.get("APPDATA")
    data_dir = os.path.join(base, APP_NAME)
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def ensure_writable_db() -> str:
    """
    确保存在一个【可写】数据库：
    - 第一次运行：从打包资源复制 Utils/test.db
    - 之后运行：一直使用用户目录里的数据库
    """
    user_db = os.path.join(get_user_data_dir(), "test.db")

    if not os.path.exists(user_db):
        bundled_db = resource_path(os.path.join("Utils", "test.db"))
        shutil.copyfile(bundled_db, user_db)

    return user_db
