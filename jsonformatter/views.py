import json
from json import JSONDecodeError

import pygments
from django.http import HttpResponse
from django.template import loader
from django.views.generic.base import View
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import JsonLexer


class FormatSubmitView(View):
    template = 'formatter/format_submit.html'

    def post(self, request):
        template = loader.get_template(self.template)
        json_to_format = request.POST.get('json_to_format',
                                          '{"a": [{"b": 123, "c": "32123"}, {"b": {"b": 123, "c": "32123"}, "c": "32123"}], "nested": {"b": 123, "c": "32123"}} ')

        errors, formatted_json = FormatSubmitView.plain_json_string_to_html(json_to_format)

        context = {}
        if errors:
            context['errors'] = errors
        context['formatted_json'] = formatted_json
        context['styles'] = HtmlFormatter().get_style_defs('.highlight')
        rendered_template = template.render(context, request)

        return HttpResponse(rendered_template, content_type='text/html')

    @staticmethod
    def plain_json_string_to_html(json_to_format):
        errors = None
        parsed_json = ''
        if json_to_format.strip() != '':
            try:
                parsed_json = json.loads(json_to_format)
            except JSONDecodeError as e:
                errors = e.msg
        formatted_json = json.dumps(parsed_json, indent=4, )
        formatted_json = highlight(formatted_json, pygments.lexers.data.JsonLexer(), HtmlFormatter())
        return errors, formatted_json

    def get(self, request):
        return self.post(request)


class FormatAjaxSubmitView(FormatSubmitView):
    template = 'formatter/format_results.html'
