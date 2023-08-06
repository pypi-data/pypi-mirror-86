#ifndef HOMCCUBE_CONFIG_HPP
#define HOMCCUBE_CONFIG_HPP

#include <string>
#include <iostream>

namespace homccube {

enum class CacheStrategy { ALWAYS, REQUESTED, DEPTH, NOTHING, UNKNOWN };

struct Config {
  CacheStrategy cache_strategy_;
  int cache_depth_;
};

CacheStrategy strategy_from_string(const std::string& str) {
  if (str == "always") {
    return CacheStrategy::ALWAYS;
  } else if (str == "requested") {
    return CacheStrategy::REQUESTED;
  } else if (str == "nothing") {
    return CacheStrategy::NOTHING;
  } else {
    return CacheStrategy::UNKNOWN;
  }
}

} // namespace homccube
#endif
