// -*- mode: c++ -*-
#ifndef DIPHA_ALT_FILTRATION_H_
#define DIPHA_ALT_FILTRATION_H_

#include <vector>
#include <memory>
#include <iostream>
#include <cmath>

#include "boundary_matrix.h"

namespace dipha_alt {
namespace filtration {

struct Simplex {
  Simplex(int d, double btime): dim(d), birth_time(btime) {}
  int ascending_order;
  int dim;
  double birth_time;
};

struct BirthDeathPair {
  int dim;
  double birth, death;

  BirthDeathPair(int d, double bt, double dt): dim(d), birth(bt), death(dt) {}

  bool Essential() const { return std::isinf(death); }

  bool operator==(const BirthDeathPair& other) const {
    return dim == other.dim && birth == other.birth && death == other.death;
  }
};

class Filtration {
 public:
  // Initialize an empty filtration
  Filtration(): simplices_(), boundaries_(), order_() {}
  // Add simplex and return the index of the simplex
  int AddSimplex(int dim, double birth_time);
  // Calculate the order of simplices by birth_time and numbering simplices
  // by that order
  void NumberSimplices();
  // Add boundary
  void AddBoundary(int to, int from);
  // Return boundary matrix
  std::unique_ptr<boundary_matrix::BoundaryMatrix> CreateBoundaryMatrix();
  std::unique_ptr<std::vector<BirthDeathPair>> ComputeBirthDeathPairs();

  std::vector<int> NumbersOfSimplices();

  ~Filtration() = default;

 private:
  // All contained simplices
  std::vector<Simplex> simplices_;
  // Boundary relation (to, from)
  std::vector<std::pair<int, int>> boundaries_;
  // Order of simplices by their birth_time
  std::vector<int> order_;
};

}  // namespace filtration
}  // namespace dipha_alt

// The following codes are available only if catch.hpp is included.
#ifdef TWOBLUECUBES_CATCH_HPP_INCLUDED
#include <boost/format.hpp>

namespace Catch {
template<>
std::string toString(const dipha_alt::filtration::BirthDeathPair& pair) {
  return str(boost::format("BDPair(dim=%1%, birth=%2%, death=%3%)")
             % pair.dim % pair.birth % pair.death);
}
}  // namespace Catch
#endif  // TWOBLUECUBES_CATCH_HPP_INCLUDED

#endif  // DIPHA_ALT_FILTRATION_H_
