import re
import codecs

from compatibility import StringIO


class XMLwriter(object):

    def __init__(self):
        self.fh = None
        self.escapes = re.compile('["&<>]')
        self.internal_fh = False

    def _set_filehandle(self, filehandle):
        self.fh = filehandle
        self.internal_fh = False

    def _set_xml_writer(self, filename):
        if isinstance(filename, StringIO):
            self.internal_fh = False
            self.fh = filename
        else:
            self.internal_fh = True
            self.fh = codecs.open(filename, 'w', 'utf-8')

    def _xml_close(self):
        if self.internal_fh:
            self.fh.close()

    def _xml_declaration(self):
        self.fh.write(
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n""")

    def _xml_start_tag(self, tag, attributes=[]):
        for key, value in attributes:
            value = self._escape_attributes(value)
            tag += ' %s="%s"' % (key, value)

        self.fh.write("<%s>" % tag)

    def _xml_start_tag_unencoded(self, tag, attributes=[]):
        for key, value in attributes:
            tag += ' %s="%s"' % (key, value)

        self.fh.write("<%s>" % tag)

    def _xml_end_tag(self, tag):
        self.fh.write("</%s>" % tag)

    def _xml_empty_tag(self, tag, attributes=[]):
        for key, value in attributes:
            value = self._escape_attributes(value)
            tag += ' %s="%s"' % (key, value)

        self.fh.write("<%s/>" % tag)

    def _xml_empty_tag_unencoded(self, tag, attributes=[]):
        for key, value in attributes:
            tag += ' %s="%s"' % (key, value)

        self.fh.write("<%s/>" % tag)

    def _xml_data_element(self, tag, data, attributes=[]):
        end_tag = tag

        for key, value in attributes:
            value = self._escape_attributes(value)
            tag += ' %s="%s"' % (key, value)

        data = self._escape_data(data)
        self.fh.write("<%s>%s</%s>" % (tag, data, end_tag))

    def _xml_string_element(self, index, attributes=[]):
        attr = ''

        for key, value in attributes:
            value = self._escape_attributes(value)
            attr += ' %s="%s"' % (key, value)

        self.fh.write("""<c%s t="s"><v>%d</v></c>""" % (attr, index))

    def _xml_si_element(self, string, attributes=[]):
        attr = ''

        for key, value in attributes:
            value = self._escape_attributes(value)
            attr += ' %s="%s"' % (key, value)

        string = self._escape_data(string)

        self.fh.write("""<si><t%s>%s</t></si>""" % (attr, string))

    def _xml_rich_si_element(self, string):

        self.fh.write("""<si>%s</si>""" % string)

    def _xml_number_element(self, number, attributes=[]):
        attr = ''

        for key, value in attributes:
            value = self._escape_attributes(value)
            attr += ' %s="%s"' % (key, value)

        self.fh.write("""<c%s><v>%.15g</v></c>""" % (attr, number))

    def _xml_formula_element(self, formula, result, attributes=[]):
        attr = ''

        for key, value in attributes:
            value = self._escape_attributes(value)
            attr += ' %s="%s"' % (key, value)

        self.fh.write("""<c%s><f>%s</f><v>%s</v></c>"""
                      % (attr, self._escape_data(formula),
                         self._escape_data(result)))

    def _xml_inline_string(self, string, preserve, attributes=[]):
        attr = ''
        t_attr = ''

        if preserve:
            t_attr = ' xml:space="preserve"'

        for key, value in attributes:
            value = self._escape_attributes(value)
            attr += ' %s="%s"' % (key, value)

        string = self._escape_data(string)

        self.fh.write("""<c%s t="inlineStr"><is><t%s>%s</t></is></c>""" %
                      (attr, t_attr, string))

    def _xml_rich_inline_string(self, string, attributes=[]):
        attr = ''

        for key, value in attributes:
            value = self._escape_attributes(value)
            attr += ' %s="%s"' % (key, value)

        self.fh.write("""<c%s t="inlineStr"><is>%s</is></c>""" %
                      (attr, string))

    def _escape_attributes(self, attribute):
        try:
            if not self.escapes.search(attribute):
                return attribute
        except TypeError:
            return attribute

        attribute = attribute.replace('&', '&amp;')
        attribute = attribute.replace('"', '&quot;')
        attribute = attribute.replace('<', '&lt;')
        attribute = attribute.replace('>', '&gt;')

        return attribute

    def _escape_data(self, data):
        try:
            if not self.escapes.search(data):
                return data
        except TypeError:
            return data

        data = data.replace('&', '&amp;')
        data = data.replace('<', '&lt;')
        data = data.replace('>', '&gt;')

        return data
