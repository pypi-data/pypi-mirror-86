#ifndef HOMCCUBE_REDUCE_HPP
#define HOMCCUBE_REDUCE_HPP

#include <cassert>
#include <numeric>
#include <iostream>
#include <memory>
#include <unordered_map>

#include <boost/range/adaptor/reversed.hpp>

#include "basic_types.hpp"
#include "cube.hpp"
#include "bitmap.hpp"
#include "cube_map.hpp"
#include "pd.hpp"
#include "config.hpp"

namespace homccube {

template <int maxdim, int dim>
struct Reducer: public PD<maxdim, dim> {
  using Bitmap = homccube::Bitmap<maxdim>;
  using LCube = Cube<maxdim, dim>;
  using UCube = Cube<maxdim, dim + 1>;
  using LowerSurvivors = std::vector<LCube>;
  using UpperSurvivors = std::vector<UCube>;
  using Column = std::vector<UCube>;
  using Record = homccube::CubeMap<maxdim, dim + 1, LCube>;
  using UpperSurvivorsMarker = homccube::CubeMap<maxdim, dim + 1, char>;

  Reducer(const Bitmap& bitmap,
          const std::shared_ptr<LowerSurvivors>& lower_survivors,
          const Config& config):
      PD<maxdim, dim>(),
      bitmap_(bitmap), lower_survivors_(lower_survivors),
      upper_survivors_marker_(bitmap.shape_, true),
      cache_(bitmap.shape_, nullptr),
      record_(bitmap.shape_, LCube::invalid_cube()),
      config_(config)
  {
  }

  ~Reducer() {
    cache_.cleanup();
  }

  void compute() {
     using boost::adaptors::reverse;

    for (LCube cube: reverse(*lower_survivors_)) {
      Column tmp_column;
      cache_column(CacheStrategy::ALWAYS, cube, reduce(cube, &tmp_column));
    }
  }

  Column* reduce(const LCube& cube, Column* column) {
    if (has_cache(cube))
      return get_cache(cube);

    bitmap_.cofaces(cube, std::back_inserter(*column));
    std::sort(column->begin(), column->end());

    for (;;) {
      // A survival column is reduced to zero. This means that
      // the column corresponds to a essential pair.
      if (column->empty()) {
        this->add_essential_pair(cube.pixel_level_);
        return column;
      }

      LCube& front = record_[column->front()];

      // The column is already reduced and computed twice or more.
      if (front == cube) {
        return cache_column(CacheStrategy::REQUESTED, cube, column);
      }

      // A non-empty column is no more reducable
      if (front.invalid()) {
        front = cube;
        upper_survivors_marker_[column->front()] = false;
        this->add_pair(cube.pixel_level_, column->front().pixel_level_);
        return column;
      }

      std::vector<UCube> tmp_column;
      Column* other = reduce(front, &tmp_column);
      column_add(*other, column);
    }
  }

  void column_add(const std::vector<UCube>& other, std::vector<UCube>* column) {
    std::vector<UCube> ret;
    std::size_t i=0;
    std::size_t j=0;
    while (i < column->size() || j < other.size()) {
      if (i == column->size()) {
        ret.push_back(other[j]);
        j++;
        continue;
      }
      if (j == other.size()) {
        ret.push_back((*column)[i]);
        i++;
        continue;
      }

      UCube ucube_i = (*column)[i];
      UCube ucube_j = other[j];
      if (ucube_i == ucube_j) {
        i++; j++;
        continue;
      }

      if (ucube_i < ucube_j) {
        ret.push_back(ucube_i); ++i; continue;
      } else {
        ret.push_back(ucube_j); ++j; continue;
      }
    }
    column->swap(ret);
  }

  std::shared_ptr<UpperSurvivors> upper_survivors() const {
    auto ret = std::make_shared<UpperSurvivors>();
    bitmap_.template foreach_cube<dim+1>(
        [this, &ret](UCube x) {
          if (upper_survivors_marker_[x])
            ret->push_back(x);
        });
    std::sort(ret->begin(), ret->end());
    return ret;
  }

  bool has_cache(const LCube& cube) {
    return cache_[cube] != nullptr;
  }

  Column* get_cache(const LCube& cube) {
    return cache_[cube];
  }

  void set_cache(const LCube& cube, Column* column) {
    cache_[cube] = column;
  }

  Column* cache_column(CacheStrategy required, const LCube& cube, Column* column) {
    if (config_.cache_strategy_ == required) {
      auto v = new Column(std::move(*column));
      set_cache(cube, v);
      return v;
    } else {
      return column;
    }
  }

  const Bitmap& bitmap_;
  const std::shared_ptr<LowerSurvivors> lower_survivors_;
  UpperSurvivorsMarker upper_survivors_marker_;
  homccube::CubeMap<maxdim, dim, std::vector<UCube>*> cache_;
  Record record_;
  Config config_;
};

} // namespace homccube

#endif
