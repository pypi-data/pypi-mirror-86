import setuptools

setuptools.setup(
    name="jwst_proposal_helper",
    version="1.2.1a0",
    author="Kornpob Bhirombhakdi",
    author_email="kbhirombhakdi@stsci.edu",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bkornpob/jwst_proposal_helper.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
        ,"License :: OSI Approved :: MIT License"
        ,"Operating System :: OS Independent"
    ],
    python_requires='>=3.'
)
