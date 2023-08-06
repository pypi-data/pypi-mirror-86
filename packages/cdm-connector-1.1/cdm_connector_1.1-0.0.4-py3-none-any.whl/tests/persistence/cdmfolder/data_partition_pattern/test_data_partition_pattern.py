﻿# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.

import os
import unittest

from cdm.enums import CdmObjectType
from cdm.objectmodel import CdmCorpusContext, CdmCorpusDefinition
from cdm.persistence.cdmfolder import ManifestPersistence
from cdm.persistence.cdmfolder.types import ManifestContent

from tests.common import async_test, TestHelper

class DataPartitionPatternTest(unittest.TestCase):
    test_subpath = os.path.join('Persistence', 'CdmFolder', 'DataPartitionPattern')

    def test_load_local_entity_with_data_partition_pattern(self):
        content = TestHelper.get_input_file_content(self.test_subpath, "test_load_local_entity_with_data_partition_pattern", "entities.manifest.cdm.json")
        manifest_content = ManifestContent()
        manifest_content.decode(content)

        cdmManifest = ManifestPersistence.from_object(CdmCorpusContext(CdmCorpusDefinition(), None), "entities", "testNamespace", "/", manifest_content)
        self.assertEqual(len(cdmManifest.entities), 1)
        self.assertEqual(cdmManifest.entities[0].object_type, CdmObjectType.LOCAL_ENTITY_DECLARATION_DEF)
        entity = cdmManifest.entities[0]
        self.assertEqual(len(entity.data_partition_patterns), 1)
        pattern = entity.data_partition_patterns[0]
        self.assertEqual(pattern.name, "testPattern")
        self.assertEqual(pattern.explanation, "test explanation")
        self.assertEqual(pattern.root_location, "test location")
        self.assertEqual(pattern.regular_expression, "\\s*")
        self.assertEqual(len(pattern.parameters), 2)
        self.assertEqual(pattern.parameters[0], "testParam1")
        self.assertEqual(pattern.parameters[1], "testParam2")
        self.assertEqual(pattern.specialized_schema, "test special schema")
        self.assertEqual(len(pattern.exhibits_traits), 1)
    