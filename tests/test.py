import os
import sys
import unittest

import config

sys.path.append("..")


class TestTasks(unittest.TestCase):

    def test_content_path_is_a_valid_directory(self):
        """Check we can access and list the files contained in constant
        CONTENT_PATH.
        """

        path_to_content_dir = config.CONTENT_PATH
        # check content path is a directory
        self.assertTrue(os.path.isdir(path_to_content_dir))
        # check content path is not empty
        self.assertGreater(len(os.listdir(path_to_content_dir)), 0)
        # Check we have write permission to directory
        self.assertTrue(os.access(path_to_content_dir, os.W_OK))


class TestSanitizeString(unittest.TestCase):
    """sanitize_string() builds the slug used as a Hugo file name."""

    def test_sanitize_string_builds_a_slug(self):
        from app.utils import sanitize_string

        # accents are transliterated, spaces and special characters become
        # hyphens, and runs of hyphens are collapsed into one
        self.assertEqual(
            sanitize_string("  un été à Paris : l'hôtel & moi  "),
            "un-ete-a-Paris-l-hotel-moi",
        )
        # dots are kept on purpose, so that a file extension survives
        self.assertEqual(sanitize_string("Ma Photo.JPG"), "Ma-Photo.JPG")
        # a string that is already a slug is left untouched
        self.assertEqual(sanitize_string("deja-un-slug"), "deja-un-slug")


class TestAllowedFile(unittest.TestCase):
    """allowed_file() guards the image upload form."""

    def test_allowed_file_accepts_only_configured_extensions(self):
        from app.utils import allowed_file

        for name in ("photo.jpg", "photo.JPG", "doc.pdf", "img.png"):
            self.assertTrue(allowed_file(name), name)
        for name in ("script.exe", "page.html", "archive.tar.gz"):
            self.assertFalse(allowed_file(name), name)
        # a name without an extension is refused
        self.assertFalse(allowed_file("noextension"))


class TestFileHeaderAndBody(unittest.TestCase):
    """get_file_header_and_body() splits a Hugo content file into its toml
    header and its body, and turns the header into form fields.
    """

    CONTENT_FILE = (
        "+++\n"
        'title = "Mon titre"\n'
        "draft = false\n"
        "# un commentaire\n"
        "+++\n"
        "\n"
        "Le corps du texte.\n"
    )

    def test_get_file_header_and_body_splits_header_from_body(self):
        from app.utils import get_file_header_and_body

        result = get_file_header_and_body(self.CONTENT_FILE)

        # the body is everything after the closing +++
        self.assertIn("Le corps du texte.", result["body"])
        self.assertNotIn("title", result["body"])

        input_fields = [f for f in result["header"] if f["is_input_field"]]
        # the header holds two input fields, numbered in reading order
        self.assertEqual([f["key"] for f in input_fields], ["1_title", "2_draft"])
        self.assertEqual(input_fields[0]["value"], "Mon titre")
        # each field carries its structure, read from config.PARAMETERS
        self.assertEqual(input_fields[0]["structure"]["type"], "str")
        self.assertEqual(input_fields[1]["structure"]["type"], "bool")

        # the comment line is kept, but not as an input field
        comments = [
            f for f in result["header"] if f["value"].strip() == "# un commentaire"
        ]
        self.assertEqual(len(comments), 1)
        self.assertFalse(comments[0]["is_input_field"])


class TestEscaping(unittest.TestCase):
    """A value POSTed from a form is escaped before being written between the
    quotes of a toml field, and un-escaped before being displayed again.
    """

    def test_escaping_double_quotes_is_reversible(self):
        from app.utils import (
            escape_special_characters_within_string_inputs,
            un_escape_special_characters_within_string_inputs,
        )

        original = 'il dit "bonjour"'
        escaped = escape_special_characters_within_string_inputs(original)

        # the double quotes are backslash-escaped so they do not close the
        # toml string
        self.assertEqual(escaped, r"il dit \"bonjour\"")
        # and the round trip gives back the original value
        self.assertEqual(
            un_escape_special_characters_within_string_inputs(escaped), original
        )


class TestRoutes(unittest.TestCase):
    """Smoke test: the app boots and its entry points answer."""

    def test_home_page_and_logout_respond(self):
        from app import main

        client = main.app.test_client()

        # the home page lists the content files
        self.assertEqual(client.get("/").status_code, 200)
        # logout redirects back to the home page
        response = client.get("/logout")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/")


if __name__ == "__main__":
    unittest.main()
