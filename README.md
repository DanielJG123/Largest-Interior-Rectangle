# Maximum Inscribed Rectangle Finder

This repository contains algorithms for finding the largest possible rectangle that can be inscribed within a given polygon. The project includes multiple implementations for different types of polygons and use cases.

## Overview

The algorithms in this repository solve the problem of finding the maximum area rectangle that can fit inside a polygon. This is a common computational geometry problem with applications in:
- Computer graphics and visualization
- CAD/CAM systems
- Geographic information systems (GIS)
- Optimization problems

## Repository Structure

```
Largest-Interior-Rectangle-1/
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── geometry_utils.py      # Common geometric utilities
│   │   ├── polygon_processor.py   # Polygon processing functions
│   │   └── rectangle_finder.py    # Main rectangle finding algorithms
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── convex_algorithm.py    # Algorithm for convex polygons
│   │   └── general_algorithm.py   # Algorithm for arbitrary polygons
│   └── visualization/
│       ├── __init__.py
│       └── plotter.py             # Visualization utilities
├── examples/
│   ├── __init__.py
│   ├── basic_example.py           # Simple usage examples
│   ├── convex_polygon_demo.py     # Convex polygon demonstrations
│   └── complex_shape_demo.py      # Complex polygon demonstrations
├── tests/
│   ├── __init__.py
│   ├── test_geometry_utils.py
│   ├── test_algorithms.py
│   └── test_visualization.py
├── requirements.txt
├── setup.py
└── README.md
```

## Algorithms

### 1. Convex Polygon Algorithm (`convex_algorithm.py`)
- **Use case**: Optimized for convex polygons
- **Method**: Uses perpendicular extensions and intersection testing
- **Performance**: Faster for convex shapes
- **Accuracy**: High precision with configurable point density

### 2. General Polygon Algorithm (`general_algorithm.py`)
- **Use case**: Works with any polygon (convex or concave)
- **Method**: Uses linear transformations and containment testing
- **Performance**: More computationally intensive but more general
- **Accuracy**: Good precision for complex shapes

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Largest-Interior-Rectangle-1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

```python
from src.algorithms.convex_algorithm import find_max_rectangle_convex
from src.algorithms.general_algorithm import find_max_rectangle_general
from src.visualization.plotter import plot_polygon_with_rectangle

# For convex polygons
polygon = [(0, 0), (2, 0), (1.5, 1), (0, 2)]
rectangle = find_max_rectangle_convex(polygon, point_gap=0.01)
plot_polygon_with_rectangle(polygon, rectangle)

# For arbitrary polygons
polygon = [(0, 0), (3, 0), (2, 2), (1, 1), (0, 2)]
rectangle = find_max_rectangle_general(polygon, point_gap=0.01)
plot_polygon_with_rectangle(polygon, rectangle)
```

## Usage Examples

See the `examples/` directory for detailed usage examples:
- `basic_example.py`: Simple polygon examples
- `convex_polygon_demo.py`: Demonstrations with convex polygons
- `complex_shape_demo.py`: Complex polygon examples

## Parameters

### Point Gap (`point_gap`)
- Controls the density of points sampled along the polygon boundary
- Smaller values = higher accuracy but slower computation
- Recommended range: 0.01 - 0.1
- Default: 0.015 for convex, 0.026 for general

## Dependencies

- `numpy`: Numerical computations
- `shapely`: Geometric operations
- `matplotlib`: Visualization
- `polygenerator`: Random polygon generation (for examples)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

[Add your license information here]

## Citation

If you use this code in your research, please cite:

```bibtex
[Add citation information here]
``` 