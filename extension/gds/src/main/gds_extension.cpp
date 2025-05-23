#include "main/gds_extension.h"

#include "function/gds_function.h"
#include "main/client_context.h"

namespace kuzu {
namespace gds_extension {

using namespace extension;

void GdsExtension::load(main::ClientContext* context) {
}

} 
} 

#if defined(BUILD_DYNAMIC_LOAD)
extern "C" {
#if defined(_WIN32)
#define INIT_EXPORT __declspec(dllexport)
#else
#define INIT_EXPORT __attribute__((visibility("default")))
#endif
INIT_EXPORT void init(kuzu::main::ClientContext* context) {
    kuzu::gds_extension::GdsExtension::load(context);
}

INIT_EXPORT const char* name() {
    return kuzu::gds_extension::GdsExtension::EXTENSION_NAME;
}
}
#endif
