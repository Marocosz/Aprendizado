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

Dependências necessárias (instale com o comando abaixo):
    pip install pymupdf4llm pdf2docx docx2pdf mammoth pypandoc
"""

import os
import argparse
import logging
import subprocess

# Configuração de Log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
                # Detecta se é a linha divisória do cabeçalho (|---|---|)
                is_separator = bool(re.match(r'^\|[\-\| :]+\|$', stripped))
                
                if is_separator:
                    if table_has_header:
                        i += 1
                        continue # Pula o separador se a tabela atual já tem um
                    else:
                        table_has_header = True
                        final_lines.append(line)
                else:
                    final_lines.append(line)
            else:
                if in_table and stripped == '':
                    # Linha vazia dentro da tabela. Checa se o conteúdo é retomado logo abaixo
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
                        continue # Ignora essa linha em branco para unir a tabela novamente
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
        import tempfile
        with open(input_path, "r", encoding="utf-8") as f:
            md_text = f.read()
        
        cleaned_md = self._clean_markdown_tables(md_text)
        
        temp_md = tempfile.NamedTemporaryFile(suffix=".md", delete=False).name
        with open(temp_md, "w", encoding="utf-8") as f:
            f.write(cleaned_md)
            
        return temp_md

    def pdf_to_markdown(self, input_path, output_path):
        """
        Converte PDF para Markdown
        Biblioteca recomendada: pymupdf4llm (Ótima para manter estrutura, tabelas e imagens)
        """
        try:
            import pymupdf4llm
            logging.info(f"Convertendo '{input_path}' para '{output_path}'...")
            
            md_text = pymupdf4llm.to_markdown(input_path)
            md_text = self._clean_markdown_tables(md_text) # Limpa as tabelas pro MD sair perfeito
            
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
            
            # Executa a conversão nativa do Office
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
        Converte Markdown para PDF
        Utilizamos pypandoc (melhor), com fallback para markdown + pdfkit
        """
        try:
            temp_md = self._clean_and_save_md(input_path)
            import pypandoc
            logging.info(f"Convertendo '{input_path}' para '{output_path}' usando Pandoc...")
            
            # Requer um motor-pdf no Pandoc (ex: wkhtmltopdf, weasyprint, pdflatex)
            # Vamos usar args pro Pandoc ficar mais flexível.
            try:
                pypandoc.convert_file(temp_md, 'pdf', format='gfm', outputfile=output_path, extra_args=['-V', 'geometry:margin=1in'])
            except OSError:
                logging.warning("Pandoc não encontrado. Baixando e instalando em 2º plano (apenas na primeira vez)...")
                pypandoc.download_pandoc()
                pypandoc.convert_file(temp_md, 'pdf', format='gfm', outputfile=output_path, extra_args=['-V', 'geometry:margin=1in'])

            logging.info("✅ Conversão de Markdown para PDF concluída!")
        except Exception as e:
            logging.error(f"O Pandoc precisa de motores externos (como Latex ou WeasyPrint) que não estão no seu PC: {e}")
            logging.info("Tentando método alternativo com qualidade máxima (MD -> DOCX -> PDF usando MS Word)...")
            
            try:
                import tempfile
                # Cria um arquivo Word temporário
                temp_docx = tempfile.NamedTemporaryFile(suffix=".docx", delete=False).name
                
                # Etapa 1: Converte o MD para Word
                self.markdown_to_word(input_path, temp_docx)
                
                # Etapa 2: Pede para o MS Word transformar o DOCX num lindo PDF
                self.word_to_pdf(temp_docx, output_path)
                
                # Limpa o arquivo temporário
                if os.path.exists(temp_docx):
                    os.remove(temp_docx)
                    
                logging.info("✅ Conversão Final concluída via intermédio DOCX!")
            except Exception as alt_err:
                logging.error(f"Erro catastrófico no método alternativo: {alt_err}")
                logging.info("Para gerar PDFs direto com Pandoc no futuro, instale o MiKTeX (pdflatex) no seu Windows.")
        finally:
            if 'temp_md' in locals() and temp_md and os.path.exists(temp_md):
                os.remove(temp_md)

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
