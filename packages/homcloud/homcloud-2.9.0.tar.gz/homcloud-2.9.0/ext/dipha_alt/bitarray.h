// -*- mode: c++ -*-
#ifndef DIPHA_ALT_BITARRAY_H_
#define DIPHA_ALT_BITARRAY_H_

#include <bm/bm.h>

#include <vector>

namespace dipha_alt {
namespace bitarray {

class BitArray {
 public:
  virtual void Put(int n, bool val = true) = 0;
  virtual bool Get(int n) const = 0;
  virtual int Pivot() const = 0;
  virtual void Add(const BitArray& other) = 0;
  virtual std::vector<int> BitPositions() const = 0;
  virtual bool Empty() const = 0;
  virtual ~BitArray() = default;
};

class BMagic: public BitArray {
 public:
  // Create Empty array with size n
  explicit BMagic(int n);
  virtual void Put(int n, bool val = true);
  virtual bool Get(int n) const;
  virtual int Pivot() const;
  virtual void Add(const BitArray& other);
  virtual bool Empty() const;
  virtual std::vector<int> BitPositions() const;

  virtual ~BMagic() = default;

 private:
  bm::bvector<> bvec_;
  int size_;
};

}  // namespace bitarray
}  // namespace dipha_alt

#endif  //  DIPHA_ALT_BITARRAY_H_
