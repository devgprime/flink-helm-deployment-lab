# Flink Helm deployment lab

Helm chart experiments for Apache Flink workloads on Kubernetes. This repository is not the upstream Helmfile project; [Helmfile](https://github.com/helmfile/helmfile) is a separate tool.

## Canonical example

New work targets `charts/flink`. It provides a minimal `FlinkDeployment` template with generic values and a values schema. It requires a compatible Flink Kubernetes Operator and its CRDs for actual deployment; rendering alone does not prove operator compatibility.

```bash
helm lint charts/flink
helm template example charts/flink --namespace flink-demo
helm template example charts/flink --set job.parallelism=2
python3 -m pip install -r tests/requirements.txt
python3 -m unittest discover -s tests -v
```

The example uses an Apache Flink example job. Supply your own image/job configuration for a real workload. CI renders and checks the chart without contacting a cluster.

## Preserved experiments

| Location | Status |
| --- | --- |
| `charts/flink` on `main` | Canonical generic example for future work |
| `HelmFlink-4` on `main` | Historical environment-specific experiment, preserved for reference |
| `helm5` branch | Alternative chart structure and configuration; retained for comparison |
| `helm5-old` branch | Earlier alternative; retained for history |

The legacy configurations contain environment-specific image names and resource references. They are not the generic quickstart. Unique branch work has not been discarded or represented as automatically merged.

## Workflow automation and benchmarking roadmap

Implemented: local lint/render checks, values validation and rendering regression tests.

Planned: operator-version compatibility tests, disposable-cluster smoke tests, deployment/recovery timing, resource measurements and automated cleanup. Chart rendering checks are not workload performance benchmarks.
