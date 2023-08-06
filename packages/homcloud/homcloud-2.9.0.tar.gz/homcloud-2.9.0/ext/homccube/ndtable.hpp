#ifndef HOMCCUBE_NDTABLE_HPP
#define HOMCCUBE_NDTABLE_HPP

namespace homccube {

constexpr int popcount(unsigned int i) {
  i = i - ((i >> 1) & 0x55555555);
  i = (i & 0x33333333) + ((i >> 2) & 0x33333333);
  i = (i + (i >> 4)) & 0x0f0f0f0f;
  i = i + (i >> 8);
  i = i + (i >> 16);
  return i & 0x3f;
}

template<int maxdim>
struct NDTable {
  int bits_to_idx[1 << maxdim];
  unsigned int idx_to_bits[maxdim + 1][1 << maxdim];
  int size[maxdim + 10];
  
  constexpr NDTable(): bits_to_idx(), idx_to_bits(), size() {
    for (int i=0; i < (1 << maxdim); ++i) {
      int m = popcount(i);
      bits_to_idx[i] = size[m];
      idx_to_bits[m][size[m]] = i;
      ++size[m];
    }
  }
};

} // namespace homccube

#endif
