#include <sstream>
#include <iomanip>
#include "SpatialInterface.h"

// 2020-07-08 KWS Override the column prefix (htm) and suffix (ID).
//                We always include the level in the name (e.g. htm16ID).
std::string htmCircleRegion (size_t level, double ra, double dec, double radius, std::string prefix = "htm", std::string suffix = "ID");
unsigned long htmID (size_t level, double ra, double dec);
