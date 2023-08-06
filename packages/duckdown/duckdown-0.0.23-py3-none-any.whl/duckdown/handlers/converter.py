# pylint: disable=E1101
""" Mixin to convert to images to s3 """
import markdown


class Converter:
    """ convert to remote if not debug """

    @property
    def markdown(self):
        """ returns a markdown instance """
        return markdown.Markdown(
            extensions=[
                "meta",
                "toc",
                "footnotes",
                "tables",
                "fenced_code",
                "attr_list",
                "def_list",
                "markdown_strikethrough.extension",
            ]
        )

    @property
    def img_path(self):
        """ return application img_path """
        return self.application.settings.get("img_path")

    @property
    def local_images(self):
        """ return application local_images """
        return self.application.settings.get("local_images")

    def convert_images(self, value):
        """ use img_path """
        if self.local_images is True:
            return value
        return value.replace("/static/", self.img_path)
