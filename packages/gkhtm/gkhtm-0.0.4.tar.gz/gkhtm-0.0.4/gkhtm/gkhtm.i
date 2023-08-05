%module gkhtm
%{
#include "HTMCircleRegion.h"
#include "HTMCircleAllIDsCassandra.h"
%}

%include <std_string.i>
%include <std_vector.i>

// Include the header file with above prototypes
%include "HTMCircleRegion.h"

namespace std {
   %template(StringVector) vector<string>;
}

%include "HTMCircleAllIDsCassandra.h"
