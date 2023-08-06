#ifndef HOMCCUBE_CUBE_HPP
#define HOMCCUBE_CUBE_HPP
#include "basic_types.hpp"

#include <algorithm>

namespace homccube {

template<int maxdim, int dim>
struct Cube {
  using BasicTypes = homccube::BasicTypes<maxdim>;
  using Coord = typename BasicTypes::Coord;
  using Shape = typename BasicTypes::Shape;
  using ND = typename BasicTypes::ND;
  using Level = typename BasicTypes::Level;
  using PixelLevel = typename BasicTypes::PixelLevel;
  union { // このへんのコードは CubeBaseというクラスに移動
    Level level_;
    struct {
      std::uint8_t nd_;
      alignas(1) std::uint8_t padding_;
      alignas(2) std::uint16_t relative_;
      alignas(4) std::uint32_t pixel_level_;
    };
  };
  Coord coord_;

  Cube(const Coord& x, ND nd, std::uint16_t relative, PixelLevel pixel_level):
      nd_(nd), padding_(0), relative_(relative), pixel_level_(pixel_level), coord_(x) {
  }

  Cube(const Coord& x, PixelLevel pixel_level): coord_(x) {
    assert(dim == 0);
    nd_ = 0;
    padding_ = 0;
    relative_ = 0;
    pixel_level_ = pixel_level;
  }

  // For sentinel cube
  Cube(Level level) {
    std::fill(coord_.begin(), coord_.end(), 0);
    level_ = level;
  }

  bool invalid() const {
    return level_ == static_cast<Level>(-1);
  }

  static Cube invalid_cube() {
    return Cube(static_cast<Level>(-1));
  }

  std::array<int, maxdim> expand_relative() const {
    std::array<int, maxdim> ret;
    uint16_t rel = relative_;

    for (int i = maxdim - 1; i >= 0; --i) {
      ret[i] = static_cast<int>(rel % 3) - 1;
      rel /= 3;
    }
    return ret;
  }

  std::string expand_relative_string() const {
    auto relative_values = expand_relative();
    std::stringstream ss;
    for (int r: relative_values) {
      ss << r << ",";
    }
    return ss.str();
  }

  friend
  std::ostream& operator<<(std::ostream& os, const Cube& cube) {
    os << "Cube<" << maxdim << "," << dim << ">[" 
       << std::bitset<maxdim>(cube.nd_) << " "
       << cube.relative_ << "<" << cube.expand_relative_string() << "> "
       << cube.pixel_level_ << " "
       << coord2s<maxdim>(cube.coord_) << "]";

    return os;
  }


};

template<int dim>
struct Cube<2, dim> {
  static const int maxdim = 2;
  using BasicTypes = homccube::BasicTypes<maxdim>;
  using Coord = typename BasicTypes::Coord;
  using Shape = typename BasicTypes::Shape;
  using ND = typename BasicTypes::ND;
  using Level = typename BasicTypes::Level;
  using PixelLevel = typename BasicTypes::PixelLevel;

  union {
    struct {
      Coord coord_;
      std::uint32_t nd_: 2; 
      std::uint32_t pixel_level_: 30;
    };
    Level level_;
  };

  Cube(Coord x, ND nd, PixelLevel pixel_level):
      coord_(x), nd_(nd), pixel_level_(pixel_level) {}

  // For a vertex
  Cube(Coord x, PixelLevel pixel_level):
      coord_(x), nd_(0), pixel_level_(pixel_level) {}
  
  // For sentinel cube
  Cube(Level level) {
    level_ = level;
  }

  bool invalid() const {
    return BasicTypes::invalid_coord_p(coord_);
  }

  static constexpr Cube invalid_cube() {
    return Cube(BasicTypes::invalid_coord(), 0, 0);
  }

