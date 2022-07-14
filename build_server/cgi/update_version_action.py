#!/usr/bin/env python3
import io

version = "0"

try:
  with open(r'versions/vec_math_version.txt', 'rt') as f:
    version = f.readline()
    version = str(int(version) + 1)
except:
  version = "0"

with open(r'versions/vec_math_version.txt', 'wt') as f:
  f.write(version)

