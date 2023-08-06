#ifndef HOMCCUBE_BASIC_TYPES_HPP
#define HOMCCUBE_BASIC_TYPES_HPP

#include <cstdint>
#include <array>
#include <bitset>
#include <string>
#include <sstream>
#include <limits>
#include <vector>
#include <array>
#include <cstdint>

#ifdef __clang__
#pragma clang diagnostic ignored "-Wunknown-warning-option"
#endif

namespace homccube {

inline bool GetBit(std::uint8_t n, int i) {
  return (1 << i) & n;
}

inline void SetBit(std::uint8_t& n, int i, bool value) {
  n |= (static_cast<std::uint8_t>(value) << i);
}

template<int maxdim> struct BasicTypes;

template<>
struct BasicTypes<2> {
  static const int maxdim = 2;
  using Axis = std::int16_t;
  using PixelLevel = std::uint32_t;
  using Level = std::uint64_t;
  using Shape = std::array<int, maxdim>;
  using Period = std::bitset<maxdim>;
  using ND = std::uint8_t;
  static const Level INFINITE_LEVEL = (1<<30) - 1;

  using Coord = std::array<Axis, 2>;

  static constexpr Coord empty_coord() {
    return Coord{-2, -2};
  };

  static constexpr Coord root_coord() {
    return Coord{-2, -3};
  }

  static constexpr Coord invalid_coord() {
    return Coord{-3, -3};
  }

  static bool invalid_coord_p(const Coord x) {
    return x[0] == -3 && x[1] == -3;
  }

  static Coord build_coord(std::initializer_list<Axis> list) {
    assert(list.size() == 2);
    return Coord{list.begin()[0], list.begin()[1]};
  }

  static std::size_t coord2index(const Coord& coord, const Shape& shape) {
    std::size_t c0 = (coord[0] + shape[0]) % shape[0];
    std::size_t c1 = (coord[1] + shape[1]) % shape[1];
    return c0 * shape[1] + c1;
  }

  static Coord index2coord(std::size_t k, const Shape& shape) {
    return Coord{static_cast<Axis>(k / shape[1]), static_cast<Axis>(k % shape[1])};
  }

  static bool valid_shape(const std::vector<int>& shape) {
    return (shape.size() == 2) &&
        (shape[0] > 0) && (shape[0] < (1<<15) - 2) &&
        (shape[1] > 0) && (shape[1] < (1<<15) - 2);
  }
};

template<>
struct BasicTypes<3> {
 private:
  static const uint32_t MASK_11BIT = 0b11111111111;
  static const uint32_t MASK_10BIT = 0b1111111111;

 public:
  static const int maxdim = 3;
  using Axis = std::int16_t;
  using PixelLevel = std::uint32_t;
  using Level = std::uint64_t;
  using Shape = std::array<int, 3>;
  using Period = std::bitset<3>;
  using ND = std::uint8_t;
  static const Level INFINITE_LEVEL = (1<<29) - 1;

  class Coord {
    inline static Axis get_field(uint32_t field, size_t n) {
      assert(n < 3);
      uint32_t value = (field >> (11 * n)) & MASK_11BIT;
      if (n == 2)
        return (value == MASK_10BIT) ? -1 : value;
      else
        return (value == MASK_11BIT) ? -1 : value;
    }

    class reference {
      uint32_t* field_;
      size_t n_;

     public:
      reference(uint32_t* field, size_t n): field_(field), n_(n) {
        assert(n < 3);
      }

#pragma GCC diagnostic ignored "-Wmaybe-uninitialized"
#pragma GCC diagnostic ignored "-Wuninitialized"
      reference& operator=(Axis x) {
        assert(x >= -1);
        *field_ &= ~(MASK_11BIT << (11 * n_));
        *field_ |= (static_cast<uint32_t>(x) & MASK_11BIT) << (11 * n_);
        return *this;
      }
#pragma GCC diagnostic warning "-Wmaybe-uninitialized"
#pragma GCC diagnostic warning "-Wuninitialized"

      operator Axis() const {
        return get_field(*field_, n_);
      }
    };

   public:
    reference operator[](size_t n) { return reference(&field_, n); }
    const Axis operator[](size_t n) const {
      return get_field(field_, n);
    }

    friend bool operator==(Coord x, Coord y) { return x.field_ == y.field_; }
    uint32_t field_;
  };

  static constexpr Coord empty_coord() {
    return Coord{((MASK_10BIT - 2) << 22) |
          ((MASK_11BIT - 1) << 11) |
          (MASK_11BIT - 1)};
  }

  static constexpr Coord root_coord() {
    return Coord{((MASK_10BIT - 3) << 22) |
          ((MASK_11BIT - 1) << 11) |
          (MASK_11BIT - 1)};
  }

