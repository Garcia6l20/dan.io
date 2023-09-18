from dan.cxx.targets import CXXObject
from dan.core.runners import async_run
from dan.core.find import find_executable
from dan.pkgconfig.package import find_package
from dan.core.pathlib import Path
from dan import self
from dan.core.target import Installer
from dan.cxx import Library, LibraryType, Executable, BuildType
from dan.src.github import GitHubReleaseSources

version = self.options.add('version', '1.5.0')
description = 'A collection of state-of-the-art algorithms for the training, serving and interpretation of Decision Forest models.'


# TODO make it a utility


class _ProtocObject(CXXObject, internal=True):

    def __init__(self, proto_file: Path, parent, *args, **kwargs) -> None:
        self.proto_file = Path(proto_file)
        name = self.proto_file.with_suffix('.pb.cc').name
        source_file = self.proto_file.with_name(name)
        if source_file.is_absolute():
            source_file = source_file.relative_to(parent.source_path)
        super().__init__(parent.build_path / source_file, parent, *args, **kwargs)
        self.header = source_file.with_suffix('.h')
        if not self.proto_file.is_absolute():
            self.proto_file = self.source_path / self.proto_file
        self.dependencies.add(self.proto_file)

    async def __build__(self):
        p = self.parent
        self.source.parent.mkdir(parents=True, exist_ok=True)
        await async_run([p.protoc, f'-I{p.source_path}', f'--cpp_out={self.build_path}',  self.proto_file], logger=p, log=False, cwd=self.build_path, env=self.toolchain.env)
        await super().__build__()


class ProtobufLibrary(Library):

    protobuf_files = []
    protobuf_headers = []

    async def __initialize__(self):

        pb = find_package('protobuf', makefile=self.makefile)
        await pb.initialize()

        self.protoc = self.makefile.cache.get('protoc_executable')
        if not self.protoc:
            self.protoc = find_executable(
                'protoc', paths=[pb.prefix], default_paths=False)
            self.makefile.cache.protoc_executable = str(self.protoc)

        self.dependencies.add(pb)
        self.includes.add(self.build_path)

        for proto_file in self.protobuf_files:
            pobj = _ProtocObject(self.source_path / proto_file, self)
            self.objs.append(pobj)
            self.protobuf_headers.append(pobj.header)

        await super().__initialize__()

    async def __install__(self, installer: Installer):
        for header in self.protobuf_headers:
            await installer.install_header(self.build_path / header, header.parent)
        return await super().__install__(installer)


class YdfSources(GitHubReleaseSources):
    name = 'ydf-sources'
    user = 'google'
    project = 'yggdrasil-decision-forests'
    use_tags = True
    patches = [
        'patches/yggdrasil_decision_forests/utils/protobuf.h.patch',
    ]


