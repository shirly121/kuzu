#include "processor/operator/profile.h"

#include "main/plan_printer.h"
#include "processor/execution_context.h"

using namespace kuzu::common;
using namespace kuzu::main;

namespace kuzu {
namespace processor {

void Profile::initLocalStateInternal(ResultSet* resultSet, ExecutionContext* /*context*/) {
    outputVector = resultSet->getValueVector(outputPos).get();
}

bool Profile::getNextTuplesInternal(ExecutionContext* context) {
    return false;
}

} // namespace processor
} // namespace kuzu
