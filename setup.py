from distutils.core import setup

setup(
    name='pymodoro',  # How you named your package folder (MyLib)
    packages=['pymodoro'],  # Chose the same as "name"
    version='1.0',
    # Start with a small number and increase it with every change you make
    license='MIT',
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='A python pomodoro app with a GUI for Windows',
    # Give a short description about your library
    author='Lucas Camillo',  # Type in your name
    author_email='lucascamillo333@hotmail.com',  # Type in your E-Mail
    url='https://github.com/user/reponame',
    # Provide either the link to your github or to your website
    download_url='https://github.com/user/reponame/archive/v_01.tar.gz',
    # I explain this later on
    keywords=['pomodoro', 'gui', 'windows'],
    # Keywords that define your package best
    install_requires=[  # I get to this in a second
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Anyone',
        # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GPL 3.0 License',  # Again, pick a license
        'Programming Language :: Python :: 3',
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.7',
    ],
)
