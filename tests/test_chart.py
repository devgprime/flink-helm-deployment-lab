from pathlib import Path
import subprocess
import unittest
import yaml

CHART = Path(__file__).resolve().parents[1] / 'charts/flink'

class ChartTests(unittest.TestCase):
    def render(self, *args):
        return subprocess.run(['helm', 'template', 'example', str(CHART), '--namespace', 'test-namespace', *args], text=True, capture_output=True)

    def test_default_resource_is_namespaced_and_typed(self):
        result = self.render()
        self.assertEqual(result.returncode, 0, result.stderr)
        resources = list(yaml.safe_load_all(result.stdout))
        self.assertEqual(len(resources), 1)
        obj = resources[0]
        self.assertEqual(obj['kind'], 'FlinkDeployment')
        self.assertEqual(obj['metadata'], {'name': 'example', 'namespace': 'test-namespace'})
        self.assertEqual(obj['spec']['flinkConfiguration']['taskmanager.numberOfTaskSlots'], '1')

    def test_job_override_is_preserved(self):
        result = self.render('--set', 'job.parallelism=2')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(yaml.safe_load(result.stdout)['spec']['job']['parallelism'], 2)

    def test_invalid_parallelism_is_rejected(self):
        result = self.render('--set', 'job.parallelism=0')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('parallelism', result.stderr)

    def test_empty_image_is_rejected(self):
        result = self.render('--set', 'image=')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('image', result.stderr)
