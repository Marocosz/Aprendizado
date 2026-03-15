"""
Conversor Universal de Documentos
=================================

Este script permite converter arquivos entre diferentes formatos (PDF, Word DOCX e Markdown MD)
usando as melhores bibliotecas disponíveis para manter a formatação, tabelas e imagens.

Como usar via Terminal (na raiz do projeto):
-----------------------
Abra o terminal na raiz do seu projeto e execute o script apontando para a pasta 'scripts':

    python scripts/converter.py <arquivo_de_entrada> <arquivo_de_saida>

O script detectará automaticamente a conversão necessária com base nas extensões dos arquivos.

Exemplos Práticos (executando da raiz do projeto):
------------------
1. PDF para Markdown:
   python scripts/converter.py meu_relatorio.pdf resultados/meu_relatorio.md

2. Markdown para Word (DOCX):
   python scripts/converter.py documentos/anotacoes.md anotacoes.docx

3. Word (DOCX) para PDF:
   python scripts/converter.py contrato.docx contrato.pdf

4. Markdown para PDF (visual idêntico ao GitHub):
   python scripts/converter.py documento.md documento.pdf

Dependências necessárias (instale com o comando abaixo):
    pip install pymupdf4llm pdf2docx docx2pdf mammoth pypandoc markdown pygments playwright
    python -m playwright install chromium
"""

import os
import argparse
import logging
import tempfile

# Configuração de Log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# CSS do GitHub Markdown — idêntico ao render do github.com
GITHUB_MARKDOWN_CSS = """
* { box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: #1f2328;
  background-color: #ffffff;
  max-width: 980px;
  margin: 0 auto;
  padding: 45px;
}

h1, h2, h3, h4, h5, h6 {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
}
h1 { font-size: 2em; padding-bottom: .3em; border-bottom: 1px solid #d1d9e0; }
h2 { font-size: 1.5em; padding-bottom: .3em; border-bottom: 1px solid #d1d9e0; }
h3 { font-size: 1.25em; }
h4 { font-size: 1em; }
h5 { font-size: .875em; }
h6 { font-size: .85em; color: #59636e; }

p { margin-top: 0; margin-bottom: 16px; }

a { color: #0969da; text-decoration: none; }
a:hover { text-decoration: underline; }

strong { font-weight: 600; }
em { font-style: italic; }

code {
  font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
  font-size: 85%;
  padding: .2em .4em;
  margin: 0;
  background-color: #f6f8fa;
  border-radius: 6px;
  border: 1px solid #d1d9e0;
}

pre {
  margin-top: 0;
  margin-bottom: 16px;
  overflow: auto;
  font-size: 85%;
  line-height: 1.45;
  background-color: #f6f8fa;
  border-radius: 6px;
  padding: 16px;
  border: 1px solid #d1d9e0;
}
pre code {
  display: inline;
  padding: 0;
  margin: 0;
  overflow: visible;
  line-height: inherit;
  background-color: transparent;
  border: 0;
  font-size: 100%;
  white-space: pre;
}

blockquote {
  margin: 0 0 16px 0;
  padding: 0 1em;
  color: #59636e;
  border-left: .25em solid #d1d9e0;
}
blockquote > :first-child { margin-top: 0; }
blockquote > :last-child { margin-bottom: 0; }

table {
  border-spacing: 0;
  border-collapse: collapse;
  display: table;
  width: 100%;
  margin-top: 0;
  margin-bottom: 16px;
}
th, td {
  padding: 6px 13px;
  border: 1px solid #d1d9e0;
  word-break: break-word;
}
th { font-weight: 600; background-color: #f6f8fa; }
tr:nth-child(2n) { background-color: #f6f8fa; }

ul, ol {
  margin-top: 0;
  margin-bottom: 16px;
  padding-left: 2em;
}
li { margin-top: .25em; }
li > p { margin-top: 16px; }
li + li { margin-top: .25em; }

hr {
  height: .25em;
  padding: 0;
  margin: 24px 0;
  background-color: #d1d9e0;
  border: 0;
}

img { max-width: 100%; height: auto; }

/* ── Correções para impressão/PDF ── */
@media print {
  body { padding: 0; }

  /* Evita quebrar linhas de tabela no meio ao virar a página */
  tr { break-inside: avoid; page-break-inside: avoid; }

  /* Evita quebrar blocos de código no meio */
  pre { break-inside: avoid; page-break-inside: avoid; overflow: visible; white-space: pre-wrap; }

  /* Evita quebrar títulos separados do parágrafo seguinte */
  h1, h2, h3, h4 { break-after: avoid; page-break-after: avoid; }
}

/* Syntax highlighting (Pygments github theme) */
.highlight .hll { background-color: #ffffcc }
.highlight .c   { color: #6a737d; font-style: italic }
.highlight .err { color: #a61717; background-color: #e3d2d2 }
.highlight .k   { color: #d73a49; font-weight: bold }
.highlight .o   { color: #d73a49 }
.highlight .cm  { color: #6a737d; font-style: italic }
.highlight .cp  { color: #999999; font-weight: bold }
.highlight .c1  { color: #6a737d; font-style: italic }
.highlight .cs  { color: #6a737d; font-weight: bold; font-style: italic }
.highlight .gd  { color: #a61717 }
.highlight .ge  { font-style: italic }
.highlight .gr  { color: #aa0000 }
.highlight .gh  { color: #0366d6; font-weight: bold }
.highlight .gi  { color: #22863a }
.highlight .go  { color: #888888 }
.highlight .gp  { color: #555555; font-weight: bold }
.highlight .gs  { font-weight: bold }
.highlight .gu  { color: #0366d6; font-weight: bold }
.highlight .gt  { color: #aa0000 }
.highlight .kc  { color: #d73a49; font-weight: bold }
.highlight .kd  { color: #d73a49; font-weight: bold }
.highlight .kn  { color: #d73a49; font-weight: bold }
.highlight .kp  { color: #d73a49 }
.highlight .kr  { color: #d73a49; font-weight: bold }
.highlight .kt  { color: #005cc5; font-weight: bold }
.highlight .m   { color: #005cc5 }
.highlight .s   { color: #032f62 }
.highlight .na  { color: #6f42c1 }
.highlight .nb  { color: #e36209 }
.highlight .nc  { color: #6f42c1; font-weight: bold }
.highlight .no  { color: #005cc5 }
.highlight .nd  { color: #6f42c1 }
.highlight .ni  { color: #005cc5 }
.highlight .ne  { color: #d73a49; font-weight: bold }
.highlight .nf  { color: #6f42c1 }
.highlight .nl  { color: #005cc5 }
.highlight .nn  { color: #005cc5; font-weight: bold }
.highlight .nt  { color: #22863a }
.highlight .nv  { color: #24292e }
.highlight .ow  { color: #d73a49; font-weight: bold }
.highlight .w   { color: #bbbbbb }
.highlight .mf  { color: #005cc5 }
.highlight .mh  { color: #005cc5 }
.highlight .mi  { color: #005cc5 }
.highlight .mo  { color: #005cc5 }
.highlight .sb  { color: #032f62 }
.highlight .sc  { color: #032f62 }
.highlight .sd  { color: #032f62; font-style: italic }
.highlight .s2  { color: #032f62 }
.highlight .se  { color: #032f62; font-weight: bold }
.highlight .sh  { color: #032f62 }
.highlight .si  { color: #005cc5 }
.highlight .sx  { color: #032f62 }
.highlight .sr  { color: #032f62 }
.highlight .s1  { color: #032f62 }
.highlight .ss  { color: #005cc5 }
.highlight .bp  { color: #e36209 }
.highlight .vc  { color: #24292e }
.highlight .vg  { color: #24292e }
.highlight .vi  { color: #24292e }
.highlight .il  { color: #005cc5 }
"""


