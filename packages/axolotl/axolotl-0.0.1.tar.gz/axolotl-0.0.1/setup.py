from setuptools import setup, find_packages
import pathlib

readme = ((pathlib.Path(__file__).parent.resolve()) / "README.md").read_text(
    encoding="utf-8"
)

setup(
    name="axolotl",
    version="0.0.1",
    description="A Minecraft launcher for power users.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/yonderbread/axolotl",
    author="yonderbread, naturecodevoid",
    packages=find_packages(),
    project_urls={
        "Bug Reports": "https://github.com/yonderbread/axolotl/issues",
        "Source": "https://github.com/yonderbread/axolotl",
    },
    license="GPL v3",
)

