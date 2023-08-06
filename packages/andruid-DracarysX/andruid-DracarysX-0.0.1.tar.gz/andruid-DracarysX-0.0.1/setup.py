import setuptools

def get_readme():
    with open("README.md", "r") as readme_fd:
        readme_data = readme_fd.read()
    return readme_data

def setup():
    setuptools.setup(
        name="andruid-DracarysX",
        version="0.0.1",
        author="Shahar Sonsino",
        author_email="shahar.sonsino@gmail.com",
        description="Android analyzer",
        long_description=get_readme(),
        long_description_content_type="text/markdown",
        url="https://github.com/DracarysX/AnDruid",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: POSIX :: Linux",
        ]
    )

if __name__ == "__main__":
    setup()
