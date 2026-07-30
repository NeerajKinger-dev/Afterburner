#!/usr/bin/env python3
"""
Unit tests for Afterburner v2.1 CorelDRAW Interoperable Export extension.
Verifies SVG document normalization, physical unit scaling, text node targeting, and multi-page extraction.
"""

import sys
import os
import unittest
import tempfile
import xml.etree.ElementTree as ET

# Add config-payload/inkscape/extensions to python path for importing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../config-payload/inkscape/extensions')))

from export_corel_interop import CorelInteropExporter, NAMESPACES


class TestCorelInteropExporter(unittest.TestCase):

    def setUp(self):
        self.exporter = CorelInteropExporter(
            font_strategy="path",
            dpi_normalization=True,
            export_format="pdf",
            export_multipage=True
        )

    def create_mock_svg(self, width="800px", height="600px", with_text=True, with_pages=True):
        """Create mock SVG root element."""
        svg_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
     width="{width}" height="{height}">
  <sodipodi:namedview id="namedview1">
"""
        if with_pages:
            svg_xml += """
    <inkscape:page id="page1" x="0" y="0" width="800" height="600" label="Cover Page" />
    <inkscape:page id="page2" x="820" y="0" width="800" height="600" label="Back Page" />
"""
        svg_xml += """
  </sodipodi:namedview>
  <g inkscape:groupmode="layer" inkscape:label="Layer 1">
    <rect x="10" y="10" width="200" height="100" fill="red" />
"""
        if with_text:
            svg_xml += """
    <text x="50" y="50" font-family="Arial" font-size="24">
      <tspan x="50" y="50">CorelDRAW Export Test</tspan>
    </text>
"""
        svg_xml += """
  </g>
</svg>
"""
        return ET.fromstring(svg_content if 'svg_content' in locals() else svg_xml)

    def test_unit_conversions(self):
        """Test pixel to mm conversions."""
        mm = CorelInteropExporter.px_to_mm(377.9527559055118)
        self.assertAlmostEqual(mm, 100.0, places=2)

    def test_viewport_normalization(self):
        """Test viewport normalization to physical millimeters (mm)."""
        root = self.create_mock_svg(width="800px", height="600px")
        w_mm, h_mm = self.exporter.normalize_viewport_units(root)

        self.assertTrue(root.get('width').endswith('mm'))
        self.assertTrue(root.get('height').endswith('mm'))
        self.assertEqual(root.get('viewBox'), "0 0 800.0000 600.0000")

    def test_text_to_path_targeting(self):
        """Test targeting and annotation of text nodes for outline conversion."""
        root = self.create_mock_svg(with_text=True)
        count = self.exporter.convert_text_to_vector_paths(root)
        self.assertEqual(count, 2, "Expected 2 text/tspan nodes targeted for path conversion")

    def test_extract_inkscape_pages(self):
        """Test extraction of Inkscape 1.2+ multi-page boundaries."""
        root = self.create_mock_svg(with_pages=True)
        pages = self.exporter.extract_inkscape_pages(root)

        self.assertEqual(len(pages), 2, "Expected 2 pages extracted")
        self.assertEqual(pages[0]['label'], "Cover Page")
        self.assertEqual(pages[1]['label'], "Back Page")
        self.assertEqual(pages[1]['x'], 820.0)


if __name__ == "__main__":
    unittest.main()
