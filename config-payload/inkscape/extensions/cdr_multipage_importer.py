#!/usr/bin/env python3
"""
Afterburner v2.0: Multi-Page CorelDRAW (.cdr) Importer for Inkscape
------------------------------------------------------------------
Extracts multi-page CorelDRAW (.cdr) documents using libcdr-tools / LibreOffice,
splits pages cleanly, and constructs native Inkscape 1.2+ multi-page SVG DOM nodes
(<inkscape:page> in <sodipodi:namedview>).
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
    # Graceful fallback for test runners outside Inkscape runtime
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

        if shutil.which("soffice") or shutil.which("libreoffice"):
            has_cdr_converter = True
        elif shutil.which("cdr2xhtml") or shutil.which("cdr2raw"):
            has_cdr_converter = True

        if not has_cdr_converter:
            missing.append("libcdr-tools (cdr2xhtml/cdr2raw) or LibreOffice (soffice)")

        has_pdf_splitter = False
        if shutil.which("pdftocairo") or shutil.which("pdf2svg"):
            has_pdf_splitter = True

        if not has_pdf_splitter:
            missing.append("pdftocairo (poppler-utils) or pdf2svg")

        return missing

    def convert_cdr_to_pdf(self, cdr_path, output_dir):
        """Convert .cdr file to intermediate multi-page PDF container."""
        if shutil.which("soffice") or shutil.which("libreoffice"):
            cmd_binary = shutil.which("soffice") or shutil.which("libreoffice")
            cmd = [cmd_binary, "--headless", "--convert-to", "pdf", "--outdir", output_dir, cdr_path]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                base_name = os.path.splitext(os.path.basename(cdr_path))[0]
                pdf_path = os.path.join(output_dir, f"{base_name}.pdf")
                if os.path.exists(pdf_path):
                    return pdf_path

        # Fallback to cdr2xhtml / cdr2raw if available
        if shutil.which("cdr2xhtml"):
            xhtml_path = os.path.join(output_dir, "output.html")
            cmd = ["cdr2xhtml", cdr_path, xhtml_path]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0 and os.path.exists(xhtml_path):
                return xhtml_path

        raise RuntimeError("Failed to convert .cdr file. Please ensure LibreOffice or libcdr-tools is installed.")

    def extract_pdf_pages_to_svg(self, pdf_path, output_dir):
        """Split multi-page PDF into individual SVG files."""
        svg_files = []

        if shutil.which("pdftocairo"):
            # pdftocairo -svg input.pdf output_dir/page
            out_prefix = os.path.join(output_dir, "page")
            cmd = ["pdftocairo", "-svg", pdf_path, out_prefix]
            subprocess.run(cmd, check=True)
            
            extracted = sorted([
                os.path.join(output_dir, f) for f in os.listdir(output_dir)
                if f.startswith("page") and f.endswith(".svg")
            ])
            return extracted

        elif shutil.which("pdf2svg"):
            # pdf2svg input.pdf output_dir/page_%d.svg all
            out_pattern = os.path.join(output_dir, "page_%d.svg")
            cmd = ["pdf2svg", pdf_path, out_pattern, "1-999"]
            subprocess.run(cmd, check=True)

            extracted = sorted([
                os.path.join(output_dir, f) for f in os.listdir(output_dir)
                if f.startswith("page_") and f.endswith(".svg")
            ])
            return extracted

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

        # Locate or create <sodipodi:namedview>
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

            # Extract page dimensions (default to 800x600 if missing)
            width_str = page_root.get('width', '800px').replace('pt', '').replace('px', '')
            height_str = page_root.get('height', '800px').replace('pt', '').replace('px', '')
            
            try:
                page_width = float(width_str)
                page_height = float(height_str)
            except ValueError:
                page_width, page_height = 800.0, 600.0

            # Add Inkscape 1.2+ native page element to <sodipodi:namedview>
            page_node = ET.SubElement(namedview, f"{{{NAMESPACES['inkscape']}}}page", {
                'x': str(current_x_offset),
                'y': '0',
                'width': str(page_width),
                'height': str(page_height),
                'label': f"Page {index}",
                'id': f"page_{index}"
            })

            # Create Layer Group for this Page Content
            layer_node = ET.SubElement(root, f"{{{NAMESPACES['svg']}}}g", {
                f"{{{NAMESPACES['inkscape']}}}groupmode": 'layer',
                f"{{{NAMESPACES['inkscape']}}}label": f"Page {index} Content",
                'id': f"layer_page_{index}",
                'transform': f"translate({current_x_offset}, 0)"
            })

            # Copy elements into layer node
            for child in list(page_root):
                tag = child.tag
                if tag.endswith('namedview') or tag.endswith('metadata') or tag.endswith('defs'):
                    continue
                layer_node.append(child)

            # Advance X offset for next page
            current_x_offset += page_width + self.page_margin

        # Set canvas dimensions on root
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
                inkex.errormsg("Error: Selected CorelDRAW (.cdr) input file does not exist.")
                return

            importer = CdrMultiPageImporter(
                target_dpi=self.options.target_dpi,
                page_margin=self.options.page_margin,
                extract_multipage=self.options.extract_multipage
            )

            with tempfile.TemporaryDirectory() as temp_dir:
                try:
                    pdf_path = importer.convert_cdr_to_pdf(input_path, temp_dir)
                    svg_files = importer.extract_pdf_pages_to_svg(pdf_path, temp_dir)

                    if not svg_files:
                        inkex.errormsg("Warning: Could not extract SVG pages from the converted PDF.")
                        return

                    # Build multi-page tree directly onto current SVG document
                    svg_root = self.document.getroot()
                    importer.build_multipage_svg(svg_files, base_root=svg_root)

                except Exception as err:
                    inkex.errormsg(f"Multi-Page CDR Import failed: {str(err)}")


if __name__ == "__main__":
    if inkex is not None and len(sys.argv) > 1:
        CdrMultiPageImporterExtension().run()
