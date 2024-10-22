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

```commandline
swt2sw -f ball-and-stick.swt -n ball-and-stick -single-point
```

Convert a text based pointcloud file to a binary format. The use of -multi-point indicates the data has multiple 
xyz location for a single genomic extent

```commandline
swt2sw -f pointcloud.swt -n pointcloud -multi-point
```

## Examples

### Command Line
```commandline
wget "https://www.dropbox.com/scl/fi/6e0mgljxd9pqo7coi5dy7/ball-and-stick.swt?rlkey=flan64vir2791z78knpotbpcb&st=tfbrqgc3&dl=0" -O ball-and-stick.swt
pip install git+https://github.com/jrobinso/hdf5-indexer.git
pip install git+https://github.com/turner/sw2swb.git
swt2sw -f ball-and-stick.swt -n ball-and-stick -single-point
```

### Google Colab Notebook - Convert CSV data to Spacewalk file
[Convert CSV data to Spacewalk file](https://colab.research.google.com/drive/1SNN4_b3_x1Xhqr7gkQbSyLBRflWLUdRO#scrollTo=6gVm7bkpYeF7)

