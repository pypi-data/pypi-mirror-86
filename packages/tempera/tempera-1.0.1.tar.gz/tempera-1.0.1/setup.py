import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tempera",
    version="1.0.1",
    author="Brendan Krueger",
    author_email="atleasticanbe@gmail.com",
    description="Convert and return temperature objects in set global scale.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hyperdimensionals/tempera",
    project_urls={
        'Source': 'https://github.com/Hyperdimensionals/tempera',
        'Donate': 'https://www.paypal.com/donate?hosted_button_id=3C7CBND5MJ5RE',
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # python_requires='>=3.7',
    keywords="temperature conversion celsius fahrenheit kelvin centigrade "
             "climate control"
)