class YdfProto(ProtobufLibrary):
    library_type = LibraryType.STATIC
    name = 'ydf-proto'
    source_path = YdfSources

    dependencies = [
        'protobuf',
    ]

    public_includes = [
        '.'
    ]
    
    protobuf_files = [
        'yggdrasil_decision_forests/dataset/data_spec.proto',
        'yggdrasil_decision_forests/dataset/example.proto',
        'yggdrasil_decision_forests/dataset/formats.proto',
        'yggdrasil_decision_forests/dataset/synthetic_dataset.proto',
        'yggdrasil_decision_forests/dataset/weight.proto',
        'yggdrasil_decision_forests/learner/abstract_learner.proto',
        'yggdrasil_decision_forests/learner/cart/cart.proto',
        'yggdrasil_decision_forests/learner/decision_tree/decision_tree.proto',
        'yggdrasil_decision_forests/learner/distributed_decision_tree/dataset_cache/dataset_cache.proto',      
        'yggdrasil_decision_forests/learner/distributed_decision_tree/load_balancer/load_balancer.proto',
        'yggdrasil_decision_forests/learner/distributed_decision_tree/training.proto',
        'yggdrasil_decision_forests/learner/distributed_gradient_boosted_trees/distributed_gradient_boosted_trees.proto',
        'yggdrasil_decision_forests/learner/distributed_gradient_boosted_trees/worker.proto',
        'yggdrasil_decision_forests/learner/generic_worker/generic_worker.proto',
        'yggdrasil_decision_forests/learner/gradient_boosted_trees/early_stopping/early_stopping_snapshot.proto',
        'yggdrasil_decision_forests/learner/gradient_boosted_trees/gradient_boosted_trees.proto',
        'yggdrasil_decision_forests/learner/hyperparameters_optimizer/hyperparameters_optimizer.proto',
        'yggdrasil_decision_forests/learner/hyperparameters_optimizer/optimizers/random.proto',
        'yggdrasil_decision_forests/learner/multitasker/multitasker.proto',
        'yggdrasil_decision_forests/learner/random_forest/random_forest.proto',
        'yggdrasil_decision_forests/metric/metric.proto',
        'yggdrasil_decision_forests/model/abstract_model.proto',
        'yggdrasil_decision_forests/model/decision_tree/decision_tree.proto',
        'yggdrasil_decision_forests/model/gradient_boosted_trees/gradient_boosted_trees.proto',
        'yggdrasil_decision_forests/model/hyperparameter.proto',
        'yggdrasil_decision_forests/model/multitasker/multitasker.proto',
        'yggdrasil_decision_forests/model/prediction.proto',
        'yggdrasil_decision_forests/model/random_forest/random_forest.proto',
        'yggdrasil_decision_forests/serving/serving.proto',
        'yggdrasil_decision_forests/utils/bitmap.proto',
        'yggdrasil_decision_forests/utils/distribute/distribute.proto',
        'yggdrasil_decision_forests/utils/distribute/implementations/grpc/grpc.proto',
        'yggdrasil_decision_forests/utils/distribute/implementations/multi_thread/multi_thread.proto',
        'yggdrasil_decision_forests/utils/distribute_cli/distribute_cli.proto',
        'yggdrasil_decision_forests/utils/distribution.proto',
        'yggdrasil_decision_forests/utils/fold_generator.proto',
        'yggdrasil_decision_forests/utils/model_analysis.proto',
        'yggdrasil_decision_forests/utils/partial_dependence_plot.proto',
    ]

class YdfSharedLib(Library, internal=True):
    library_type = LibraryType.SHARED
    source_path = YdfSources
    installed = True
    public_includes = [
        '.'
    ]
    header_match = r'.{0,}yggdrasil_decision_forests/.+'

    async def __initialize__(self):
        self.includes.add(
            self.build_path,
            public=True,
        )
        if self.toolchain.build_type.is_debug_mode:
            # minimal optimization required
            if self.toolchain.type in ('gcc', 'clang'):
                self.compile_options.add('-Og')

        return await super().__initialize__()

    __headers_installed = False
    def __install_headers__(self, installer: Installer):
        if YdfSharedLib.__headers_installed:
            return []
        YdfSharedLib.__headers_installed = True
        return super().__install_headers__(installer)


