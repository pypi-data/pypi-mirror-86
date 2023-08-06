#ifndef HOMCCUBE_CUBE_MAP_HPP
#define HOMCCUBE_CUBE_MAP_HPP

#include "basic_types.hpp"
#include "cube.hpp"
#include "ndtable.hpp"

#include <numeric>

namespace homccube {



template<int maxdim, int dim, typename T>
struct CubeMap {
  using BasicTypes = homccube::BasicTypes<maxdim>;
  using Shape = typename BasicTypes::Shape;
  
  static constexpr int ndsize = homccube::NDTable<maxdim>().size[dim];

  CubeMap(const Shape& shape): shape_(shape) {
    num_vertices_ = calculate_num_vertices();
    
    for (int i = 0; i < ndsize; ++i) 
      data_[i].resize(num_vertices_);
  }
  
  CubeMap(const Shape& shape, T init): shape_(shape) {
    num_vertices_ = calculate_num_vertices();
    
    for (int i = 0; i < ndsize; ++i) 
      data_[i].resize(num_vertices_, init);
  }

  int calculate_num_vertices() const {
    return std::accumulate(shape_.begin(), shape_.end(), 1, std::multiplies<size_t>());
  }

  T& operator [](const Cube<maxdim, dim>& cube) {
    static constexpr auto ndtable = homccube::NDTable<maxdim>();
    return data_[ndtable.bits_to_idx[cube.nd_]][index(cube)];
  }

  const T& operator [](const Cube<maxdim, dim>& cube) const {
    static constexpr auto ndtable = homccube::NDTable<maxdim>();
    return data_[ndtable.bits_to_idx[cube.nd_]][index(cube)];
  }

  std::size_t index(const Cube<maxdim, dim>& cube) const {
    std::size_t retval = 0;
    for (int i = 0; i < maxdim; ++i) {
      assert(cube.coord_[i] >= 0);
      retval = retval * shape_[i] + cube.coord_[i];
    }
    return retval;
  }

  void cleanup() {
    for (int i = 0; i < ndsize; ++i)
      for (int j = 0; j < num_vertices_; ++j)
        delete data_[i][j];
  }

  Shape shape_;
  int num_vertices_;
  std::array<std::vector<T>, ndsize> data_;
};

} // namespace homccube

#endif
