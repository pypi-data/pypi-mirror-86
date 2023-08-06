#ifndef HOMCCUBE_DIPHA_HPP
#define HOMCCUBE_DIPHA_HPP

#include "bitmap.hpp"
#include "link_find.hpp"
#include "reduce.hpp"

namespace homccube { namespace dipha {

template<int maxdim, int dim>
using Survivors = std::shared_ptr<std::vector<Cube<maxdim, dim>>>;

template<int maxdim>
Survivors<maxdim, 1>
compute_0th_pd(const Bitmap<maxdim>& bitmap, std::ostream* out, uint64_t* num_pairs) {
  LinkFind<maxdim> link_find(bitmap);
  link_find.compute();
  *num_pairs += link_find.write_dipha_diagram(bitmap, out);
  return link_find.survivors_;
}

template<int maxdim, int dim>
Survivors<maxdim, dim + 1>
compute_kth_pd(const Bitmap<maxdim>& bitmap,
               const Survivors<maxdim, dim> lower_survivors,
               Config config, std::ostream* out, uint64_t* num_pairs) {
  if (maxdim <= dim || (maxdim == dim && lower_survivors->size() == 0))
    return nullptr;
  Reducer<maxdim, dim> reducer(bitmap, lower_survivors, config);
  reducer.compute();
  *num_pairs += reducer.write_dipha_diagram(bitmap, out);
  return reducer.upper_survivors();
}

}} // namespace homccube::dipha
#endif

