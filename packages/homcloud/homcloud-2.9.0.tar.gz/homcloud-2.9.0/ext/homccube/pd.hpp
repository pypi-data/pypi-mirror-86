#ifndef HOMCCUBE_PD_HPP
#define HOMCCUBE_PD_HPP

#include <vector>

#include "basic_types.hpp"
#include "dipha_format.hpp"
#include "bitmap.hpp"

namespace homccube {

template<int maxdim, int dim>
struct PD {
  using BasicTypes = homccube::BasicTypes<maxdim>;
  using PixelLevel = typename BasicTypes::PixelLevel;

  static const auto INFINITE_LEVEL = BasicTypes::INFINITE_LEVEL;

  PD() {}

  void add_essential_pair(PixelLevel birth) {
    birth_levels_.push_back(birth);
    death_levels_.push_back(INFINITE_LEVEL);
  }

  void add_pair(PixelLevel birth, PixelLevel death) {
    if (birth == death)
      return;

    birth_levels_.push_back(birth);
    death_levels_.push_back(death);
  }

  // Returns the number of all pairs
  uint64_t write_dipha_diagram(const Bitmap<maxdim>& bitmap, std::ostream* out) {
    uint64_t num_pairs = 0;
    for (size_t i = 0; i < birth_levels_.size(); ++i) {
      if (death_levels_[i] == INFINITE_LEVEL) {
        dipha::write_essential_pair(dim, bitmap.level2value(birth_levels_[i]), out);
        ++num_pairs;
      } else {
        double birth = bitmap.level2value(birth_levels_[i]);
        double death = bitmap.level2value(death_levels_[i]);
        if (birth != death) {
          dipha::write_pair(dim, birth, death, out);
          ++num_pairs;
        }
      }
    }
    return num_pairs;
  }

  std::vector<PixelLevel> birth_levels_;
  std::vector<PixelLevel> death_levels_;
};

} // namespace homccube
#endif
