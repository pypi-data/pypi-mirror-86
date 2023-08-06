// -*- mode: c++ -*-
#ifndef DIPHA_ALT_READ_FILTRATION_H_
#define DIPHA_ALT_READ_FILTRATION_H_

#include <memory>
#include <stdexcept>

#include <boost/numeric/ublas/vector.hpp>
#include <boost/range/algorithm/equal.hpp>

#include "filtration.h"


namespace dipha_alt {
namespace read_filtration {

std::unique_ptr<filtration::Filtration> ReadFiltration(std::istream* is);
std::unique_ptr<filtration::Filtration> CreateFiltrationFromCubes(
    const std::vector<int>& shape, const std::vector<double>& cubes);

std::unique_ptr<std::vector<int>> NumCubes(const std::vector<int>& shape);

class ReadFiltrationError : public std::runtime_error {
 public:
  explicit ReadFiltrationError(const char* msg): std::runtime_error(msg) {}
};

using Vector = std::vector<int>;

struct Cube {
  Vector v, dv;

  bool operator==(const Cube& other) const {
    return v == other.v && dv == other.dv;
  }

  bool operator<(const Cube& other) const {
    if (v < other.v)
      return true;
    if (v > other.v)
      return false;
    return dv < other.dv;
  }
};

std::unique_ptr<std::vector<Cube>> AllNdCubes(const Vector& shape, int dim);
std::unique_ptr<std::vector<Vector>> VerticesOfCube(const Cube& cube);
std::unique_ptr<std::vector<Cube>> Boundary(const Cube& cube);

}  // namespace read_filtration
}  // namespace dipha_alt

#ifdef TWOBLUECUBES_CATCH_HPP_INCLUDED
#include <sstream>
#include <boost/numeric/ublas/io.hpp>

namespace Catch {
template<>
std::string toString(const dipha_alt::read_filtration::Cube& cube) {
  using std::string;
  return string("Cube(") + toString(cube.v) + "," + toString(cube.dv) + ")";
}

}  // namespace Catch
#endif  // TWOBLUECUBES_CATCH_HPP_INCLUDED

#endif  // DIPHA_ALT_READ_FILTRATION_H_
