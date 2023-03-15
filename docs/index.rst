.. PyComP documentation master file, created by
   sphinx-quickstart on Mon Mar 13 19:51:19 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyComP - Python Compression Library
===================================

PyComP is a Python library for compressing and decompressing data. It provides a simple and efficient way to reduce the size of data files without losing any information.

**Features**

PyComP has a range of features that make it a powerful tool for data compression:

- **Supports multiple algorithms:** PyComP supports several compression algorithms, including Huffman, Arithmetic, Range, ABS and ANS, which can be selected based on your specific requirements.
- **Customizable compression level:** PyComP allows you to specify the compression level, which determines the balance between compression ratio and speed. Higher levels result in smaller file sizes but slower processing times.
- **Easy-to-use functions:** PyComP provides a range of convenient functions for compressing and decompressing data and files.

**Compression algorithms**

Here is a list of algorithms implemented.

- `Huffman codes <https://github.com/JEENB/PyComP/blob/version1.0/PyComP/compressors/huffman.py>`
- `rANS <https://github.com/JEENB/PyComP/blob/version1.0/PyComP/compressors/rANS.py>`
- `sANS <https://github.com/JEENB/PyComP/blob/version1.0/PyComP/compressors/sANS.py>`
- `uABS <https://github.com/JEENB/PyComP/blob/version1.0/PyComP/compressors/uABS.py>`
- `Arithmetic coder <https://github.com/JEENB/PyComP/blob/version1.0/PyComP/compressors/arithmetic.py>`
- `Symmetric Numeral <https://github.com/JEENB/PyComP/blob/version1.0/PyComP/compressors/symmetric_numeral.py>`


**Install the `PyComP` package**

   ``git clone <repo> and cd``

   ``pip install -e . #install the package in a editable mode``

.. code-block:: python
   ## Here's how you can use the library. 
   ## Each compressor comes with an encode and decode function
   import PyComP.compressors.ANS as ANS  ## imports the ANS class

   symbols = ['q','w','e','r','t','y']
   frequency = [9,8,4,7,6,1]

   compressor = ANS(symbols, frequency)
   compressor.encode(msg = ['q','q','w','w','e','e','r'])

.. toctree::
   :maxdepth: 2
   :caption: Contents:


   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