class YdfModel(YdfSharedLib):
    name = 'ydf-model'

    dependencies = [
        'absl_flags',
        'absl_flags_parse',
        'absl_flags_usage',
        'absl_random_random',
        'absl_synchronization',
        'protobuf',
        'farmhash',
    ]

    private_dependencies = [
        'boost-headers',
        YdfProto,
    ]
    
    public_compile_definitions = [
        # NOTE: YGGDRASIL_EXAMPLE_IDX_64_BITS won't work since VerticalDataset::ExtractAndAppend index signature doesn't match uint64_t (either uint32_t or int64_t :/)
        'YGGDRASIL_EXAMPLE_IDX_32_BITS',
    ]

    sources = [
        'yggdrasil_decision_forests/utils/bytestream.cc',
        'yggdrasil_decision_forests/utils/bitmap.cc',
        'yggdrasil_decision_forests/utils/blob_sequence.cc',
        'yggdrasil_decision_forests/utils/filesystem_default.cc',
        'yggdrasil_decision_forests/utils/filesystem.cc',
        'yggdrasil_decision_forests/utils/concurrency_default.cc',
        'yggdrasil_decision_forests/utils/concurrency.cc',
        'yggdrasil_decision_forests/utils/csv.cc',
        'yggdrasil_decision_forests/utils/distribution.cc',
        'yggdrasil_decision_forests/utils/registration.cc',
        'yggdrasil_decision_forests/utils/logging_default.cc',
        'yggdrasil_decision_forests/utils/sharded_io.cc',
        'yggdrasil_decision_forests/utils/regex.cc',
        'yggdrasil_decision_forests/utils/plot.cc',
        'yggdrasil_decision_forests/utils/html.cc',
        'yggdrasil_decision_forests/utils/usage_default.cc',

        'yggdrasil_decision_forests/dataset/data_spec_inference.cc',
        'yggdrasil_decision_forests/dataset/data_spec.cc',
        # 'yggdrasil_decision_forests/dataset/synthetic_dataset.cc',
        'yggdrasil_decision_forests/dataset/formats.cc',
        'yggdrasil_decision_forests/dataset/vertical_dataset.cc',
        'yggdrasil_decision_forests/dataset/vertical_dataset_io.cc',
        'yggdrasil_decision_forests/dataset/weight.cc',
        'yggdrasil_decision_forests/dataset/example_reader.cc',
        'yggdrasil_decision_forests/dataset/example_writer.cc',
        'yggdrasil_decision_forests/dataset/csv_example_reader.cc',
        'yggdrasil_decision_forests/dataset/csv_example_writer.cc',

        'yggdrasil_decision_forests/serving/example_set.cc',
        'yggdrasil_decision_forests/serving/utils.cc',

        'yggdrasil_decision_forests/serving/decision_forest/utils.cc',
        'yggdrasil_decision_forests/serving/decision_forest/8bits_numerical_features.cc',
        'yggdrasil_decision_forests/serving/decision_forest/decision_forest_serving.cc',
        'yggdrasil_decision_forests/serving/decision_forest/decision_forest.cc',
        'yggdrasil_decision_forests/serving/decision_forest/register_engines.cc',
        'yggdrasil_decision_forests/serving/decision_forest/model_compiler.cc',
        'yggdrasil_decision_forests/serving/decision_forest/quick_scorer_extended.cc',

        'yggdrasil_decision_forests/metric/comparison.cc',
        'yggdrasil_decision_forests/metric/metric.cc',
        'yggdrasil_decision_forests/metric/ranking_mrr.cc',
        'yggdrasil_decision_forests/metric/ranking_ndcg.cc',
        'yggdrasil_decision_forests/metric/report.cc',
        'yggdrasil_decision_forests/metric/uplift.cc',

        'yggdrasil_decision_forests/model/abstract_model.cc',
        'yggdrasil_decision_forests/model/fast_engine_factory.cc',
        'yggdrasil_decision_forests/model/metadata.cc',
        'yggdrasil_decision_forests/model/model_engine_wrapper.cc',
        'yggdrasil_decision_forests/model/model_library.cc',
        
        'yggdrasil_decision_forests/model/decision_tree/decision_tree.cc',
        'yggdrasil_decision_forests/model/decision_tree/decision_tree_io_blob_sequence.cc',
        'yggdrasil_decision_forests/model/decision_tree/decision_tree_io.cc',
        'yggdrasil_decision_forests/model/decision_tree/structure_analysis.cc',

        'yggdrasil_decision_forests/model/random_forest/random_forest.cc',
        'yggdrasil_decision_forests/model/gradient_boosted_trees/gradient_boosted_trees.cc',
        
        'yggdrasil_decision_forests/model/multitasker/multitasker.cc',
    ]


