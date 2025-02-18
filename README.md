# swt2sw

A tool to convert Spacewalk text-based files (.swt) to Spacewalk binary files (.sw). This format is based on the Hierarchical Data Format (HDF5).

## Installation

**Tested with Python 3.12.2**

```
pip install git+https://github.com/jrobinso/hdf5-indexer.git
```

```
pip install git+https://github.com/turner/swt2sw.git
```

## Command Line Usage

Convert a text based ball & stick file to a binary format. The use of -single-point indicates the data has a single 
xyz location for a single genomic extent

```
swt2sw -f ball-and-stick.swt -n ball-and-stick -single-point
```

Convert a text based pointcloud file to a binary format. The use of -multi-point indicates the data has multiple 
xyz location for a single genomic extent

```
swt2sw -f pointcloud.swt -n pointcloud -multi-point
```
## Documentation

Detailed file format specifications can be found here [Spacewalk Wiki](https://github.com/igvteam/spacewalk/wiki). This documentation includes:

- **Spacewalk Binary File Format (.sw):**  
  The new, efficient binary format based on HDF5. It offers enhanced performance, improved scalability, and robust support for complex, hierarchical datasets.

- **Legacy Spacewalk Text Format (.swt):**  
  The original text-based format that is now deprecated. While some legacy files are still in use, it is highly recommended to migrate to the binary format to leverage modern performance improvements and future enhancements.

For comprehensive technical details and migration guidelines, please refer to the [Spacewalk Wiki](https://github.com/igvteam/spacewalk/wiki).

## Examples

```
wget "https://www.dropbox.com/scl/fi/6e0mgljxd9pqo7coi5dy7/ball-and-stick.swt?rlkey=flan64vir2791z78knpotbpcb&st=tfbrqgc3&dl=0" -O ball-and-stick.swt
pip install git+https://github.com/jrobinso/hdf5-indexer.git
pip install git+https://github.com/turner/sw2swb.git
swt2sw -f ball-and-stick.swt -n ball-and-stick -single-point
```

### Google Colab Notebook - Convert CSV data to Spacewalk file
Included in this project is a Google Colab Notebook that is a detailed example of how to convert a simple
CSV file to Spacewalk Binary File format. Click this button to run the notebook 
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/turner/swt2sw/blob/main/docs/CSVtoSpacewalk.ipynb)


