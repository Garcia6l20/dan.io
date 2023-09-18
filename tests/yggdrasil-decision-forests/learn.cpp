#include "yggdrasil_decision_forests/model/model_library.h"

namespace ydf = yggdrasil_decision_forests;

int main() {
    
    // Load the model.
    std::unique_ptr<ydf::model::AbstractModel> model;
    const auto status = ydf::model::LoadModel("h://Projects/g6-workspace/mm/programs/batector/models/rf_model/assets", &model);
    if (!status.ok()) {
        std::cerr << status << '\n';
        throw std::runtime_error("failed to load model");
    }

    // Compile the model into an inference engine.
    const auto engine = model->BuildFastEngine().value();

    // Index the input features of the model.
    //
    // For efficiency reasons, it is important to index the input features when
    // loading the model, and not when generating predictions.
    const auto& features = engine->features();
    // const auto feature_cd = features.GetNumericalFeatureId("cd").value();
    const auto feature_fme = features.GetNumericalFeatureId("fme").value();
    const auto feature_min = features.GetNumericalFeatureId("min").value();
    const auto feature_max = features.GetNumericalFeatureId("max").value();

    // At this point, "model" can be discarded.
    model.reset(nullptr);

    // Allocate memory for 10 examples. Alternatively, for speed-sensitive code,
    // the "examples" object can be allocated in the stage 2 and reused everytime.
    auto examples = engine->AllocateExamples(10);

    // Set all the values to be missing. The values may then be overridden by the
    // "Set*" methods. If all the values are set with "Set*" methods, "FillMissing"
    // can be skipped.
    examples->FillMissing(features);

    // Prepare one example.
    // examples->SetNumerical(/*example_idx=*/0, feature_cd, 6.0, features);
    examples->SetNumerical(/*example_idx=*/0, feature_fme, 46.0, features);
    examples->SetNumerical(/*example_idx=*/0, feature_min, 45.0, features);
    examples->SetNumerical(/*example_idx=*/0, feature_max, 50.0, features);
    // examples->SetCategorical(/*example_idx=*/0, feature_country, "UK", features);
    // examples->SetCategoricalSet(/*example_idx=*/0, feature_text,
    //     std::vector<std::string>{"hello", "world"}, features);

    // Prepare another example.
    // examples->SetNumerical(/*example_idx=*/1, feature_age, 30, features);
    // examples->SetCategorical(/*example_idx=*/1, feature_country, "UK", features);
    // examples->SetCategoricalSet(/*example_idx=*/1, feature_text,
    //     std::vector<std::string>{"hello", "world"}, features);

    // Run the model on the two examples.
    //
    // Note: When possible, prepare and run multiple examples at a time.
    std::vector<float> predictions;
    engine->Predict(*examples, /*num_examples=*/1, &predictions);

    int idx = 0;
    for (auto const& pred : predictions) {
        std::cout << idx++ << ": " << pred << '\n';        
    }

    return 0;
}
