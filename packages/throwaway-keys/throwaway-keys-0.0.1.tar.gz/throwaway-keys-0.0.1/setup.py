# Modules
import setuptools

# Read from README
with open("README.md", "r") as f:
    description = f.read()

# Begin setup
setuptools.setup(
    name = "throwaway-keys",
    version = "0.0.1",
    author = "iiPython",
    author_email = "ben@iipython.cf",
    description = "Package to generate 'throwaway' keys for encrypting information",
    long_description = description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/ii-Python/throwaway-keys",
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3.8"
)
