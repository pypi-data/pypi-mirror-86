from django import template
from django.utils.html import mark_safe
from psu_base.classes.Log import Log
from psu_base.templatetags.tag_processing import supporting_functions as support
from django.urls import reverse
from psu_upload.services import upload_service, retrieval_service
import base64

register = template.Library()
log = Log()


@register.tag()
def file_link(parser, token):
    return FileLinkNode(token.split_contents())


@register.tag()
def database_image(parser, token):
    return DatabaseImageNode(token.split_contents())


class FileLinkNode(template.Node):
    """Generates a link to an uploaded file in S3"""
    def __init__(self, args):
        self.args = args

    def render(self, context):
        # Prepare attributes
        attrs = support.process_args(self.args, context)
        log.trace(attrs, function_name='upload_taglib.FileLinkNode')

        # File (psu_upload.models.UploadedFile|DatabaseFile) is required
        file_instance = attrs.get('file')
        if not file_instance:
            log.error("No file instance was given. Unable to render link to file")
            return ''

        # Attrs with defaults
        target = attrs.get('target', '_blank')
        icon = attrs.get('icon', True)
        size = attrs.get('size', False)
        original_name = attrs.get('original_name', False)
        html_class = attrs.get('class', '')

        # Remove special attrs that should not appear in the HTML element or that are handled above
        for ii in ['file', 'target', 'icon', 'size', 'class']:
            if ii in attrs:
                del attrs[ii]

        icon_class_str = None
        if icon:
            # Default icon
            icon_class_str = file_instance.icon_class()
            # If an actual class was specified
            if type(icon) is str and icon.lower() not in ['y', 'yes', 'n', 'no', 'true', 'false', 'none']:
                icon_class_str = icon
            # If string is something negative, no icon
            elif type(icon) is str and icon.lower() in ['n', 'no', 'false', 'none']:
                icon = False
            # otherwise, use default icon

            icon = f"""<span class="{icon_class_str} upload-link upload-link-icon" aria-hidden="true"></span> """

        pieces = [f"""<span class="upload-link upload-link-container {html_class}" """]

        # Append any other attrs (id, style, etc)
        for attr_key, attr_val in attrs.items():
            pieces.append(f"{attr_key}=\"{attr_val}\"")

        # Close container tag
        pieces.append(">")

        # Add link
        if upload_service.using_s3():
            pieces.append(
                f"""<a href="{file_instance.file.url}" class="upload-link upload-link-a" target="{target}">"""
            )
        else:
            try:
                file_url = reverse("upload:database_file", args=[file_instance.id])
            except Exception as ee:
                log.error(f"Could not link to file: {file_instance.id}")
                log.error(ee)
                file_url = '#'
            pieces.append(
                f"""<a href="{file_url}" class="upload-link upload-link-a" target="{target}">"""
            )

        # If including an icon
        if icon:
            pieces.append(icon)

        # File name
        if original_name:
            name = file_instance.original_name
        else:
            name = file_instance.basename if upload_service.using_s3() else file_instance.filename

        pieces.append(f"""<span class="upload-link upload-link-name">{name}</span>""")

        # End the link
        pieces.append('</a>')

        # If displaying the file size (not part of click-able link)
        if size:
            if (type(size) is str and size.lower() in ['n', 'no', 'false', 'none']):
                pass
            else:
                pieces.append(f""" <span class="upload-link upload-link-size">{file_instance.readable_size()}</span>""")

        # End container
        pieces.append("</span>")

        # Return full HTML
        return mark_safe(' '.join(pieces))


class DatabaseImageNode(template.Node):
    """Display an image file from the database (in an <img /> tag)"""
    def __init__(self, args):
        self.args = args

    def render(self, context):
        # Prepare attributes
        attrs = support.process_args(self.args, context)
        log.trace(attrs, function_name='upload_taglib.DatabaseImageNode')

        # File (psu_upload.models.DatabaseFile) is required
        file_instance = attrs.get('file')
        if not file_instance:
            log.error("No file instance was given. Unable to render image")
            return ''

        if 'image' not in file_instance.content_type:
            return f"""<span class="{file_instance.icon_class()}"></span>"""

        # Remove special attrs that should not appear in the HTML element or that are handled above
        for ii in ['file']:
            if ii in attrs:
                del attrs[ii]

        pieces = [f"""<img """]

        b64img = base64.b64encode(file_instance.file).decode()
        pieces.append(f"""src = "data:{file_instance.content_type};base64,{b64img}" """)

        # Append any other attrs (id, style, etc)
        for attr_key, attr_val in attrs.items():
            pieces.append(f"{attr_key}=\"{attr_val}\"")

        # Close container tag
        pieces.append(" />")

        # Return full HTML
        return mark_safe(' '.join(pieces))
