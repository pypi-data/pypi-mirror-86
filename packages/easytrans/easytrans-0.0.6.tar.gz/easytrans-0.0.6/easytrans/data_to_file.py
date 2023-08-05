import os
from collections import Iterable

from docxtpl import DocxTemplate

from easytrans.constant import FAILURE_STATUS, SUCCESS_STATUS, DOC_FORMAT
from easytrans.utils import FileUtil


class DataExportDoc(object):

    @staticmethod
    def data_to_doc(data, docx_template_path, doc_dir=None, doc_name=None, variable_name="data"):
        try:
            if not data or not docx_template_path:
                return FAILURE_STATUS, "'data' or 'docx_template_path' error!"

            if not os.path.isfile(docx_template_path) or not os.path.splitext(docx_template_path)[1] in DOC_FORMAT:
                return FAILURE_STATUS, "'{0}' file format error!".format(docx_template_path)

            doc_t = DocxTemplate(docx_template_path)
            doc_t.render({variable_name: data})

            if not doc_name:
                doc_name = FileUtil.generate_file_name()

            if not doc_dir:
                doc_dir = os.getcwd()

            if not os.path.exists(doc_dir):
                os.makedirs(doc_dir)

            doc_path = os.path.join(doc_dir, "{0}.docx".format(doc_name))

            doc_t.save(doc_path)

            return SUCCESS_STATUS, doc_path

        except Exception as e:
            return FAILURE_STATUS, repr(e)


class DataExportExcel(object):
    pass


class DataExportTxt(object):
    pass
