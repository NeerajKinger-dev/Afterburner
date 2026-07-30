#!/usr/bin/env python3
"""
Afterburner v2.1: Multi-Page CorelDRAW (.cdr) Importer for Inkscape
------------------------------------------------------------------
Extracts multi-page CorelDRAW (.cdr) documents using libcdr-tools / LibreOffice / Inkscape,
splits pages cleanly, and constructs native Inkscape 1.2+ multi-page SVG DOM nodes
(<inkscape:page> in <sodipodi:namedview>).
"""

import os
import re
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

for prefix, uri in NAMESPACES.items():
    ET.register_namespace(prefix, uri)


def natural_sort_key(s):
    """Sort strings containing numbers in human/natural order (page1, page2, page10)."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]


class CdrMultiPageImporter:
    """Core logic for extracting multi-page CDR files and building Inkscape multi-page SVG DOM."""

    def __init__(self, target_dpi=300, page_margin=20.0, extract_multipage=True):
        self.target_dpi = target_dpi
        self.page_margin = page_margin
        self.extract_multipage = extract_multipage

    @staticmethod
    def check_system_dependencies():
        """Verify presence of conversion tools: soffice/libreoffice, cdr2xhtml, pdftocairo, or pdf2svg."""
        missing = []
        has_cdr_converter = False

        if shutil.which("soffice") or shutil.which("libreoffice") or shutil.which("unoconv") or shutil.which("inkscape"):
            has_cdr_converter = True
        elif shutil.which("cdr2xhtml") or shutil.which("cdr2raw"):
            has_cdr_converter = True

        if not has_cdr_converter:
            missing.append("libcdr-tools (cdr2xhtml/cdr2raw) or LibreOffice (soffice) or Inkscape CLI")

        has_pdf_splitter = False
        if shutil.which("pdftocairo") or shutil.which("pdf2svg") or shutil.which("inkscape"):
            has_pdf_splitter = True

        if not has_pdf_splitter:
            missing.append("pdftocairo (poppler-utils) or pdf2svg")

        return missing

    def convert_cdr_to_pdf(self, cdr_path, output_dir):
        """Convert .cdr file to intermediate multi-page PDF or HTML container."""
        errors = []

        # 1. Try LibreOffice / soffice / unoconv
        for cmd_name in ["soffice", "libreoffice", "unoconv"]:
            binary = shutil.which(cmd_name)
            if binary:
                cmd = [binary, "--headless", "--convert-to", "pdf", "--outdir", output_dir, cdr_path]
                result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if result.returncode == 0:
                    base_name = os.path.splitext(os.path.basename(cdr_path))[0]
                    pdf_path = os.path.join(output_dir, f"{base_name}.pdf")
                    if os.path.exists(pdf_path):
                        return pdf_path
                errors.append(f"{cmd_name} output: {result.stderr or result.stdout}")

        # 2. Try Inkscape CLI direct conversion
        inkscape_bin = shutil.which("inkscape")
        if inkscape_bin:
            base_name = os.path.splitext(os.path.basename(cdr_path))[0]
            pdf_path = os.path.join(output_dir, f"{base_name}.pdf")
            cmd = [inkscape_bin, cdr_path, f"--export-filename={pdf_path}", "--export-type=pdf"]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0 and os.path.exists(pdf_path):
                return pdf_path

        # 3. Fallback to cdr2xhtml
        if shutil.which("cdr2xhtml"):
            xhtml_path = os.path.join(output_dir, "output.html")
            cmd = ["cdr2xhtml", cdr_path, xhtml_path]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0 and os.path.exists(xhtml_path):
                svg_files = self._extract_svgs_from_html(xhtml_path, output_dir)
                if svg_files:
                    return xhtml_path

        raise RuntimeError("Failed to convert .cdr file. Diagnostics:\n" + "\n".join(errors))

    def _extract_svgs_from_html(self, html_path, output_dir):
        """Parse HTML file from cdr2xhtml and save individual embedded <svg> elements as SVG files."""
        extracted = []
        try:
            with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            svg_blocks = re.findall(r'(<svg.*?>.*?</svg>)', content, re.DOTALL | re.IGNORECASE)
            for idx, svg_code in enumerate(svg_blocks, start=1):
                page_file = os.path.join(output_dir, f"page_{idx:03d}.svg")
                with open(page_file, 'w', encoding='utf-8') as out_f:
                    out_f.write('<?xml version="1.0" encoding="UTF-8"?>\n' + svg_code)
                extracted.append(page_file)
        except Exception:
            pass
        return extracted

    def extract_pdf_pages_to_svg(self, input_container_path, output_dir):
        """Split multi-page PDF or HTML container into individual SVG files."""
        if input_container_path.endswith(".html") or input_container_path.endswith(".xhtml"):
            return self._extract_svgs_from_html(input_container_path, output_dir)

        if shutil.which("pdftocairo"):
            out_prefix = os.path.join(output_dir, "page")
            cmd = ["pdftocairo", "-svg", input_container_path, out_prefix]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        elif shutil.which("pdf2svg"):
            out_pattern = os.path.join(output_dir, "page_%d.svg")
            cmd = ["pdf2svg", input_container_path, out_pattern, "1-999"]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        elif shutil.which("inkscape"):
            out_pattern = os.path.join(output_dir, "page_1.svg")
            cmd = [shutil.which("inkscape"), input_container_path, f"--export-filename={out_pattern}", "--export-type=svg"]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Collect ALL SVG files generated in output_dir
        svg_files = sorted([
            os.path.join(output_dir, f) for f in os.listdir(output_dir)
            if f.endswith(".svg") and os.path.isfile(os.path.join(output_dir, f))
        ], key=natural_sort_key)

        return svg_files

    def build_multipage_svg(self, svg_file_list, base_root=None):
        """
        Construct Inkscape 1.2+ multi-page SVG tree.
        Creates <sodipodi:namedview> with child <inkscape:page> elements
        and places page layers at calculated X-axis offsets.
        """
        if base_root is None:
            root = ET.Element('{http://www.w3.org/2000/svg}svg', {
                'version': '1.1',
                'xmlns': NAMESPACES['svg'],
                'xmlns:inkscape': NAMESPACES['inkscape'],
                'xmlns:sodipodi': NAMESPACES['sodipodi'],
                'xmlns:xlink': NAMESPACES['xlink'],
            })
        else:
            root = base_root

        namedview = root.find(f"{{{NAMESPACES['sodipodi']}}}namedview")
        if namedview is None:
            namedview = ET.SubElement(root, f"{{{NAMESPACES['sodipodi']}}}namedview", {
                'id': 'namedview1',
                f"{{{NAMESPACES['inkscape']}}}document-units": 'px'
            })

        current_x_offset = 0.0

        for index, svg_path in enumerate(svg_file_list, start=1):
            tree = ET.parse(svg_path)
            page_root = tree.getroot()

            width_str = page_root.get('width', '800px').replace('pt', '').replace('px', '').replace('mm', '')
            height_str = page_root.get('height', '800px').replace('pt', '').replace('px', '').replace('mm', '')
            
            try:
                page_width = float(width_str)
                page_height = float(height_str)
            except ValueError:
                page_width, page_height = 800.0, 600.0

            ET.SubElement(namedview, f"{{{NAMESPACES['inkscape']}}}page", {
                'x': str(current_x_offset),
                'y': '0',
                'width': str(page_width),
                'height': str(page_height),
                'label': f"Page {index}",
                'id': f"page_{index}"
            })

            layer_node = ET.SubElement(root, f"{{{NAMESPACES['svg']}}}g", {
                f"{{{NAMESPACES['inkscape']}}}groupmode": 'layer',
                f"{{{NAMESPACES['inkscape']}}}label": f"Page {index} Content",
                'id': f"layer_page_{index}",
                'transform': f"translate({current_x_offset}, 0)"
            })

            for child in list(page_root):
                tag = child.tag
                if tag.endswith('namedview') or tag.endswith('metadata') or tag.endswith('defs'):
                    continue
                layer_node.append(child)

            current_x_offset += page_width + self.page_margin

        if svg_file_list:
            root.set('width', str(current_x_offset))
            root.set('height', str(page_height))

        return root


if inkex is not None:
    class CdrMultiPageImporterExtension(inkex.EffectExtension):
        def add_arguments(self, pars):
            pars.add_argument("--input_file", type=str, default="", help="Input CDR File")
            pars.add_argument("--extract_multipage", type=inkex.Boolean, default=True, help="Extract multi-page document")
            pars.add_argument("--target_dpi", type=int, default=300, help="Rendering DPI")
            pars.add_argument("--page_margin", type=float, default=20.0, help="Page Spacing Margin")

        def effect(self):
            missing_deps = CdrMultiPageImporter.check_system_dependencies()
            if missing_deps:
                msg = (
                    "Afterburner CDR Importer Dependency Error:\n"
                    "Missing system packages required to extract multi-page .cdr files:\n"
                    + "\n".join(f"- {dep}" for dep in missing_deps)
                    + "\n\nPlease install 'libreoffice' and 'poppler-utils' (pdftocairo) or 'pdf2svg' via your package manager."
                )
                inkex.errormsg(msg)
                return

            input_path = self.options.input_file
            if not input_path or not os.path.exists(input_path):
                inkex.errormsg(f"Error: Selected CorelDRAW (.cdr) input file '{input_path}' does not exist.")
                return

            importer = CdrMultiPageImporter(
                target_dpi=self.options.target_dpi,
                page_margin=self.options.page_margin,
                extract_multipage=self.options.extract_multipage
            )

            with tempfile.TemporaryDirectory() as temp_dir:
                try:
                    container_path = importer.convert_cdr_to_pdf(input_path, temp_dir)
                    svg_files = importer.extract_pdf_pages_to_svg(container_path, temp_dir)

                    if not svg_files:
                        inkex.errormsg("Warning: Could not extract SVG pages from the converted document.\nPlease ensure 'poppler-utils' (pdftocairo) or 'pdf2svg' is installed.")
                        return

                    svg_root = self.document.getroot()
                    importer.build_multipage_svg(svg_files, base_root=svg_root)

                except Exception as err:
                    inkex.errormsg(f"Multi-Page CDR Import failed:\n{str(err)}")


if __name__ == "__main__":
    if inkex is not None and len(sys.argv) > 1:
        CdrMultiPageImporterExtension().run()
