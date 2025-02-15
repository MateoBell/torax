# Copyright 2024 DeepMind Technologies Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for the source registry."""


from absl.testing import absltest
from absl.testing import parameterized
from torax.sources import bootstrap_current_source
from torax.sources import bremsstrahlung_heat_sink
from torax.sources import electron_cyclotron_source
from torax.sources import electron_density_sources
from torax.sources import fusion_heat_source
from torax.sources import generic_current_source
from torax.sources import generic_ion_el_heat_source as ion_el_heat
from torax.sources import ion_cyclotron_source
from torax.sources import ohmic_heat_source
from torax.sources import qei_source
from torax.sources import register_source
from torax.sources import source_models as source_models_lib


class SourceTest(parameterized.TestCase):
  """Tests for the source registry."""

  @parameterized.parameters(
      bootstrap_current_source.SOURCE_NAME,
      bremsstrahlung_heat_sink.SOURCE_NAME,
      electron_cyclotron_source.SOURCE_NAME,
      electron_density_sources.GENERIC_PARTICLE_SOURCE_NAME,
      electron_density_sources.GAS_PUFF_SOURCE_NAME,
      electron_density_sources.PELLET_SOURCE_NAME,
      fusion_heat_source.SOURCE_NAME,
      generic_current_source.SOURCE_NAME,
      ion_el_heat.SOURCE_NAME,
      ohmic_heat_source.SOURCE_NAME,
      qei_source.SOURCE_NAME,
  )
  def test_sources_in_registry_build_successfully(self, source_name: str):
    """Test that all sources in the registry build successfully."""
    registered_source = register_source.get_registered_source(source_name)
    source_class = registered_source.source_class
    source_runtime_params_class = registered_source.default_runtime_params_class
    source_builder_class = registered_source.source_builder_class
    source_builder = source_builder_class()
    self.assertIsInstance(
        source_builder.runtime_params, source_runtime_params_class
    )
    if not source_builder.links_back:
      source = source_builder()
      self.assertIsInstance(source, source_class)
    else:
      # If the source links back, we need to create a `SourceModels` object to
      # pass to the source builder.
      source_models = source_models_lib.SourceModels(
          source_builders={
              source_name: source_builder,
          }
      )
      source = source_builder(source_models)
    self.assertIsInstance(source, source_class)


if __name__ == "__main__":
  absltest.main()
