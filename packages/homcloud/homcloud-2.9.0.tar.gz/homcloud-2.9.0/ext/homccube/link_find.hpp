#ifndef HOMCCUBE_LINK_FIND_HPP
#define HOMCCUBE_LINK_FIND_HPP
#include <memory>

#include "basic_types.hpp"
#include "pd.hpp"
#include "bitmap.hpp"
#include "cube_map.hpp"


namespace homccube {

template<int maxdim>
struct LinkFind: public PD<maxdim, 0> {
  using BasicTypes = homccube::BasicTypes<maxdim>;
  using Coord = typename BasicTypes::Coord;
  using PixelLevel = typename BasicTypes::PixelLevel;
  using Axis = typename BasicTypes::Axis;
  using Bitmap = homccube::Bitmap<maxdim>;
  using Vertex = Cube<maxdim, 0>;
  using Survivor = Cube<maxdim, 1>;
  static constexpr auto empty_coord = BasicTypes::empty_coord;
  static constexpr auto root_coord = BasicTypes::root_coord;

  struct Tree {
    Tree(const Bitmap& bitmap):
        bitmap_(bitmap), data_(bitmap.num_vertices_, empty_coord()) {
    }

    Coord& operator [](const Coord& coord) {
      return data_[bitmap_.coord2index(coord)];
    }

    const Coord& operator [](const Coord& coord) const {
      return data_[bitmap_.coord2index(coord)];
    }

    bool empty_p(const Coord& coord) const {
      return (*this)[coord] == empty_coord();
    }

    Coord root(const Coord coord) {
      Coord& parent = (*this)[coord];
      if (parent == root_coord())
        return coord;
      return parent = root(parent);
    }

    void set_root(const Coord coord) {
      (*this)[coord] = root_coord();
    }

    const Bitmap& bitmap_;
    std::vector<Coord> data_;
  };

  LinkFind(const Bitmap& bitmap):
      PD<maxdim, 0>(), bitmap_(bitmap), tree_(bitmap),
      survivors_(std::make_shared<std::vector<Survivor>>())
  {
  }

  void compute() {
    auto vertices = bitmap_.sorted_vertices();
    std::vector<Coord> neighbours;

    this->add_essential_pair(vertices[0].pixel_level_);

    for (const auto& vertex: vertices) {
      Coord center = vertex.coord_;
      tree_.set_root(center);
      PixelLevel center_level = vertex.pixel_level_;

      neighbours.clear();
      bitmap_.neighbours(center, neighbours);
      for (const auto& neighbour: neighbours) {
        if (tree_.empty_p(neighbour))
          continue;
        Coord root1 = tree_.root(center);
        Coord root2 = tree_.root(neighbour);
        PixelLevel level1 = bitmap_.levels(root1);
        PixelLevel level2 = bitmap_.levels(root2);

        if (level1 == level2) {
          survivors_->push_back(bitmap_.template cube<1>(center, neighbour));
        } else if (level1 > level2) {
          if (level1 != center_level)
            this->add_pair(level1, center_level);
          tree_[root1] = tree_[center] = root2;
        } else {
          this->add_pair(level2, center_level);
          tree_[root2] = tree_[neighbour] = root1;
        }
      }
    }
    std::sort(survivors_->begin(), survivors_->end());
  }

  const Bitmap& bitmap_;
  Tree tree_;
  std::shared_ptr<std::vector<Survivor>> survivors_;
};

} // namespace homccube

#endif
