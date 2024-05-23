import threading
from pybars import Compiler

from . import constant


class HtmlGeneratorService:
    def __init__(self):
        self.compiler_lock = threading.Lock()
        self.thread_local = threading.local()

    def _get_compiler(self):
        compiler = getattr(self.thread_local, 'compiler', None)
        if compiler is None:
            with self.compiler_lock:
                compiler = Compiler()
            self.thread_local.compiler = compiler
        return compiler

    def generate_html(self, template_html, template_data):
        compiler = self._get_compiler()
        try:
            template = compiler.compile(template_html)
            html = template(template_data).replace(constant.LINE_BREAK, "").replace(constant.SPACE_TAB, "")
            return html
        except Exception as e:
            raise Exception(f"Error generating HTML: {str(e)}")



