#ifndef HOMCCUBE_BITMAP_HPP
#define HOMCCUBE_BITMAP_HPP

#include <cassert>
#include <numeric>
#include <iostream>
#include <functional>

#include "basic_types.hpp"
#include "cube.hpp"
#include "ndtable.hpp"
#include "io.hpp"

namespace homccube {

template<int maxdim>
struct Bitmap {
  using BasicTypes = homccube::BasicTypes<maxdim>;
  using Coord = typename BasicTypes::Coord;
  using PixelLevel = typename BasicTypes::PixelLevel;
  using Period = typename BasicTypes::Period;
  using Axis = typename BasicTypes::Axis;
  using Shape = typename BasicTypes::Shape;
  using ND = typename BasicTypes::ND;
  using Vertex = Cube<maxdim, 0>;
  
  Bitmap(const std::vector<int>& shape, Period period = Period(0), bool use_values=true) {
    assert(shape.size() == maxdim);

    std::copy(shape.begin(), shape.end(), shape_.begin());
    period_ = period;
    use_values_ = use_values;
    num_vertices_ = compute_num_vertices();
    if (use_values)
      values_.resize(num_vertices_);
    levels_.resize(num_vertices_);
    level2value_.resize(num_vertices_);
  }

  void load(std::initializer_list<double> list) {
    assert(num_vertices_ == list.size());
    std::copy(list.begin(), list.end(), values_.begin());
    update_levels();
  }

  void load(std::istream* io) {
    for (std::size_t i = 0; i < num_vertices_; ++i)
      values_[i] = binread<double>(io);
    update_levels();
  }

  void update_levels() {
    std::vector<std::size_t> sorted_indices(num_vertices_);
    std::iota(sorted_indices.begin(), sorted_indices.end(), 0);
    std::sort(sorted_indices.begin(), sorted_indices.end(),
              [this](std::size_t x, std::size_t y) {
                return values_[x] < values_[y];
              });
    for (std::size_t i = 0; i < num_vertices_; ++i)
      levels_[sorted_indices[i]] = i;

    for (std::size_t i = 0; i < num_vertices_; ++i)
      level2value_[i] = values_[sorted_indices[i]];
  }

  std::size_t compute_num_vertices() const {
    return std::accumulate(shape_.begin(), shape_.end(), 1,
                           std::multiplies<size_t>());
  }

  std::size_t coord2index(const Coord& coord) const {
    return BasicTypes::coord2index(coord, shape_);
  }

  Coord index2coord(std::size_t k) const {
    return BasicTypes::index2coord(k, shape_);
  }

  double& values(const Coord& coord) { return values_[coord2index(coord)]; }
  const double& values(const Coord& coord) const {
    return values_[coord2index(coord)];
  }
  PixelLevel& levels(const Coord& coord) { return levels_[coord2index(coord)]; }
  const PixelLevel& levels(const Coord& coord) const {
    return levels_[coord2index(coord)];
  }

  Vertex vertex(const Coord& x) const {
    return Vertex(x, levels(x));
  }

  template<int dim>
  inline PixelLevel search_maxlevel(const Coord& x, const Coord& y) const {
    if (maxdim == 2) return search_maxlevel_2(x, y);
    if (maxdim == 3) return search_maxlevel_3(x, y);
    if (maxdim == 4) return search_maxlevel_4(x, y);

    std::array<int, maxdim> on;
    int k = 0;
    for (int i = 0; i < maxdim; ++i)
      if (x[i] != y[i])
        on[k++] = i;

    PixelLevel maxlevel = 0;

    for (std::uint8_t i = 0; i < (1 << dim); ++i) {
      Coord at = x;
      for (int j = 0; j < dim; ++j) {
        at[on[j]] = GetBit(i, j) ? y[on[j]] : x[on[j]];
      }
      PixelLevel level = levels(at);
      if (maxlevel <= level) {
        maxlevel = level;
      }
    }
    return maxlevel;
  }

  inline PixelLevel search_maxlevel_2(const Coord& x, const Coord& y) const {
    static const auto build_coord = BasicTypes::build_coord;
    PixelLevel maxlevel = levels(build_coord({x[0], x[1]}));
    if (x[0] != y[0])
      maxlevel = std::max(maxlevel, levels(build_coord({y[0], x[1]})));
    if (x[1] != y[1])
      maxlevel = std::max(maxlevel, levels(build_coord({x[0], y[1]})));
    if ((x[0] != y[0]) && (x[1] != y[1]))
      maxlevel = std::max(maxlevel, levels(build_coord({y[0], y[1]})));
    return maxlevel;
  }

  inline PixelLevel search_maxlevel_3(const Coord& x, const Coord& y) const {
    static const auto build_coord = BasicTypes::build_coord;
    PixelLevel maxlevel = 0;

    std::array<Coord, 2> cubes = {x, y};
    int imax = (x[0] == y[0]) ? 1 : 2;
    int jmax = (x[1] == y[1]) ? 1 : 2;
    int kmax = (x[2] == y[2]) ? 1 : 2;
    for (int i = 0; i < imax; ++i) {
      for (int j = 0; j < jmax; ++j) {
        for (int k = 0; k < kmax; ++k) {
          Coord at = build_coord({cubes[i][0], cubes[j][1], cubes[k][2]});
          maxlevel = std::max(maxlevel, levels(at));
        }
      }
    }
    return maxlevel;
  }

