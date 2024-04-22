### 1. Overview
The Spacewalk binary file format (.swb) is an extensible format for the visualization of 3D genomic data with the [Spacewalk visualization tool](https://spacewalk-site.netlify.app/).
Typical datasets include super-resolution chromatin tracing data and genomic simulation data. 

### 2. File Structure
The Spacewalk binary file format is based on HDF5 (The Hierarchical Data Format). HDF5 is a hierarchical format. Key HDF5 concepts are:
- **Groups**: The HDF5 analog to a directory of a computer file system (or folder of a graphical user interface).
- **Datasets**: The M by N array that stores a particular chunk data in the file. Dimensions of the array are chosen based on the type of data stored.
- **Attributes**: A propery of groups and datasets that enables optional storage of associated metadata as key/value pairs.

### 3. Data Description
For each dataset or group of data:
- **Data Types**: Describe the data types used, whether standard or custom.
- **Layout**: Explain the layout of the data, including dimensions and shapes of datasets.
- **Compression and Chunking**: Note any compression or chunking strategies used to optimize space and read/write performance.

### 4. Metadata
Detail any metadata conventions you’ve adopted:
- **Naming Conventions**: Outline naming rules for datasets, attributes, and other components.
- **Attribute Details**: Provide templates or specific examples of attribute data structures, especially for custom metadata related to additional columns.

### 5. Custom Extensions
If your format allows extensions or custom data:
- **Adding Custom Data**: Explain how users can add custom data or extend existing structures.
- **Interoperability**: Discuss how these extensions affect interoperability with standard HDF5 tools or other common data tools.

### 6. Usage Examples
Include code snippets or examples:
- **Creating Files**: Show how to create a new .swb file with basic and complex structures.
- **Reading/Writing Data**: Provide examples of how to read from and write to these files, highlighting any custom APIs or utilities you’ve developed.
- **Handling Metadata**: Demonstrate how to interact with metadata, particularly custom attributes.

### 7. API Documentation
If you have developed specific APIs or utilities for working with your file format:
- **Function Documentation**: Document each function or method, including parameters, return values, and exceptions.
- **Libraries and Dependencies**: List any external libraries or dependencies required to work with the .swb format.

### 8. Best Practices
Offer guidance on:
- **Performance Optimization**: Tips for optimizing read/write operations, choosing compression settings, etc.
- **Data Integrity**: Suggestions for ensuring data integrity and avoiding common pitfalls in data handling.

### 9. Versioning and Compatibility
Discuss how versioning is handled:
- **Format Versions**: Explain how different versions of the format are identified and maintained.
- **Backward Compatibility**: Provide details on backward compatibility or migration paths for older format versions.

### 10. Contact and Support
Provide information on how to get support:
- **Community and Communication Channels**: List forums, mailing lists, or other channels where users can ask questions and share experiences.
- **Issue Reporting and Contributions**: Explain how users can report issues or contribute to the development of the format.

By structuring your documentation in this way, you make it accessible and useful to developers at all levels of expertise, ensuring that your file format can be widely adopted and maintained effectively.