#pragma once

#include "storage/storage_manager.h"

namespace kuzu {
namespace storage {
class GStorageManager : public StorageManager {
private:
    std::string statsPath;
public:
    GStorageManager(const std::string& statsPath, const catalog::Catalog& catalog,
        MemoryManager& memoryManager)
        : StorageManager(memoryManager), statsPath(std::move(statsPath)) {
        loadTables(catalog, nullptr, nullptr);
    }

    ~GStorageManager() override = default;

    void loadTables(const catalog::Catalog& catalog, common::VirtualFileSystem* vfs,
        main::ClientContext* context) override;
};
} // namespace storage
} // namespace kuzu