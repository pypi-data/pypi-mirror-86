from setuptools import setup, Extension, find_packages

with open("README.md") as f:
    long_description = f.read()

if __name__ == "__main__":
    setup(
        name="VSColab",
        version="0.1.0",
        description="VSColab - Access Google Colab GPU's and TPU's in Your VSCode",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Anusikh Panda",
        author_email="anusikh2001@gmail.com",
        packages=find_packages(),
        include_package_data=True,
        install_requires=["colab_ssh>=0.2.64"],
        platforms=["linux", "unix"],
        python_requires=">3.5.2",
    )