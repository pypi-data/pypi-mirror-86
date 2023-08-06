// -*- mode: c++ -*-
#ifndef DIPHA_ALT_BOUNDARY_MATRIX_H_
#define DIPHA_ALT_BOUNDARY_MATRIX_H_

#include "bitarray.h"

namespace dipha_alt {
namespace boundary_matrix {

class BirthDeathPair {
 public:
  int birth, death;

  BirthDeathPair(int b, int d): birth(b), death(d) {}
  bool Essential();
  bool operator==(const BirthDeathPair& other) const {
    return birth == other.birth && death == other.death;
  }

  enum { INFTY = -1 };
};

class BoundaryMatrix {
 public:
  using BitArray = bitarray::BMagic;

  explicit BoundaryMatrix(int size);
  // Put *val* at (m, n)
  // m and n should be m < n
  void Put(int m, int n, int val = true);
  // Return all birth-death pairs
  std::vector<BirthDeathPair> Pairs();
  // Reduce the matrix
  void Reduce();

 private:
  int size_;
  std::vector<BitArray> columns_;
  std::vector<int> birth_to_death_;

  bool IsBirth(int k);
};

}  // namespace boundary_matrix
}  // namespace dipha_alt


// The following codes are available only if catch.hpp is included.
#ifdef TWOBLUECUBES_CATCH_HPP_INCLUDED
#include <boost/format.hpp>

namespace Catch {
template<>
std::string toString(const dipha_alt::boundary_matrix::BirthDeathPair& pair) {
  return str(boost::format("BDPair(%1%, %2%)") % pair.birth % pair.death);
}
}  // namespace Catch
#endif  // TWOBLUECUBES_CATCH_HPP_INCLUDED

#endif  // DIPHA_ALT_BOUNDARY_MATRIX_H_
