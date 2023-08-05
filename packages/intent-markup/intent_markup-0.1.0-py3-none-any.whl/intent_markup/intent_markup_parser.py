import xml.etree.ElementTree as xml
from typing import Union

from intent_markup.intent_markup import IntentMarkup, MustWord


class IntentMarkupParser:

    @staticmethod
    def parse(raw_xml: Union[str, bytes]):
        def parse_must_words(element: xml.Element):
            text = element.text
            fuzzy = element.attrib["fuzzy"] == "true" if "fuzzy" in element.attrib else False
            return MustWord(text, fuzzy)

        def element_to_string(element):
            s = str(element.text) or ""
            for sub_element in element:
                s += element_to_string(sub_element)
            if element.tail is not None:
                s += element.tail
            return s

        parsed_xml = xml.fromstring(raw_xml)

        autocomplete = parsed_xml.attrib["autocomplete"] == "true" if "autocomplete" in parsed_xml.attrib else True
        value = element_to_string(parsed_xml)
        must_words = list(map(parse_must_words, parsed_xml.findall("must")))

        return IntentMarkup(autocomplete, value, must_words)
