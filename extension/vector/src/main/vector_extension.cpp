#include "main/vector_extension.h"

#include "catalog/hnsw_index_catalog_entry.h"
#include "main/client_context.h"
#include "main/database.h"

namespace kuzu {
namespace vector_extension {

static void initHNSWEntries(const transaction::Transaction* transaction,
    catalog::Catalog& catalog) {
    for (auto& indexEntry : catalog.getIndexEntries(transaction)) {
        if (indexEntry->getIndexType() == HNSWIndexCatalogEntry::TYPE_NAME &&
            !indexEntry->isLoaded()) {
            indexEntry->setAuxInfo(HNSWIndexAuxInfo::deserialize(indexEntry->getAuxBufferReader()));
        }
    }
}

void VectorExtension::load(main::ClientContext* context) {
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
    kuzu::vector_extension::VectorExtension::load(context);
}

INIT_EXPORT const char* name() {
    return kuzu::vector_extension::VectorExtension::EXTENSION_NAME;
}
}
#endif