class DocumentConverter:
    """
    Classe para converter documentos entre PDF, Word (DOCX) e Markdown (MD).
    Utiliza as melhores bibliotecas do estado da arte para cada tipo de conversão.
    """
    def __init__(self):
        pass

    def _check_file_exists(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")

    def _clean_markdown_tables(self, md_text):
        """
        Corrige tabelas quebradas criadas por conversores de PDF.
        Remove linhas em branco indesejadas e cabeçalhos repetidos no meio da mesma tabela.
        """
        import re
        lines = md_text.split('\n')
        final_lines = []
        in_table = False
        table_has_header = False

        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            is_table_row = stripped.startswith('|') and stripped.endswith('|')

            if is_table_row:
                in_table = True
                is_separator = bool(re.match(r'^\|[\-\| :]+\|$', stripped))

                if is_separator:
                    if table_has_header:
                        i += 1
                        continue
                    else:
                        table_has_header = True
                        final_lines.append(line)
                else:
                    final_lines.append(line)
            else:
                if in_table and stripped == '':
                    next_is_table = False
                    for j in range(i + 1, min(i + 5, len(lines))):
                        next_stripped = lines[j].strip()
                        if next_stripped.startswith('|') and next_stripped.endswith('|'):
                            next_is_table = True
                            break
                        elif next_stripped != '':
                            break

                    if next_is_table:
                        i += 1
                        continue
                    else:
                        in_table = False
                        table_has_header = False
                        final_lines.append(line)
                else:
                    in_table = False
                    table_has_header = False
                    final_lines.append(line)

            i += 1

        return '\n'.join(final_lines)

    def _clean_and_save_md(self, input_path):
        with open(input_path, "r", encoding="utf-8") as f:
            md_text = f.read()

        cleaned_md = self._clean_markdown_tables(md_text)

        temp_md = tempfile.NamedTemporaryFile(suffix=".md", delete=False).name
        with open(temp_md, "w", encoding="utf-8") as f:
            f.write(cleaned_md)

        return temp_md

    def _markdown_to_html(self, input_path):
        """
        Converte Markdown para HTML com renderização idêntica ao GitHub.
        Usa a biblioteca markdown com extensões GFM + Pygments para syntax highlighting.
        """
        import markdown
        from pygments.formatters import HtmlFormatter

        with open(input_path, "r", encoding="utf-8") as f:
            md_content = f.read()

        # Extensões que replicam o GitHub Flavored Markdown
        extensions = [
            'tables',           # tabelas estilo GFM
            'fenced_code',      # blocos de código com ```
            'codehilite',       # syntax highlighting via Pygments
            'toc',              # âncoras nos títulos
            'nl2br',            # quebras de linha como <br>
            'sane_lists',       # listas mais previsíveis
            'attr_list',        # {: .classe } em elementos
        ]

        extension_configs = {
            'codehilite': {
                'css_class': 'highlight',
                'guess_lang': False,
                'linenums': False,
            },
        }

        md = markdown.Markdown(extensions=extensions, extension_configs=extension_configs)
        html_body = md.convert(md_content)

        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
{GITHUB_MARKDOWN_CSS}
  </style>
</head>
<body>
{html_body}
</body>
</html>"""

        return html

    def pdf_to_markdown(self, input_path, output_path):
        """
        Converte PDF para Markdown
        Biblioteca recomendada: pymupdf4llm (Ótima para manter estrutura, tabelas e imagens)
        """
        try:
            import pymupdf4llm
            logging.info(f"Convertendo '{input_path}' para '{output_path}'...")

            md_text = pymupdf4llm.to_markdown(input_path)
            md_text = self._clean_markdown_tables(md_text)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(md_text)
            logging.info("✅ Conversão de PDF para Markdown concluída com sucesso!")
        except ImportError:
            logging.error("A biblioteca 'pymupdf4llm' não está instalada.")
            logging.info("Para instalar execute: pip install pymupdf4llm")

    def pdf_to_word(self, input_path, output_path):
        """
        Converte PDF para Word (DOCX)
        Biblioteca recomendada: pdf2docx (Mantém layouts, tabelas e formatação)
        """
        try:
            from pdf2docx import Converter
            logging.info(f"Convertendo '{input_path}' para '{output_path}'...")

            cv = Converter(input_path)
            cv.convert(output_path, start=0, end=None)
            cv.close()
            logging.info("✅ Conversão de PDF para Word concluída com sucesso!")
        except ImportError:
            logging.error("A biblioteca 'pdf2docx' não está instalada.")
            logging.info("Para instalar execute: pip install pdf2docx")

    def word_to_pdf(self, input_path, output_path):
        """
        Converte Word (DOCX) para PDF
        Biblioteca recomendada: docx2pdf (Usa o próprio MS Word no Windows/Mac, gerando o PDF perfeito)
        """
        try:
            from docx2pdf import convert
            logging.info(f"Convertendo '{input_path}' para '{output_path}'...")

            convert(input_path, output_path)
            logging.info("✅ Conversão de Word para PDF concluída com sucesso!")
        except ImportError:
            logging.error("A biblioteca 'docx2pdf' não está instalada.")
            logging.info("Para instalar execute: pip install docx2pdf")

    def word_to_markdown(self, input_path, output_path):
        """
        Converte Word para Markdown
        Biblioteca recomendada: mammoth (Excelente para transformar DOCX mantendo títulos, listas, etc.)
        """
        try:
            import mammoth
            logging.info(f"Convertendo '{input_path}' para '{output_path}'...")

            with open(input_path, "rb") as docx_file:
                result = mammoth.convert_to_markdown(docx_file)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(result.value)

            logging.info("✅ Conversão de Word para Markdown concluída com sucesso!")
            if result.messages:
                logging.warning(f"Avisos durante a conversão: {result.messages}")
        except ImportError:
            logging.error("A biblioteca 'mammoth' não está instalada.")
            logging.info("Para instalar execute: pip install mammoth")

    def markdown_to_word(self, input_path, output_path):
        """
        Converte Markdown para Word
        Biblioteca recomendada: pypandoc (Melhor motor de conversão de texto)
        """
        temp_md = None
        try:
            import pypandoc
            logging.info(f"Convertendo '{input_path}' para '{output_path}'...")

            temp_md = self._clean_and_save_md(input_path)

            try:
                pypandoc.convert_file(temp_md, 'docx', format='gfm', outputfile=output_path)
            except OSError:
                logging.warning("Pandoc não encontrado. Baixando e instalando em 2º plano (apenas na primeira vez)...")
                pypandoc.download_pandoc()
                pypandoc.convert_file(temp_md, 'docx', format='gfm', outputfile=output_path)

            logging.info("✅ Conversão de Markdown para Word concluída com sucesso!")
        except ImportError:
            logging.error("A biblioteca 'pypandoc' não está instalada ou o C-Pandoc não está no sistema.")
            logging.info("Para instalar execute: pip install pypandoc")
            logging.info("NOTA: Você precisa instalar o Pandoc (https://pandoc.org/installing.html)")
        finally:
            if temp_md and os.path.exists(temp_md):
                os.remove(temp_md)

    def markdown_to_pdf(self, input_path, output_path):
        """
        Converte Markdown para PDF com visual idêntico ao render do GitHub.

        Fluxo:
          1. Converte o Markdown para HTML com extensões GFM + syntax highlighting (Pygments)
          2. Aplica o CSS exato do github.com (github-markdown-css)
          3. Usa Playwright (Chromium headless) para imprimir o HTML em PDF

        Resultado: PDF com tipografia, tabelas, código colorido e espaçamento
        exatamente iguais ao que você vê em github.com ao abrir um .md.
        """
        temp_html = None
        try:
            from playwright.sync_api import sync_playwright

            logging.info(f"Convertendo '{input_path}' para '{output_path}' com renderização GitHub...")

            # Gera o HTML com estilo GitHub
            html_content = self._markdown_to_html(input_path)

            # Salva em arquivo temporário para o Playwright carregar via file://
            temp_html = tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8")
            temp_html.write(html_content)
            temp_html.close()
            temp_html_path = temp_html.name

            # Usa Playwright para imprimir o HTML como PDF
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page(viewport={"width": 1024, "height": 5000})
                page.emulate_media(media="screen")

                # set_content tem timing mais previsível que goto(file://)
                with open(temp_html_path, "r", encoding="utf-8") as fh:
                    html_content = fh.read()
                page.set_content(html_content, wait_until="networkidle")

                # Garante que fontes e layout do documento inteiro estão prontos
                # antes de paginar — evita células em branco no final de documentos longos
                page.evaluate("() => document.fonts.ready")
                page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(500)

                page.pdf(
                    path=output_path,
                    format="A4",
                    margin={
                        "top": "20mm",
                        "bottom": "20mm",
                        "left": "15mm",
                        "right": "15mm",
                    },
                    print_background=True,
                )
                browser.close()

            logging.info("✅ PDF gerado com visual idêntico ao GitHub!")

        except ImportError:
            logging.error("Playwright não está instalado.")
            logging.info("Para instalar execute:")
            logging.info("  pip install playwright markdown pygments")
            logging.info("  python -m playwright install chromium")
        except Exception as e:
            logging.error(f"Erro na conversão MD→PDF: {e}")
        finally:
            if temp_html and os.path.exists(temp_html.name):
                os.remove(temp_html.name)

    def auto_convert(self, input_path, output_path):
        """
        Detecta a extensão de entrada e saída e chama o método apropriado automaticamente.
        """
        try:
            self._check_file_exists(input_path)
        except Exception as e:
            logging.error(e)
            return

        in_ext = os.path.splitext(input_path)[1].lower()
        out_ext = os.path.splitext(output_path)[1].lower()

        if in_ext == '.pdf' and out_ext == '.md':
            self.pdf_to_markdown(input_path, output_path)

        elif in_ext == '.pdf' and out_ext == '.docx':
            self.pdf_to_word(input_path, output_path)

        elif in_ext == '.docx' and out_ext == '.pdf':
            self.word_to_pdf(input_path, output_path)

        elif in_ext == '.docx' and out_ext == '.md':
            self.word_to_markdown(input_path, output_path)

        elif in_ext == '.md' and out_ext == '.pdf':
            self.markdown_to_pdf(input_path, output_path)

        elif in_ext == '.md' and out_ext == '.docx':
            self.markdown_to_word(input_path, output_path)

        else:
            logging.warning(f"Conversão de '{in_ext}' para '{out_ext}' não suportada diretamente ou é a mesma extensão.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Conversor Universal de Documentos.\nSuporta conversões bidirecionais entre PDF, DOCX (Word) e MD (Markdown).",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("input_file", help="Caminho do arquivo de origem")
    parser.add_argument("output_file", help="Caminho do arquivo de destino (Extensão define o formato)")

    args = parser.parse_args()

    converter = DocumentConverter()
    converter.auto_convert(args.input_file, args.output_file)
