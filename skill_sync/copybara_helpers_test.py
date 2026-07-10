"""Unit tests for Copybara Starlark helper functions in copybara_helpers.bara.sky."""

import fnmatch
import unittest


class MockObject:

  def __init__(self, *args, **kwargs):
    pass

  def __getattr__(self, name):
    return MockObject()

  def __call__(self, *args, **kwargs):
    return MockObject()

  def __add__(self, other):
    return MockObject()

  def __radd__(self, other):
    return MockObject()


class MockGlob:

  def __init__(self, include, exclude=None):
    self.include = include
    self.exclude = exclude


class DynamicTransformMock:

  def __init__(self, impl):
    self.impl = impl


class MockDestinationReader:

  def __init__(self, files_dict):
    self.files_dict = files_dict
    self.copied = []

  def file_exists(self, path):
    return path in self.files_dict

  def copy_destination_files(self, glob_obj):
    if isinstance(glob_obj, MockGlob):
      self.copied.extend(glob_obj.include)
    else:
      self.copied.append(glob_obj)


class MockFile:

  def __init__(self, path):
    self.path = path


class MockBuildozerModify:

  def __init__(self, target, commands):
    self.target = target
    self.commands = commands


class MockBuildozer:

  def modify(self, target, commands):
    return MockBuildozerModify(target, commands)


class MockCoreMove:

  def __init__(self, before, after):
    self.before = before
    self.after = after


class MockCtx:

  def __init__(self, files_dict):
    self.files_dict = files_dict
    self.files = [MockFile(path) for path in files_dict.keys()]
    self.written = {}
    self.buildozer_calls = []
    self._destination_reader = MockDestinationReader(files_dict)

  def destination_reader(self):
    return self._destination_reader

  def run(self, arg):
    if isinstance(arg, MockGlob):
      matched = []
      for f in self.files:
        for pattern in arg.include:
          match_pattern = pattern.replace("**/", "*").replace("**", "*")
          if fnmatch.fnmatch(f.path, match_pattern):
            matched.append(f)
            break
      return matched
    elif isinstance(arg, MockBuildozerModify):
      self.buildozer_calls.append(arg)
      return []
    elif isinstance(arg, DynamicTransformMock):
      arg.impl(self)
      return []
    elif isinstance(arg, MockCoreMove):
      # Perform moving/renaming on mock files
      src_prefix = arg.before + "/" if arg.before else ""
      dest_prefix = arg.after + "/" if arg.after else ""

      new_files_dict = {}
      for path, content in list(self.files_dict.items()):
        if path.startswith(src_prefix):
          rel_path = path[len(src_prefix):]
          new_path = dest_prefix + rel_path
          new_files_dict[new_path] = content
        else:
          new_files_dict[path] = content
      self.files_dict.clear()
      self.files_dict.update(new_files_dict)
      self.files = [MockFile(path) for path in self.files_dict.keys()]
      return []
    return self.files

  def read_path(self, f):
    path = f if isinstance(f, str) else f.path
    return self.files_dict[path]

  def write_path(self, f, content):
    path = f if isinstance(f, str) else f.path
    self.files_dict[path] = content
    self.written[path] = content

  def new_path(self, path):
    return path

  def success(self):
    return "SUCCESS"


class CopybaraHelpersTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    # Read copybara_helpers.bara.sky and extract helper functions using exec()
    with open(
        "third_party/data_agent_kit/data_agent_common/skill_sync/copybara_helpers.bara.sky",
        "r",
        encoding="utf-8",
    ) as f:
      content = f.read()

    class MockCore:

      def __init__(self):
        self.last_workflow_args = None

      def workflow(self, **kwargs):
        self.last_workflow_args = kwargs
        return MockObject()

      def dynamic_transform(self, impl):
        return DynamicTransformMock(impl)

      def move(self, before, after):
        return MockCoreMove(before, after)

      def __getattr__(self, name):
        return MockObject()

    cls.mock_core = MockCore()

    def starlark_fail(msg):
      raise ValueError(msg)

    globals_dict = {
        "load": lambda *args, **kwargs: None,
        "glob": lambda include, exclude=None: MockGlob(include, exclude),
        "core": cls.mock_core,
        "buildozer": MockBuildozer(),
        "metadata": MockObject(),
        "git": MockObject(),
        "service": MockObject(),
        "piper": MockObject(),
        "authoring": MockObject(),
        "leakr": MockObject(),
        "fail": starlark_fail,
    }
    # pylint: disable=exec-used
    exec(content, globals_dict)

    # Extract the helper functions for testing
    cls._dak_skills_sync_workflow = staticmethod(
        globals_dict["dak_skills_sync_workflow"]
    )
    def add_license_headers_mock(ctx, skill_path):
      transform = globals_dict["_add_license_headers"](skill_path)
      transform.impl(ctx)
    cls._add_license_headers_mock = staticmethod(add_license_headers_mock)
    def clean_frontmatter_transform_mock(ctx, skill_path):
      transform = globals_dict["_clean_frontmatter_transform"](skill_path)
      transform.impl(ctx)
    cls._clean_frontmatter_transform_mock = staticmethod(
        clean_frontmatter_transform_mock
    )
    cls.STATIC_CHECKS = globals_dict["STATIC_CHECKS"]

    cls._generate_license = staticmethod(globals_dict["_generate_license"])
    cls.PY_LICENSE = cls._generate_license("#")
    cls.JS_LICENSE = cls._generate_license("//")

  def _clean_frontmatter_at_path(self, ctx, file_path):
    parts = file_path.split("/")
    skill_path = "/".join(parts[:-1]) if len(parts) > 1 else "."
    self._clean_frontmatter_transform_mock(ctx, skill_path)

  def test_add_license_headers_prepends_when_missing(self):
    # File has no license header
    ctx = MockCtx({"scripts/test.py": "def hello():\n    print('hello')\n"})
    self._add_license_headers_mock(ctx, "scripts")

    self.assertIn("scripts/test.py", ctx.written)
    self.assertEqual(
        ctx.written["scripts/test.py"],
        self.PY_LICENSE + "def hello():\n    print('hello')\n",
    )

  def test_add_license_headers_does_nothing_if_header_exists(self):
    # File already has Copyright notice
    content = "# Copyright 2026 Google LLC\ndef hello():\n    print('hello')\n"
    ctx = MockCtx({"scripts/test.py": content})
    self._add_license_headers_mock(ctx, "scripts")

    self.assertEqual(ctx.written, {})

  def test_add_license_headers_preserves_shebang(self):
    # File has shebang at the top
    ctx = MockCtx({
        "scripts/test.py": (
            "#!/usr/bin/env python3\ndef hello():\n    print('hello')\n"
        )
    })
    self._add_license_headers_mock(ctx, "scripts")

    self.assertIn("scripts/test.py", ctx.written)
    self.assertEqual(
        ctx.written["scripts/test.py"],
        "#!/usr/bin/env python3\n"
        + self.PY_LICENSE
        + "def hello():\n    print('hello')\n",
    )

  def test_add_license_headers_prepends_js_when_missing(self):
    # JS file has no license header
    ctx = MockCtx({"scripts/test.js": "console.log('hello');\n"})
    self._add_license_headers_mock(ctx, "scripts")

    self.assertIn("scripts/test.js", ctx.written)
    self.assertEqual(
        ctx.written["scripts/test.js"],
        self.JS_LICENSE + "console.log('hello');\n",
    )

  def test_add_license_headers_does_nothing_if_js_header_exists(self):
    # JS file already has Copyright notice
    content = "// Copyright 2026 Google LLC\nconsole.log('hello');\n"
    ctx = MockCtx({"scripts/test.js": content})
    self._add_license_headers_mock(ctx, "scripts")

    self.assertEqual(ctx.written, {})

  def test_add_license_headers_preserves_js_shebang(self):
    # JS file has shebang at the top
    ctx = MockCtx(
        {"scripts/test.js": "#!/usr/bin/env node\nconsole.log('hello');\n"}
    )
    self._add_license_headers_mock(ctx, "scripts")

    self.assertIn("scripts/test.js", ctx.written)
    self.assertEqual(
        ctx.written["scripts/test.js"],
        "#!/usr/bin/env node\n" + self.JS_LICENSE + "console.log('hello');\n",
    )

  def test_clean_skill_metadata_adds_missing_license_and_metadata(self):
    # SKILL.md without license or metadata blocks
    input_content = """---
name: my_skill
description: simple skill
---
Some body text
"""
    ctx = MockCtx({"my_skill/SKILL.md": input_content})
    self._clean_frontmatter_at_path(ctx, "my_skill/SKILL.md")

    self.assertIn("my_skill/SKILL.md", ctx.written)
    expected_frontmatter = (
        "---\n"
        "name: my_skill\n"
        "description: simple skill\n"
        "metadata:\n"
        "  version: v1\n"
        "  publisher: google\n"
        "license: Apache-2.0\n"
        "---\n"
    )
    self.assertTrue(
        ctx.written["my_skill/SKILL.md"].startswith(expected_frontmatter)
    )
    self.assertTrue(
        ctx.written["my_skill/SKILL.md"].endswith("Some body text\n")
    )

  def test_clean_skill_metadata_standardizes_and_preserves_custom_fields(self):
    # SKILL.md with custom fields in metadata and old values
    input_content = """---
name: my_skill
license: old-license
metadata:
  custom_field: custom-value
  publisher: old-publisher
---
Some body text
"""
    ctx = MockCtx({"my_skill/SKILL.md": input_content})
    self._clean_frontmatter_at_path(ctx, "my_skill/SKILL.md")

    self.assertIn("my_skill/SKILL.md", ctx.written)
    expected_frontmatter = (
        "---\n"
        "name: my_skill\n"
        "metadata:\n"
        "  custom_field: custom-value\n"
        "  publisher: google\n"
        "  version: v1\n"
        "license: Apache-2.0\n"
        "---\n"
    )
    self.assertEqual(
        ctx.written["my_skill/SKILL.md"][: len(expected_frontmatter)],
        expected_frontmatter,
    )
    self.assertTrue(
        ctx.written["my_skill/SKILL.md"].endswith("Some body text\n")
    )

  def test_clean_skill_metadata_empty_metadata_block(self):
    # metadata: block exists but is empty
    input_content = """---
name: my_skill
metadata:
---
Some body text
"""
    ctx = MockCtx({"my_skill/SKILL.md": input_content})
    self._clean_frontmatter_at_path(ctx, "my_skill/SKILL.md")

    self.assertIn("my_skill/SKILL.md", ctx.written)
    expected_frontmatter = (
        "---\n"
        "name: my_skill\n"
        "metadata:\n"
        "  version: v1\n"
        "  publisher: google\n"
        "license: Apache-2.0\n"
        "---\n"
    )
    self.assertTrue(
        ctx.written["my_skill/SKILL.md"].startswith(expected_frontmatter)
    )

  def test_clean_skill_metadata_partially_filled_metadata_version_only(self):
    # metadata block has version: v1 but lacks publisher
    input_content = """---
name: my_skill
metadata:
  version: v1
---
Some body text
"""
    ctx = MockCtx({"my_skill/SKILL.md": input_content})
    self._clean_frontmatter_at_path(ctx, "my_skill/SKILL.md")

    self.assertIn("my_skill/SKILL.md", ctx.written)
    expected_frontmatter = (
        "---\n"
        "name: my_skill\n"
        "metadata:\n"
        "  version: v1\n"
        "  publisher: google\n"
        "license: Apache-2.0\n"
        "---\n"
    )
    self.assertTrue(
        ctx.written["my_skill/SKILL.md"].startswith(expected_frontmatter)
    )

  def test_clean_skill_metadata_partially_filled_metadata_publisher_only(self):
    # metadata block has publisher but lacks version
    input_content = """---
name: my_skill
metadata:
  publisher: old-pub
---
Some body text
"""
    ctx = MockCtx({"my_skill/SKILL.md": input_content})
    self._clean_frontmatter_at_path(ctx, "my_skill/SKILL.md")

    self.assertIn("my_skill/SKILL.md", ctx.written)
    expected_frontmatter = (
        "---\n"
        "name: my_skill\n"
        "metadata:\n"
        "  publisher: google\n"
        "  version: v1\n"
        "license: Apache-2.0\n"
        "---\n"
    )
    self.assertTrue(
        ctx.written["my_skill/SKILL.md"].startswith(expected_frontmatter)
    )

  def test_clean_skill_metadata_already_correct_no_change(self):
    # metadata block and license are already fully correct and present
    input_content = """---
name: my_skill
metadata:
  version: v1
  publisher: google
license: Apache-2.0
---
Some body text
"""
    ctx = MockCtx({"my_skill/SKILL.md": input_content})
    self._clean_frontmatter_at_path(ctx, "my_skill/SKILL.md")

    self.assertIn("my_skill/SKILL.md", ctx.written)
    self.assertEqual(ctx.written["my_skill/SKILL.md"], input_content)

  def test_clean_skill_metadata_preserves_multiple_custom_metadata_fields(self):
    # metadata has multiple custom fields that must be preserved
    input_content = """---
name: my_skill
metadata:
  category: database
  publisher: old-pub
  tags:
    - spanner
    - sql
---
Some body text
"""
    ctx = MockCtx({"my_skill/SKILL.md": input_content})
    self._clean_frontmatter_at_path(ctx, "my_skill/SKILL.md")

    self.assertIn("my_skill/SKILL.md", ctx.written)
    expected_frontmatter = (
        "---\n"
        "name: my_skill\n"
        "metadata:\n"
        "  category: database\n"
        "  publisher: google\n"
        "  tags:\n"
        "    - spanner\n"
        "    - sql\n"
        "  version: v1\n"
        "license: Apache-2.0\n"
        "---\n"
    )
    self.assertTrue(
        ctx.written["my_skill/SKILL.md"].startswith(expected_frontmatter)
    )

  def test_clean_skill_metadata_preserves_custom_indentation(self):
    # metadata block has 4-space indentation for its children
    input_content = """---
name: my_skill
metadata:
    category: database
    publisher: old-pub
---
Some body text
"""
    ctx = MockCtx({"my_skill/SKILL.md": input_content})
    self._clean_frontmatter_at_path(ctx, "my_skill/SKILL.md")

    self.assertIn("my_skill/SKILL.md", ctx.written)
    expected_frontmatter = (
        "---\n"
        "name: my_skill\n"
        "metadata:\n"
        "    category: database\n"
        "    publisher: google\n"
        "    version: v1\n"
        "license: Apache-2.0\n"
        "---\n"
    )
    self.assertTrue(
        ctx.written["my_skill/SKILL.md"].startswith(expected_frontmatter)
    )

  def test_clean_skill_metadata_no_frontmatter_boundaries_does_nothing(self):
    # File has no --- yaml boundaries
    input_content = (
        "Some plain text skill description without yaml frontmatter.\n"
    )
    ctx = MockCtx({"my_skill/SKILL.md": input_content})
    self._clean_frontmatter_at_path(ctx, "my_skill/SKILL.md")

    # Should not write to file
    self.assertEqual(ctx.written, {})

  def test_clean_skill_metadata_strips_top_level_publisher_and_version(self):
    # publisher and version keys misplaced at the top level
    input_content = """---
name: my_skill
publisher: misplaced-pub
version: v2
---
Some body text
"""
    ctx = MockCtx({"my_skill/SKILL.md": input_content})
    self._clean_frontmatter_at_path(ctx, "my_skill/SKILL.md")

    self.assertIn("my_skill/SKILL.md", ctx.written)
    expected_frontmatter = (
        "---\n"
        "name: my_skill\n"
        "metadata:\n"
        "  version: v1\n"
        "  publisher: google\n"
        "license: Apache-2.0\n"
        "---\n"
    )
    self.assertTrue(
        ctx.written["my_skill/SKILL.md"].startswith(expected_frontmatter)
    )

  def test_clean_skill_metadata_empty_frontmatter_block(self):
    # A mostly empty frontmatter block
    input_content = """---
---
Some body text
"""
    ctx = MockCtx({"my_skill/SKILL.md": input_content})
    self._clean_frontmatter_at_path(ctx, "my_skill/SKILL.md")

    self.assertIn("my_skill/SKILL.md", ctx.written)
    expected_frontmatter = (
        "---\n"
        "metadata:\n"
        "  version: v1\n"
        "  publisher: google\n"
        "license: Apache-2.0\n"
        "---\n"
    )
    self.assertTrue(
        ctx.written["my_skill/SKILL.md"].startswith(expected_frontmatter)
    )

  def test_static_checks_contains_expected_transformations(self):
    # Verify that STATIC_CHECKS list has exactly the two validation checks.
    self.assertIsInstance(self.STATIC_CHECKS, list)
    self.assertEqual(len(self.STATIC_CHECKS), 2)

  def test_clean_frontmatter_transform_cleans_metadata(self):
    # Verify that the specific dynamic transform cleans frontmatter at destination
    dest_skill_path = "google3/third_party/data_agent_kit/data_agent_common/skills/gcs_security_assessment"
    dest_path = dest_skill_path + "/SKILL.md"
    ctx = MockCtx({
        dest_path: (
            "---\nname: gcs-security-assessment\ndescription: skill\n---\nbody"
        )
    })
    self._clean_frontmatter_transform_mock(ctx, dest_skill_path)

    self.assertIn(dest_path, ctx.written)
    content = ctx.written[dest_path]
    self.assertTrue(content.startswith("---\nname: gcs-security-assessment\n"))
    self.assertIn("license: Apache-2.0", content)

  def test_dak_skills_sync_workflow_executes_successfully(self):
    # 1. Define skills sync workflow.
    self._dak_skills_sync_workflow(
        origin_files=MockGlob(["skills/**"]),
        workflow_name="gcs_skills_sync",
        author="GCS Team <no-reply@google.com>",
        owner_mdb="daii-optimize-team",
        contact_email="gcs@google.com",
        destination_skills_globs=["gcs_**"],
    )

    # Verify workflow details were recorded correctly.
    self.assertIsNotNone(self.mock_core.last_workflow_args)
    args = self.mock_core.last_workflow_args
    self.assertEqual(args["name"], "gcs_skills_sync")

    # Find the dynamic transform.
    dyn_transform = None
    for t in args["transformations"]:
      if isinstance(t, DynamicTransformMock):
        dyn_transform = t
        break
    self.assertIsNotNone(dyn_transform, "Should contain a dynamic transform")

    # 2. Prepare mock workspace environment.
    files = {
        # Destination BUILD file to fetch and modify
        "google3/third_party/data_agent_kit/data_agent_common/skills/BUILD": (
            "# BUILD file contents"
        ),
        # Skills in the origin source path
        "gcs_security_assessment/SKILL.md": (
            "---\nname: gcs_security_assessment\ndescription: test skill\n---\nbody"
        ),
        "gcs_security_assessment/scripts/helper.py": (
            "def foo(): pass"
        ),
    }
    ctx = MockCtx(files)

    # 3. Execute the dynamic transform implementation!
    res = dyn_transform.impl(ctx)
    self.assertEqual(res, "SUCCESS")

    # 4. Assert files were moved to DAK skills path.
    self.assertIn(
        "google3/third_party/data_agent_kit/data_agent_common/skills/"
        "gcs_security_assessment/SKILL.md",
        ctx.files_dict,
    )
    self.assertIn(
        "google3/third_party/data_agent_kit/data_agent_common/skills/"
        "gcs_security_assessment/scripts/helper.py",
        ctx.files_dict,
    )

    # Assert original paths are removed (since they were moved).
    self.assertNotIn("gcs_security_assessment/SKILL.md", ctx.files_dict)

    # Assert buildozer.modify was called to register the skill.
    self.assertEqual(len(ctx.buildozer_calls), 1)
    call = ctx.buildozer_calls[0]
    self.assertEqual(
        call.target,
        "google3/third_party/data_agent_kit/data_agent_common/skills:"
        "%define_partner_skills",
    )
    self.assertEqual(call.commands, ["add skills gcs_security_assessment"])

    # Assert frontmatter cleaning was executed on SKILL.md.
    dest_skill_md = "google3/third_party/data_agent_kit/data_agent_common/skills/gcs_security_assessment/SKILL.md"
    self.assertIn(dest_skill_md, ctx.written)
    content = ctx.written[dest_skill_md]
    self.assertTrue(content.startswith("---\nname: gcs_security_assessment\n"))
    self.assertIn("license: Apache-2.0", content)

    # Assert license header was prepended to python files.
    dest_helper_py = "google3/third_party/data_agent_kit/data_agent_common/skills/gcs_security_assessment/scripts/helper.py"
    self.assertIn(dest_helper_py, ctx.written)
    self.assertTrue(ctx.written[dest_helper_py].startswith(self.PY_LICENSE))

  def test_dak_skills_sync_workflow_narrows_destination_files_glob(self):
    # Define a workflow with alloydb prefix glob
    self._dak_skills_sync_workflow(
        origin_files=MockGlob(["skills/**"]),
        workflow_name="alloydb_skills_sync",
        author="AlloyDB Team <no-reply@google.com>",
        owner_mdb="test-mdb",
        contact_email="alloydb@google.com",
        destination_skills_globs=["alloydb_postgres_**"],
    )

    args = self.mock_core.last_workflow_args
    self.assertIsNotNone(args)
    dest_files_glob = args["destination_files"]
    self.assertIsInstance(dest_files_glob, MockGlob)

    # Test file matching behavior
    def matches_glob(path, mock_glob):
      for pattern in mock_glob.include:
        match_pattern = pattern.replace("**/", "*").replace("**", "*")
        if fnmatch.fnmatch(path, match_pattern):
          return True
      return False

    # Should match AlloyDB skills
    self.assertTrue(matches_glob(
        "google3/third_party/data_agent_kit/data_agent_common/skills/alloydb_postgres_data/SKILL.md",
        dest_files_glob
    ))
    # Should match BUILD file
    self.assertTrue(matches_glob(
        "google3/third_party/data_agent_kit/data_agent_common/skills/BUILD",
        dest_files_glob
    ))

    # Should NOT match GCS skills
    self.assertFalse(matches_glob(
        "google3/third_party/data_agent_kit/data_agent_common/skills/gcs_security_assessment/SKILL.md",
        dest_files_glob
    ))


if __name__ == "__main__":
  unittest.main()
