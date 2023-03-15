# PyComP - Python Compression Library
PyComP is a light-weight python library for compressing and decompressing data. It provides a simple and efficient way to reduce the size of data files without losing any information.
PyComP has a range of features that make it a powerful tool for data compression: 

- Supports multiple algorithms: PyComP supports several compression algorithms, including Huffman, Arith- metic, Range, ABS and ANS, which can be selected based on your specific requirements.
- Customizable compression level: PyComP allows you to specify the compression level, which determines the balance between compression ratio and speed. Higher levels result in smaller file sizes but slower processing times.
- Easy-to-use functions: PyComP provides a range of convenient functions for compressing and decompressing data and files.

## Compression algorithms
Here is a list of algorithms implemented.

- [Huffman codes](https://github.com/JEENB/PyComP/blob/version1.0/PyComP/compressors/huffman.py)
- [rANS](https://github.com/JEENB/PyComP/blob/version1.0/PyComP/compressors/rANS.py)
- [sANS](https://github.com/JEENB/PyComP/blob/version1.0/PyComP/compressors/sANS.py)
- [uABS](https://github.com/JEENB/PyComP/blob/version1.0/PyComP/compressors/uABS.py)
- [Arithmetic coder](https://github.com/JEENB/PyComP/blob/version1.0/PyComP/compressors/arithmetic.py)
- [Symmetric Numeral](https://github.com/JEENB/PyComP/blob/version1.0/PyComP/compressors/symmetric_numeral.py)


- Install the `PyComP` package
    ```
    git clone <repo> and cd
    pip install -e . #install the package in a editable mode
    ``` 
### Library Usage
   ```
   ## Here's how you can use the library. 
   ## Each compressor comes with an encode and decode function
   from PyComP.compressors.ANS import rANS  ## imports the ANS class

   symbols = ['q','w','e','r','t','y']
   frequency = [9,8,4,7,6,1]

   compressor = rANS(symbols, frequency)
   encoded_msg , _ = compressor.encode(msg = ['q','q','w','w','e','e','r'], start_state =0)
   print(encoded_msg)
   ```
## Contact
The best way to contact the maintainers is to file an issue with your question. 
