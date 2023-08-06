from distutils.core import setup

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='trtopicter',
    packages=['trtopicter'],
    include_package_data=True,
    version='0.0.2',
    license='MIT',
    description='Turkish topic detector using machine learning',
    # long_description_content_type='text/markdown',
    # long_description=long_description,
    author='Apdullah YAYIK',
    author_email='apdullahyayik@gmail.com',
    url='https://github.com/apdullahyayik/Tr-topicter',
    download_url='https://github.com/apdullahyayik/Tr-topicter/archive/v0.0.3.tar.gz',
    keywords=['Turkish domain detector', 'text classification', 'topic classification'],
    install_requires=['fasttext'],
    python_requires='>=3.4'
)
