# sw2swb

A tool to convert Spacewalk text-based files (.sw) to Spacewalk binary files (.swb). SWB is based on the Hierarchical Data Format (HDF5).

## Installation

**Tested with Python 3.12.2**

```
pip install git+https://github.com/turner/sw2swb.git
```

## Command Line Usage

Convert a text baserd ball & stick file to a binary format. The use of -single-point indicates the data has a single 
xyz location for a single genomic extent

```commandline
sw2swb -f ball-and-stick.sw -n ball-and-stick -single-point
```

Convert a text baserd pointcloude file to a binary format. The use of -multi-point indicates the data has multiple 
xyz location for a single genomic extent

```commandline
sw2swb -f ball-and-stick.sw -n ball-and-stick -single-point
```

## Example

```commandline
wget "https://www.dropbox.com/scl/fi/6e0mgljxd9pqo7coi5dy7/ball-and-stick.sw?rlkey=flan64vir2791z78knpotbpcb&dl=0" -O ball-and-stick.sw
pip install git+https://github.com/turner/sw2swb.git
sw2swb -f ball-and-stick.sw -n ball-and-stick -single-point
```