class YdfLearner(YdfSharedLib):
    name = 'ydf-learner'

    dependencies = [
        YdfModel,
        'eigen3',
    ]

    sources = [
        'yggdrasil_decision_forests/utils/adaptive_work.cc',
        'yggdrasil_decision_forests/utils/model_analysis.cc',
        'yggdrasil_decision_forests/utils/hyper_parameters.cc',
        'yggdrasil_decision_forests/utils/feature_importance.cc',
        'yggdrasil_decision_forests/utils/partial_dependence_plot.cc',
        'yggdrasil_decision_forests/utils/fold_generator.cc',
        'yggdrasil_decision_forests/utils/snapshot.cc',
        'yggdrasil_decision_forests/utils/distribute/distribute.cc',
        'yggdrasil_decision_forests/utils/distribute/utils.cc',
        'yggdrasil_decision_forests/utils/distribute/core.cc',
        'yggdrasil_decision_forests/utils/evaluation.cc',

        'yggdrasil_decision_forests/learner/abstract_learner.cc',
        'yggdrasil_decision_forests/learner/cart/cart.cc',
        'yggdrasil_decision_forests/learner/decision_tree/generic_parameters.cc',
        'yggdrasil_decision_forests/learner/decision_tree/oblique.cc',
        'yggdrasil_decision_forests/learner/decision_tree/training.cc',
        'yggdrasil_decision_forests/learner/decision_tree/utils.cc',
        'yggdrasil_decision_forests/learner/distributed_decision_tree/dataset_cache/column_cache.cc',
        'yggdrasil_decision_forests/learner/distributed_decision_tree/dataset_cache/dataset_cache.cc',
        'yggdrasil_decision_forests/learner/distributed_decision_tree/dataset_cache/dataset_cache_common.cc',
        'yggdrasil_decision_forests/learner/distributed_decision_tree/dataset_cache/dataset_cache_reader.cc',
        'yggdrasil_decision_forests/learner/distributed_decision_tree/dataset_cache/dataset_cache_worker.cc',
        'yggdrasil_decision_forests/learner/distributed_decision_tree/load_balancer/load_balancer.cc',
        'yggdrasil_decision_forests/learner/distributed_decision_tree/training.cc',
        'yggdrasil_decision_forests/learner/distributed_gradient_boosted_trees/common.cc',
        'yggdrasil_decision_forests/learner/distributed_gradient_boosted_trees/distributed_gradient_boosted_trees.cc',
        'yggdrasil_decision_forests/learner/distributed_gradient_boosted_trees/worker.cc',
        'yggdrasil_decision_forests/learner/export_doc.cc',
        'yggdrasil_decision_forests/learner/export_doc_main.cc',
        'yggdrasil_decision_forests/learner/generic_worker/generic_worker.cc',
        'yggdrasil_decision_forests/learner/gradient_boosted_trees/early_stopping/early_stopping.cc',
        'yggdrasil_decision_forests/learner/gradient_boosted_trees/gradient_boosted_trees.cc',
        'yggdrasil_decision_forests/learner/gradient_boosted_trees/gradient_boosted_trees_hparams_templates.cc',
        'yggdrasil_decision_forests/learner/gradient_boosted_trees/loss/loss_imp_binary_focal.cc',
        'yggdrasil_decision_forests/learner/gradient_boosted_trees/loss/loss_imp_binomial.cc',
        'yggdrasil_decision_forests/learner/gradient_boosted_trees/loss/loss_imp_cross_entropy_ndcg.cc',
        'yggdrasil_decision_forests/learner/gradient_boosted_trees/loss/loss_imp_mean_square_error.cc',
        'yggdrasil_decision_forests/learner/gradient_boosted_trees/loss/loss_imp_multinomial.cc',
        'yggdrasil_decision_forests/learner/gradient_boosted_trees/loss/loss_imp_ndcg.cc',
        'yggdrasil_decision_forests/learner/gradient_boosted_trees/loss/loss_imp_poisson.cc',
        'yggdrasil_decision_forests/learner/gradient_boosted_trees/loss/loss_interface.cc',
        'yggdrasil_decision_forests/learner/gradient_boosted_trees/loss/loss_library.cc',
        'yggdrasil_decision_forests/learner/gradient_boosted_trees/loss/loss_utils.cc',
        # 'yggdrasil_decision_forests/learner/gradient_boosted_trees/plot_training.cc',
        'yggdrasil_decision_forests/learner/hyperparameters_optimizer/hyperparameters_optimizer.cc',
        'yggdrasil_decision_forests/learner/hyperparameters_optimizer/optimizers/random.cc',
        'yggdrasil_decision_forests/learner/learner_library.cc',
        'yggdrasil_decision_forests/learner/multitasker/multitasker.cc',
        'yggdrasil_decision_forests/learner/random_forest/random_forest.cc',
        'yggdrasil_decision_forests/learner/random_forest/random_forest_hparams_templates.cc',
        'yggdrasil_decision_forests/learner/types.cc',
    ]


