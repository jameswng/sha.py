
##SHA.PY

*sha.py* computes the sha2-256/512 hashes. For servers without the binaries.
```
usage: sha.py [-h] [-5] [-b <size>] file [file ...]

return sha256 digest in hex for named files

positional arguments:
  file                  filename

optional arguments:
  -h, --help            show this help message and exit
  -5, --sha512          generate sha2-512 digest
  -b <size>, --block-size <size>
                        block size to read file, default 8192
