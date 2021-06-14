import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pymodoro-gui',
    packages=setuptools.find_packages(),
    version='1.2.3',
    license='GPL 3.0',
    description='A pomodoro app with a GUI for Windows',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Lucas Camillo',
    author_email='lucascamillo333@hotmail.com',
    url='https://github.com/Lcrs123/pymodoro-gui.git',
    keywords=['pomodoro', 'gui', 'windows', 'tkinter'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.7',
        'Operating System :: Microsoft :: Windows',
    ],
)
