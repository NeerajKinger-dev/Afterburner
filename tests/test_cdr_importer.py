#!/usr/bin/env python3
"""
Unit tests for Afterburner v2.0 Multi-Page CorelDRAW (.cdr) Importer extension.
Verifies SVG DOM manipulation, <inkscape:page> node creation, and offset calculation.
"""

import sys
import os
import unittest
import tempfile
import xml.etree.ElementTree as ET

# Add config-payload/inkscape/extensions to python path for importing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../config-payload/inkscape/extensions')))

from cdr_multipage_importer import CdrMultiPageImporter, NAMESPACES


class TestCdrMultiPageImporter(unittest.TestCase):

    def setUp(self):
        self.importer = CdrMultiPageImporter(target_dpi=300, page_margin=20.0, extract_multipage=True)
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_mock_svg_page(self, filename, width=800, height=600, circle_color="red"):
        """Create a mock SVG page file."""
        filepath = os.path.join(self.temp_dir.name, filename)
        svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}px" height="{height}px" viewBox="0 0 {width} {height}">
  <rect width="{width}" height="{height}" fill="white" />
  <circle cx="100" cy="100" r="50" fill="{circle_color}" />
</svg>
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(svg_content)
        return filepath

    def test_dependency_check(self):
        """Test system dependency checker function."""
        missing = CdrMultiPageImporter.check_system_dependencies()
        self.assertIsInstance(missing, list)

    def test_multipage_svg_dom_reconstruction(self):
        """Verify that multi-page SVG DOM nodes (<inkscape:page> in <sodipodi:namedview>) are created properly."""
        page1 = self.create_mock_svg_page("page1.svg", width=800, height=600, circle_color="red")
        page2 = self.create_mock_svg_page("page2.svg", width=800, height=600, circle_color="blue")
        page3 = self.create_mock_svg_page("page3.svg", width=800, height=600, circle_color="green")

        svg_files = [page1, page2, page3]
        root_element = self.importer.build_multipage_svg(svg_files)

        # Check <sodipodi:namedview>
        namedview = root_element.find(f"{{{NAMESPACES['sodipodi']}}}namedview")
        self.assertIsNotNone(namedview, "sodipodi:namedview element must be present in SVG root")

        # Check <inkscape:page> elements
        pages = namedview.findall(f"{{{NAMESPACES['inkscape']}}}page")
        self.assertEqual(len(pages), 3, "Expected 3 <inkscape:page> elements for 3 extracted pages")

        # Verify page 1 coordinates
        self.assertEqual(pages[0].get('x'), '0.0')
        self.assertEqual(pages[0].get('width'), '800.0')
        self.assertEqual(pages[0].get('label'), 'Page 1')

        # Verify page 2 coordinates (800 + margin 20 = 820.0)
        self.assertEqual(pages[1].get('x'), '820.0')
        self.assertEqual(pages[1].get('width'), '800.0')
        self.assertEqual(pages[1].get('label'), 'Page 2')

        # Verify page 3 coordinates (820 + 800 + margin 20 = 1640.0)
        self.assertEqual(pages[2].get('x'), '1640.0')
        self.assertEqual(pages[2].get('width'), '800.0')
        self.assertEqual(pages[2].get('label'), 'Page 3')

        # Check Layer Groups
        layers = root_element.findall(f"{{{NAMESPACES['svg']}}}g")
        page_layers = [l for l in layers if l.get(f"{{{NAMESPACES['inkscape']}}}groupmode") == 'layer']
        self.assertEqual(len(page_layers), 3, "Expected 3 layer groups for extracted page content")

        self.assertEqual(page_layers[0].get(f"{{{NAMESPACES['inkscape']}}}label"), "Page 1 Content")
        self.assertEqual(page_layers[0].get("transform"), "translate(0.0, 0)")

        self.assertEqual(page_layers[1].get(f"{{{NAMESPACES['inkscape']}}}label"), "Page 2 Content")
        self.assertEqual(page_layers[1].get("transform"), "translate(820.0, 0)")

        self.assertEqual(page_layers[2].get(f"{{{NAMESPACES['inkscape']}}}label"), "Page 3 Content")
        self.assertEqual(page_layers[2].get("transform"), "translate(1640.0, 0)")


if __name__ == "__main__":
    unittest.main()