class Ydf(Library):
    name = 'ydf'
    installed = True
    library_type = LibraryType.INTERFACE
    dependencies = [
        YdfModel, YdfLearner
    ]


if self.options.add('build-executables', False).value:

    class YdfExecutable(Executable, internal=True):
        source_path = YdfSources
        installed = True
        build_type = BuildType.release


    class YdfTrain(YdfExecutable):
        name = 'ydf-train'
        dependencies = [
            Ydf,
        ]
        sources = [
            'yggdrasil_decision_forests/cli/train.cc',
        ]

    class YdfPredict(YdfExecutable):
        name = 'ydf-predict'
        dependencies = [
            Ydf,
        ]
        sources = [
            'yggdrasil_decision_forests/cli/predict.cc',
        ]

    class YdfEvaluate(YdfExecutable):
        name = 'ydf-evaluate'
        dependencies = [
            Ydf,
        ]
        sources = [
            'yggdrasil_decision_forests/cli/evaluate.cc',
        ]

    class YdfEditModel(YdfExecutable):
        name = 'ydf-edit-model'
        dependencies = [
            Ydf,
        ]
        sources = [
            'yggdrasil_decision_forests/cli/edit_model.cc',
        ]

    class YdfAnalyze(YdfExecutable):
        name = 'ydf-analyze'
        dependencies = [
            Ydf,
        ]
        sources = [
            'yggdrasil_decision_forests/cli/analyze_model_and_dataset.cc',
        ]

    class YdfComputeVariablesImprotance(YdfExecutable):
        name = 'ydf-compute-variables-imprortance'
        dependencies = [
            Ydf,
        ]
        sources = [
            'yggdrasil_decision_forests/cli/compute_variable_importances.cc',
        ]

    class YdfCompileModel(YdfExecutable):
        name = 'ydf-compile'
        dependencies = [
            Ydf,
        ]
        sources = [
            'yggdrasil_decision_forests/cli/compile_model.cc',
        ]


    class YdfBenchmarkInference(YdfExecutable):
        name = 'ydf-benchmark-inference'
        dependencies = [
            Ydf,
        ]
        sources = [
            'yggdrasil_decision_forests/cli/benchmark_inference.cc',
        ]

    class YdfInferDataspec(YdfExecutable):
        name = 'ydf-infer-dataspec'
        dependencies = [
            Ydf,
        ]
        sources = [
            'yggdrasil_decision_forests/cli/infer_dataspec.cc',
        ]


    class YdfShowDataspec(YdfExecutable):
        name = 'ydf-show-dataspec'
        dependencies = [
            Ydf,
        ]
        sources = [
            'yggdrasil_decision_forests/cli/show_dataspec.cc',
        ]

    class YdfShowModel(YdfExecutable):
        name = 'ydf-show-model'
        dependencies = [
            Ydf,
        ]
        sources = [
            'yggdrasil_decision_forests/cli/show_model.cc',
        ]
