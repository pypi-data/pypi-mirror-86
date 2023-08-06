// -*- mode: c++ -*-
#ifndef DIPHA_ALT_WRITE_DIAGRAM_H_
#define DIPHA_ALT_WRITE_DIAGRAM_H_

#include <ostream>

#include "filtration.h"

namespace dipha_alt {
namespace write_diagram {

void WriteDiagram(const std::vector<filtration::BirthDeathPair>& pairs,
                  std::ostream *os);

}  // namespace write_diagram
}  // namespace dipha_alt


#endif  // DIPHA_ALT_WRITE_DIAGRAM_H_