  inline PixelLevel search_maxlevel_4(const Coord& x, const Coord& y) const {
    static const auto build_coord = BasicTypes::build_coord;
    PixelLevel maxlevel = 0;

    std::array<Coord, 2> cubes = {x, y};
    int imax = (x[0] == y[0]) ? 1 : 2;
    int jmax = (x[1] == y[1]) ? 1 : 2;
    int kmax = (x[2] == y[2]) ? 1 : 2;
    int lmax = (x[3] == y[3]) ? 1 : 2;
    for (int i = 0; i < imax; ++i) {
      for (int j = 0; j < jmax; ++j) {
        for (int k = 0; k < kmax; ++k) {
          for (int l = 0; l < lmax; ++l) {
            Coord at = build_coord({cubes[i][0], cubes[j][1], cubes[k][2], cubes[l][3]});
            maxlevel = std::max(maxlevel, levels(at));
          }
        }
      }
    }
    return maxlevel;
  }

#pragma GCC diagnostic ignored "-Wuninitialized"
  template<int dim>
  Cube<maxdim, dim> cube(const Coord& x, const Coord& y) const {
    Coord base;
    ND nd = 0;
    
    for (int i = 0; i < maxdim; ++i) {
      base[i] = std::min(x[i], y[i]);
      SetBit(nd, i, x[i] != y[i]);
      if (base[i] < 0)
        base[i] = shape_[i] - 1;
      else if (base[i] == shape_[i])
        base[i] = 0;
    }
    return Cube<maxdim, dim>(base, nd, search_maxlevel<dim>(x, y));
  }
#pragma GCC diagnostic warning "-Wuninitialized"
  
  template<int dim, typename Inserter>
  void coface(const Cube<maxdim, dim>& cube, int i, Axis d, Inserter inserter) const {
    Axis k = cube.coord_[i] + d;
    if (k < 0 && !period_[i])
      return;
    if (k >= shape_[i] && !period_[i])
      return;

    Coord y;
    for (int j = 0; j < maxdim; ++j)
      y[j] = (i == j) ? k : cube.coord_[j] + GetBit(cube.nd_, j);

    inserter = this->template cube<dim + 1>(cube.coord_, y);
  }
  
  template<int dim, typename Iterator>
  void cofaces(const Cube<maxdim, dim>& cube, Iterator inserter) const {
    if (dim >= maxdim)
      return;
    for (int i = 0; i < maxdim; ++i) {
      if (GetBit(cube.nd_, i) == 0) {
        coface(cube, i, 1, inserter);
        coface(cube, i, -1, inserter);
      }
    }
  }

  template<int dim>
  std::vector<Cube<maxdim, dim + 1>> cofaces(const Cube<maxdim, dim>& cube) const {
    std::vector<Cube<maxdim, dim + 1>> retval;
    cofaces(cube, std::back_inserter(retval));
    return retval;
  }

  void neighbour(int i, Axis d, Coord& coord, 
                 std::vector<Coord>& retvals) const {
    Axis orig = coord[i];
    Axis v = coord[i] + d;
    if ((v < 0 || v >= shape_[i]) && !period_[i])
      return;

    coord[i] = v;
    retvals.push_back(coord);
    coord[i] = orig;
  }
  
  void neighbours(const Coord& center,
                  std::vector<Coord>& retvals) const {
    Coord c = center;
    for (int i = 0; i < maxdim; ++i)
      neighbour(i, -1, c, retvals);
    for (int i = 0; i < maxdim; ++i)
      neighbour(i, 1, c, retvals);
  }

  std::vector<Vertex> sorted_vertices() const {
    std::vector<Vertex> retval;

    for (std::size_t i = 0; i < num_vertices_; ++i)
      retval.emplace_back(index2coord(i), levels_[i]);
    std::sort(retval.begin(), retval.end(),
              [](const Vertex& x, const Vertex& y) { return x.level_ < y.level_; });
    return retval;
  }

  template<int dim>
  void cube_iter(const Coord& x, ND nd, std::function<void (Cube<maxdim, dim>)> f) const {
    Coord y = x;
    for (int i = 0; i < maxdim; ++i) {
      if (GetBit(nd, i)) {
        y[i] = y[i] + 1;
        if (y[i] >= shape_[i] && !period_[i])
          return;
      }
    }
    f(cube<dim>(x, y));
  }


  template<int dim>
  void foreach_cube(std::function<void (Cube<maxdim, dim>)> f) const {
    static constexpr auto ndtable = homccube::NDTable<maxdim>();
    static const size_t N = ndtable.size[dim];
    
    for (std::size_t i = 0; i < num_vertices_; ++i) {
      Coord bottom = index2coord(i);
      for (size_t j = 0; j < N; ++j) {
        this->cube_iter<dim>(bottom, static_cast<ND>(ndtable.idx_to_bits[dim][j]), f);
      }
    }
  }

  double level2value(PixelLevel level) const {
    return use_values_ ? level2value_[level] : level;
  }

  Shape shape_;
  Period period_;
  bool use_values_;
  size_t num_vertices_;
  std::vector<double> values_;
  std::vector<PixelLevel> levels_;
  std::vector<double> level2value_;
};
  
} // namespace homccube

#endif