  friend std::ostream& operator<<(std::ostream& os, const Cube& cube) {
    os << "Cube<2," << dim << ">["
       << cube.pixel_level_ << " "
       << std::bitset<maxdim>(cube.nd_) << " "
       << coord2s<2>(cube.coord_) << "]";
    return os;
  }
};


template<int dim>
struct Cube<3, dim> {
  static const int maxdim = 3;
  using BasicTypes = homccube::BasicTypes<maxdim>;
  using Coord = typename BasicTypes::Coord;
  using Shape = typename BasicTypes::Shape;
  using ND = typename BasicTypes::ND;
  using Level = typename BasicTypes::Level;
  using PixelLevel = typename BasicTypes::PixelLevel;

  union {
    struct {
      Coord coord_;
      std::uint32_t nd_: 3; 
      std::uint32_t pixel_level_: 29;
    };
    Level level_;
  };

  Cube(Coord x, ND nd, PixelLevel pixel_level):
      coord_(x), nd_(nd), pixel_level_(pixel_level) {}

  // For a vertex
  Cube(Coord x, PixelLevel pixel_level):
      coord_(x), nd_(0), pixel_level_(pixel_level) {}
  
  // For sentinel cube
  Cube(Level level) {
    level_ = level;
  }

  bool invalid() const {
    return level_ == static_cast<Level>(-1);
  }

  static Cube invalid_cube() {
    return Cube(static_cast<Level>(-1));
  }

  friend std::ostream& operator<<(std::ostream& os, const Cube& cube) {
    os << "Cube<3," << dim << ">["
       << cube.pixel_level_ << " "
       << std::bitset<maxdim>(cube.nd_) << " "
       << coord2s<3>(cube.coord_) << "]";
    return os;
  }
};

template<int dim>
struct Cube<4, dim> {
  static const int maxdim = 4;
  using BasicTypes = homccube::BasicTypes<maxdim>;
  using Coord = typename BasicTypes::Coord;
  using Shape = typename BasicTypes::Shape;
  using ND = typename BasicTypes::ND;
  using Level = typename BasicTypes::Level;
  using PixelLevel = typename BasicTypes::PixelLevel;
  static const auto INVALID_LEVEL = BasicTypes::INVALID_LEVEL;

  union {
    struct {
      Coord coord_;
      std::uint32_t nd_: 4; 
      std::uint32_t pixel_level_: 28;
    };
    Level level_;
  };

  Cube(Coord x, ND nd, PixelLevel pixel_level):
      coord_(x), nd_(nd), pixel_level_(pixel_level) {}

  // For a vertex
  Cube(Coord x, PixelLevel pixel_level):
      coord_(x), nd_(0), pixel_level_(pixel_level) {}
  
  // For sentinel cube
  Cube(Level level) {
    level_ = level;
  }

  bool invalid() const {
    return pixel_level_ == INVALID_LEVEL;
  }

  static constexpr Cube invalid_cube() {
    return Cube(Coord{{{0, 0, 0, 0}}}, INVALID_LEVEL);
  }

  friend std::ostream& operator<<(std::ostream& os, const Cube& cube) {
    os << "Cube<4," << dim << ">["
       << cube.pixel_level_ << " "
       << std::bitset<maxdim>(cube.nd_) << " "
       << coord2s<4>(cube.coord_) << "]";
    return os;
  }
};


template<int maxdim, int dim>
bool operator==(const Cube<maxdim, dim>& x, const Cube<maxdim, dim>& y) {
  return x.level_ == y.level_;
}

template<int maxdim, int dim>
bool operator!=(const Cube<maxdim, dim>& x, const Cube<maxdim, dim>& y) {
  return x.level_ != y.level_;
}

template<int maxdim, int dim>
bool operator<(const Cube<maxdim, dim>& x, const Cube<maxdim, dim>& y) {
  return x.level_ < y.level_;
}

template<typename Cube>
struct CubeHash {
  size_t operator()(const Cube& cube) const { return cube.level_; }
};
  
} // namespace homccube

#endif
