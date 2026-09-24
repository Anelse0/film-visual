"""Deterministic checks only; behavior and aesthetics require recorded agent runs."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TEST_TMP = Path(os.environ.get("FILM_VISUAL_TEST_TMP", tempfile.gettempdir()))


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


patcher = module("replace_visual")
installer = module("install")
counter = module("check_mj_prompt")


def plan_for(data, pairs):
    return {"sha256": hashlib.sha256(data).hexdigest(), "edits": [
        {"start": data.index(old), "end": data.index(old) + len(old),
         "old_hex": old.hex(), "new_hex": new.hex()} for old, new in pairs]}


class Contract(unittest.TestCase):
    def test_entry_and_local_links(self):
        text = (ROOT / "SKILL.md").read_text()
        front = text.split("---", 2)[1]
        self.assertEqual(re.search(r"^name: (.+)$", front, re.M)[1], ROOT.name)
        self.assertRegex(front, r"description: .+")
        for file in ROOT.rglob("*.md"):
            for link in re.findall(r"\]\(([^)]+)\)", file.read_text()):
                if link.startswith(("https://", "#")):
                    continue
                target = (file.parent / link.split("#")[0]).resolve()
                self.assertIn(ROOT, target.parents, f"external runtime link: {file}: {link}")
                self.assertTrue(target.is_file(), link)

    def test_self_containment_and_project_defaults(self):
        for file in ROOT.rglob("*"):
            self.assertFalse(file.is_symlink(), file)
        runtime = [ROOT / "SKILL.md", *ROOT.glob("references/*.md"), *ROOT.glob("templates/*.md")]
        for file in runtime:
            content = file.read_text()
            for forbidden in ("Noah", "Mason", "Reckless_Rivals", "RR_library", "02_pard", "/Users/", "/home/", "project_check.py", "route_check.py", "../film-director", "../film-creative"):
                self.assertNotIn(forbidden, content, file)
        # Imports are limited to the standard library; never import external Skill code.
        import ast
        allowed = {"argparse", "hashlib", "json", "pathlib", "re", "shutil", "tempfile"}
        for file in ROOT.glob("scripts/*.py"):
            for node in ast.walk(ast.parse(file.read_text())):
                if isinstance(node, ast.Import):
                    self.assertTrue(all(n.name.split('.')[0] in allowed for n in node.names), file)
                elif isinstance(node, ast.ImportFrom):
                    self.assertIn(node.module.split('.')[0], allowed, file)

    def test_templates_unapproved_by_default(self):
        # Checks scaffold defaults only, not whether a real approval is truthful.
        for file in ROOT.glob("templates/*.md"):
            content = file.read_text()
            self.assertIn("提案", content)
            self.assertIn("证据", content)
            self.assertIn("待测", content)
            self.assertNotRegex(content, r"状态[：:]\s*(已采用|已验收)")
            self.assertEqual(content.count("{{"), content.count("}}"))


class PromptBudget(unittest.TestCase):
    def test_urls_and_parameter_tail_are_excluded(self):
        prompt = 'https://example.invalid/ref.png?x=12 Eye-level gray T-shirt, soft light --ar 2:3 --no hanger, mannequin'
        result = counter.measure(prompt)
        self.assertEqual(result['body_words'], 5)
        self.assertTrue(result['parameter_tail_present'])

    def test_quoted_display_text_is_counted_not_parsed_as_parameters(self):
        prompt = 'A sign reading "--no entry" beside a gate --ar 16:9'
        self.assertEqual(counter.measure(prompt)['body_words'], 8)
        self.assertEqual(counter.split_body(prompt)[1], '--ar 16:9')
        self.assertEqual(counter.measure('A sign reading "say \\"hello\\""')['body_words'], 5)

    def test_soft_budget_does_not_truncate_or_impose_minimum(self):
        prompt = ' '.join(['gray'] * 51)
        self.assertTrue(counter.measure(prompt, 'simple')['over_soft_budget'])
        self.assertEqual(counter.measure(prompt, 'simple')['body_words'], 51)
        self.assertIsNone(counter.measure(prompt, 'simple')['within_user_limit'])
        self.assertFalse(counter.measure('Gray shirt', 'simple')['over_soft_budget'])

    def test_non_english_is_not_reported_as_zero_word_success(self):
        result = counter.measure('灰色训练服 gray shirt --ar 2:3')
        self.assertFalse(result['word_budget_applicable'])
        self.assertIsNone(result['body_words'])
        self.assertIsNone(result['over_soft_budget'])
        with self.assertRaises(ValueError):
            counter.measure('灰色训练服', max_words=50)

    def test_ambiguous_input_and_invalid_limit_rejected(self):
        for prompt in ['', '--ar 16:9', '```text\ngray shirt\n```', 'A sign reading "hello']:
            with self.subTest(prompt=prompt), self.assertRaises(ValueError):
                counter.measure(prompt)
        for limit in [0, -1, True, 3.5]:
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                counter.measure('Gray shirt', max_words=limit)

    def test_cli_hard_limit_exit_status_and_read_only_file(self):
        with tempfile.TemporaryDirectory(dir=TEST_TMP) as tmp:
            source = Path(tmp) / 'prompt.txt'
            original = b'\xef\xbb\xbfGray shirt\r\n--ar 2:3\r\n'
            source.write_bytes(original)
            cmd = [sys.executable, '-B', str(ROOT/'scripts/check_mj_prompt.py'), '--input', str(source)]
            for limit, status in [(2, 0), (1, 1)]:
                result = subprocess.run(cmd + ['--max-words', str(limit)], capture_output=True)
                self.assertEqual(result.returncode, status, result.stderr)
                self.assertEqual(json.loads(result.stdout)['body_words'], 2)
                self.assertEqual(source.read_bytes(), original)
            self.assertEqual(list(Path(tmp).iterdir()), [source])


class ByteReplacement(unittest.TestCase):
    def test_utf8_bom_mixed_newlines_dialogue_and_multiple_spans(self):
        data = b'\xef\xbb\xbf' + '9秒\r\nLOOK\r\n旧光。\n镜1 0—3秒\r\n甲：“不要走。”  \r\n动作：停下\n声音：雨\r\n反射：过强。\r\n'.encode()
        pairs = [('旧光。'.encode(), '中性光，暗侧可读。'.encode()), ('过强。'.encode(), b'')]
        plan = plan_for(data, pairs)
        out = patcher.apply_patch_bytes(data, plan)
        expected = data.replace(pairs[0][0], pairs[0][1]).replace(pairs[1][0], b'')
        self.assertEqual(out, expected)

    def test_other_encodings_preserved(self):
        data = 'LOOK\r\n旧光\r\n对白原文'.encode('utf-16')
        old, new = '旧光'.encode('utf-16-le'), '新光'.encode('utf-16-le')
        self.assertEqual(patcher.apply_patch_bytes(data, plan_for(data, [(old, new)])), data.replace(old, new))

    def test_stale_input_and_wrong_selected_bytes_fail(self):
        data = b'prefix LOOK old suffix'
        plan = plan_for(data, [(b'old', b'new')])
        with self.assertRaises(ValueError):
            patcher.apply_patch_bytes(data + b'!', plan)
        plan['edits'][0]['old_hex'] = b'BAD'.hex()
        with self.assertRaises(ValueError):
            patcher.apply_patch_bytes(data, plan)

    def test_ranges_fail_closed(self):
        data = b'abcdef'
        cases = [[], [{'start': -1, 'end': 2, 'old_hex': '', 'new_hex': ''}],
                 [{'start': True, 'end': 2, 'old_hex': '62', 'new_hex': ''}],
                 [{'start': 2, 'end': 2, 'old_hex': '', 'new_hex': ''}],
                 [{'start': 0, 'end': 7, 'old_hex': data.hex(), 'new_hex': ''}]]
        overlap = plan_for(data, [(b'abc', b'x'), (b'bc', b'y')])
        cases.append(overlap['edits'])
        for edits in cases:
            with self.subTest(edits=edits), self.assertRaises(ValueError):
                patcher.apply_patch_bytes(data, {'sha256': patcher.sha256(data), 'edits': edits})

    def test_cli_preserves_source_refuses_overwrite_and_symlink(self):
        with tempfile.TemporaryDirectory(dir=TEST_TMP) as tmp:
            base = Path(tmp)
            src, patch, out = base/'in.txt', base/'patch.json', base/'out.txt'
            src.write_bytes(b'prefix OLD suffix\r\n')
            patch.write_text(json.dumps(plan_for(src.read_bytes(), [(b'OLD', b'NEW')])) )
            cmd = [sys.executable, '-B', str(ROOT/'scripts/replace_visual.py'), '--input', str(src), '--patch', str(patch)]
            checked = subprocess.run(cmd + ['--check'], capture_output=True)
            self.assertEqual(checked.returncode, 0, checked.stderr)
            self.assertFalse(out.exists())
            written = subprocess.run(cmd + ['--output', str(out)], capture_output=True)
            self.assertEqual(written.returncode, 0, written.stderr)
            self.assertEqual(out.read_bytes(), b'prefix NEW suffix\r\n')
            self.assertEqual(src.read_bytes(), b'prefix OLD suffix\r\n')
            self.assertEqual(subprocess.run(cmd + ['--output', str(out)], capture_output=True).returncode, 2)
            link = base/'link.txt'
            link.symlink_to(src)
            self.assertEqual(subprocess.run(cmd + ['--output', str(link)], capture_output=True).returncode, 2)


class Installation(unittest.TestCase):
    def test_local_install_and_existing_work_protected(self):
        with tempfile.TemporaryDirectory(dir=TEST_TMP) as tmp:
            target = installer.install(ROOT, Path(tmp))
            self.assertEqual((target/'SKILL.md').read_bytes(), (ROOT/'SKILL.md').read_bytes())
            (target/'user-edit.txt').write_text('keep')
            with self.assertRaises(FileExistsError):
                installer.install(ROOT, Path(tmp))
            self.assertEqual((target/'user-edit.txt').read_text(), 'keep')

    def test_linked_install_parent_rejected(self):
        with tempfile.TemporaryDirectory(dir=TEST_TMP) as tmp:
            base = Path(tmp)
            project, outside = base/'project', base/'outside'
            project.mkdir()
            outside.mkdir()
            (project/'.agents').symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                installer.install(ROOT, project)
            self.assertEqual(list(outside.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
