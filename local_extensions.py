import urllib
from cookiecutter.utils import simple_filter


@simple_filter
def test_database_url(url):
    parsed_url = urllib.parse.urlparse(url)
    test_path_parts = parsed_url.path.split("/", 1)
    test_path_parts[1] = "test_" + test_path_parts[1]
    test_path = "/".join(test_path_parts)
    return parsed_url._replace(path=test_path).geturl()
