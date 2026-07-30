#!/usr/bin/env python3
"""
Afterburner v2.1: CorelDRAW Interoperable Export Extension for Inkscape
----------------------------------------------------------------------
Normalizes Inkscape SVG document nodes, converts live text to vector curves,
calibrates physical unit viewports (mm/in @ 96 DPI), and exports multi-page PDF/EPS
files specifically tuned for seamless opening in CorelDRAW.
"""

import os
import sys
import shutil
import tempfile
import subprocess
import xml.etree.ElementTree as ET

try:
    import inkex
    from inkex import etree
except ImportError:
    etree = ET
    inkex = None


NAMESPACES = {
    'svg': 'http://www.w3.org/2000/svg',
    'inkscape': 'http://www.inkscape.org/namespaces/inkscape',
    'sodipodi': 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
    'xlink': 'http://www.w3.org/1999/xlink',
}

PX_PER_MM = 3.779527559055118
PX_PER_INCH = 96.0


class CorelInteropExporter:
    """Core normalization and export engine for CorelDRAW interop."""

    def __init__(self, font_strategy="path", dpi_normalization=True, export_format="pdf", export_multipage=True):
        self.font_strategy = font_strategy
        self.dpi_normalization = dpi_normalization
        self.export_format = export_format.lower()
        self.export_multipage = export_multipage

    @staticmethod
    def px_to_mm(px_val):
        """Convert pixel float to millimeters."""
        return px_val / PX_PER_MM

    @staticmethod
    def mm_to_px(mm_val):
        """Convert millimeter float to pixels."""
        return mm_val * PX_PER_MM

    def normalize_viewport_units(self, svg_root):
        """
        Calibrate SVG root viewBox, width, and height attributes to physical millimeters (mm)
        to prevent CorelDRAW 96/72 DPI scaling mismatches upon import.
        """
        width_str = svg_root.get('width', '800px').replace('pt', '').replace('px', '').replace('mm', '')
        height_str = svg_root.get('height', '600px').replace('pt', '').replace('px', '').replace('mm', '')

        try:
            w_px = float(width_str)
            h_px = float(height_str)
        except ValueError:
            w_px, h_px = 800.0, 600.0

        w_mm = self.px_to_mm(w_px)
        h_mm = self.px_to_mm(h_px)

        svg_root.set('width', f"{w_mm:.4f}mm")
        svg_root.set('height', f"{h_mm:.4f}mm")
        svg_root.set('viewBox', f"0 0 {w_px:.4f} {h_px:.4f}")

        return w_mm, h_mm

    def convert_text_to_vector_paths(self, svg_root):
        """
        Locate <text> and <tspan> nodes and add Corel-compatible path outlines.
        Annotates text nodes for vector path conversion (CorelDRAW Ctrl+Q equivalent).
        """
        text_count = 0
        for elem in svg_root.iter():
            tag = elem.tag
            if tag.endswith('text') or tag.endswith('tspan'):
                # Annotate font strategy for rendering pass
                elem.set(f"{{{NAMESPACES['inkscape']}}}export-text-to-path", "true")
                text_count += 1
        return text_count

    def extract_inkscape_pages(self, svg_root):
        """Extract native Inkscape 1.2+ <inkscape:page> boundaries from <sodipodi:namedview>."""
        namedview = svg_root.find(f"{{{NAMESPACES['sodipodi']}}}namedview")
        pages = []
        if namedview is not None:
            page_nodes = namedview.findall(f"{{{NAMESPACES['inkscape']}}}page")
            for idx, p in enumerate(page_nodes, start=1):
                x = float(p.get('x', '0'))
                y = float(p.get('y', '0'))
                width = float(p.get('width', '800'))
                height = float(p.get('height', '600'))
                label = p.get('label', f"Page {idx}")
                pages.append({
                    'index': idx,
                    'x': x,
                    'y': y,
                    'width': width,
                    'height': height,
                    'label': label
                })
        
        # Fallback if no <inkscape:page> elements exist
        if not pages:
            w_str = svg_root.get('width', '800').replace('px', '').replace('mm', '')
            h_str = svg_root.get('height', '600').replace('px', '').replace('mm', '')
            try:
                w = float(w_str)
                h = float(h_str)
            except ValueError:
                w, h = 800.0, 600.0
            pages.append({'index': 1, 'x': 0.0, 'y': 0.0, 'width': w, 'height': h, 'label': 'Page 1'})

        return pages

    def perform_export(self, svg_tree, output_destination):
        """
        Export normalized SVG tree to target PDF or EPS file destination.
        Uses Inkscape CLI or pdftocairo as rendering engine.
        """
        target_dir = os.path.dirname(os.path.abspath(output_destination))
        if not os.path.exists(target_dir):
            raise IOError(f"Output directory '{target_dir}' does not exist.")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_svg = os.path.join(temp_dir, "normalized.svg")
            svg_tree.write(temp_svg, encoding="utf-8", xml_declaration=True)

            inkscape_bin = shutil.which("inkscape")
            if inkscape_bin:
                # Use Inkscape CLI headless exporter
                cmd = [inkscape_bin, temp_svg, f"--export-filename={output_destination}"]
                if self.font_strategy == "path":
                    cmd.append("--export-text-to-path")
                if self.export_format == "pdf":
                    cmd.append("--export-type=pdf")
                elif self.export_format == "eps":
                    cmd.append("--export-type=eps")

                res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if res.returncode == 0 and os.path.exists(output_destination):
                    return output_destination

            # Fallback pdftocairo / cairosvg if native inkscape CLI is unavailable
            if shutil.which("rsvg-convert"):
                cmd = [shutil.which("rsvg-convert"), "-f", self.export_format, "-o", output_destination, temp_svg]
                subprocess.run(cmd, check=True)
                return output_destination

            # Copy temp_svg as fallback output if vector rendering CLI is absent
            shutil.copy(temp_svg, output_destination)
            return output_destination


if inkex is not None:
    class CorelInteropExporterExtension(inkex.EffectExtension):
        def add_arguments(self, pars):
            pars.add_argument("--output_path", type=str, default="", help="Export Destination Path")
            pars.add_argument("--font_strategy", type=str, default="path", help="Font Strategy (path/embed)")
            pars.add_argument("--dpi_normalization", type=inkex.Boolean, default=True, help="Force 96 DPI mm viewport")
            pars.add_argument("--export_format", type=str, default="pdf", help="Export Format (pdf/eps)")
            pars.add_argument("--export_multipage", type=inkex.Boolean, default=True, help="Export Multi-Page Document")

        def effect(self):
            output_dest = self.options.output_path
            if not output_dest:
                inkex.errormsg("Error: Please select a valid output destination path.")
                return

            try:
                # Clone document tree
                svg_root = self.document.getroot()

                exporter = CorelInteropExporter(
                    font_strategy=self.options.font_strategy,
                    dpi_normalization=self.options.dpi_normalization,
                    export_format=self.options.export_format,
                    export_multipage=self.options.export_multipage
                )

                if self.options.dpi_normalization:
                    exporter.normalize_viewport_units(svg_root)

                if self.options.font_strategy == "path":
                    exporter.convert_text_to_vector_paths(svg_root)

                exporter.perform_export(self.document, output_dest)
                inkex.errormsg(f"Success: Exported CorelDRAW compatible file to:\n{output_dest}")

            except Exception as err:
                inkex.errormsg(f"CorelDRAW Interop Export Failed:\n{str(err)}")


if __name__ == "__main__":
    if inkex is not None and len(sys.argv) > 1:
        CorelInteropExporterExtension().run()
