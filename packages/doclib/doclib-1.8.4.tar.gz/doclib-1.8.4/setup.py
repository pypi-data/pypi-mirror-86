import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='doclib',
     version='1.8.4',
     scripts=['doclib/__init__.py'],
     author="DoctorNumberFour",
     author_email="miloszecket@gmail.com",
     description="A chatbot library for euphoria.io.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://gitlab.com/DoctorNumberFour/DocLib",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "Programming Language :: Python :: 3.8",
         "Programming Language :: Python :: 3.7",
         "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
         "Operating System :: Unix",
         "Operating System :: POSIX",
         "Operating System :: Microsoft"
     ],
     install_requires=['websocket-client', 'websockets', 'attrdict', 'colorama'],
     python_requires='>=3.7'
 )