  static Coord build_coord(std::initializer_list<Axis> list) {
    assert(list.size() == 3);
    uint32_t field =
        (static_cast<uint32_t>(list.begin()[0]) & MASK_11BIT) |
        ((static_cast<uint32_t>(list.begin()[1]) & MASK_11BIT) << 11) |
        ((static_cast<uint32_t>(list.begin()[2]) & MASK_10BIT) << 22);
    return Coord{field};
  }

  static std::size_t coord2index(const Coord& coord, const Shape& shape) {  
    std::size_t retval = 0;
    for (int i=0; i < maxdim; ++i) {
      retval = retval * shape[i] + ((coord[i] + shape[i]) % shape[i]);
    }
    return retval;
  }

  static Coord index2coord(std::size_t k, const Shape& shape) {
    Coord x = {0};
    for (int i = maxdim - 1; i >= 0; --i) {
      x[i] = k % shape[i];
      k /= shape[i];
    }
    return x;
  }
    
  // Return true if the shape is acceptable for 3D cubical set
  //
  // 2048 is not acceptable because -1 == 2047 has special meaning in coord
  static bool valid_shape(const std::vector<int>& shape) {
    return
        (shape.size() == 3) &&
        (shape[0] > 0) && (shape[0] < 2046) &&
        (shape[1] > 0) &&(shape[1] < 2046) &&
        (shape[2] > 0) && (shape[2] < 1022) &&
        ((size_t)shape[0] * (size_t)shape[1] * (size_t)shape[2] <= (1<<29) - 4);
  }
};

template<>
struct BasicTypes<4> {
  static const int maxdim = 4;
  using Axis = std::int16_t;
  using PixelLevel = std::uint32_t;
  using Level = std::uint64_t;
  using Shape = std::array<int, 4>;
  using ND = std::uint8_t;
  using Period = std::bitset<4>;

  static const Level INFINITE_LEVEL = static_cast<uint32_t>((1<<28) - 1);
  static const PixelLevel INVALID_LEVEL = static_cast<uint32_t>((1<<28) - 2);

  class Coord {
    inline static Axis get_value(uint8_t value) {
      return (value == 0xff) ? -1 : value;
    }
    
    class reference {
      uint8_t* data_;
      size_t n_;

     public:
      reference(uint8_t* data, size_t n): data_(data), n_(n) {
        assert(n < 4);
      }

      reference& operator=(Axis x) {
        assert(x >= -1);
        data_[n_] = static_cast<uint8_t>(x);
        return *this;
      }

      operator Axis() const {
        return get_value(data_[n_]);
      }
    };

   public:
    reference operator[](size_t n) { return reference(data_, n); }
    const Axis operator[](size_t n) const {
      assert(n < 4);
      return get_value(data_[n]);
    }

    friend bool operator==(Coord x, Coord y) { return x.field_ == y.field_; }

    union {
      uint8_t data_[4];
      uint32_t field_;
    };
  };

  static bool valid_shape(const std::vector<int>& shape) {
    return
        (shape.size() == 4) &&
        (shape[0] > 0) && (shape[0] <= 253) &&
        (shape[1] > 0) &&(shape[1] <= 253) &&
        (shape[2] > 0) && (shape[2] <= 252) &&
        (shape[3] > 0) && (shape[3] <= 252) &&
        ((size_t)shape[0] * (size_t)shape[1] * (size_t)shape[2] * (size_t)shape[3]
         <= (1<<28) - 4);
  }

  static constexpr Coord empty_coord() {
    return build_coord({0, 0, 254, 0});
  };

  static constexpr Coord root_coord() {
    return build_coord({0, 0, 0, 254});
  }

  static constexpr Coord build_coord(std::initializer_list<Axis> list) {
    uint8_t x = list.begin()[0];
    uint8_t y = list.begin()[1];
    uint8_t z = list.begin()[2];
    uint8_t w = list.begin()[1];
    return Coord{{{x, y, z, w}}};
  }
  
  static std::size_t coord2index(const Coord& coord, const Shape& shape) {  
    std::size_t retval = 0;
    for (int i=0; i < maxdim; ++i) {
      retval = retval * shape[i] + ((coord[i] + shape[i]) % shape[i]);
    }
    return retval;
  }

  static Coord index2coord(std::size_t k, const Shape& shape) {
    Coord x;
    for (int i = maxdim - 1; i >= 0; --i) {
      x[i] = k % shape[i];
      k /= shape[i];
    }
    return x;
  }

};


template<int maxdim> using Coord = typename BasicTypes<maxdim>::Coord;
template<int maxdim> using Shape = typename BasicTypes<maxdim>::Shape;


template<int maxdim>
std::string coord2s(const Coord<maxdim>& coord) {
  std::stringstream ss;
  ss << "{";
  for (int i = 0; i < maxdim; ++i) {
    ss << coord[i];
    if (i != maxdim - 1)
      ss << ",";
  }
  ss << "}";
  return ss.str();
}

} // namespace homccube
#endif

