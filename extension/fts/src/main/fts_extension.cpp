#include "main/fts_extension.h"

#include "catalog/catalog.h"
#include "catalog/fts_index_catalog_entry.h"
#include "function/stem.h"
#include "main/client_context.h"

namespace kuzu {
namespace fts_extension {

using namespace extension;

static void initFTSEntries(const transaction::Transaction* transaction, catalog::Catalog& catalog) {
    for (auto& indexEntry : catalog.getIndexEntries(transaction)) {
        if (indexEntry->getIndexType() == FTSIndexCatalogEntry::TYPE_NAME &&
            !indexEntry->isLoaded()) {
            indexEntry->setAuxInfo(FTSIndexAuxInfo::deserialize(indexEntry->getAuxBufferReader()));
        }
    }
}

void FtsExtension::load(main::ClientContext* context) {
    auto& db = *context->getDatabase();
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
    kuzu::fts_extension::FtsExtension::load(context);
}

INIT_EXPORT const char* name() {
    return kuzu::fts_extension::FtsExtension::EXTENSION_NAME;
}
}
#endif
