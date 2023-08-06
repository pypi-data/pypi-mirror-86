# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.similar_posts']

package_data = \
{'': ['*']}

install_requires = \
['gensim>=3.5.0', 'pelican>=4.5,<5.0']

extras_require = \
{'markdown': ['markdown>=3.2.2,<4.0.0']}

setup_kwargs = {
    'name': 'pelican-similar-posts',
    'version': '1.0.0',
    'description': 'Pelican plugin to add similar posts to articles, based on a vector space model',
    'long_description': 'Similar Posts: A Plugin for Pelican\n===================================\n\n[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/similar-posts/build)](https://github.com/pelican-plugins/similar-posts/actions) [![PyPI Version](https://img.shields.io/pypi/v/pelican-similar-posts)](https://pypi.org/project/pelican-similar-posts/)\n\n**Similar Posts** is a Pelican plugin that adds the `similar_posts` variable to every published article\'s context.\n\nThe inputs to the similarity measurement algorithm are article tags. Thus, for this plugin to be of any use, at least some of your articles must have a `tags` element in their [metadata](http://docs.getpelican.com/en/stable/content.html#file-metadata).\n\nThe `similar_posts` variable is a list of `Article` objects, or an empty list if no articles could be found with at least one tag in common with the given article. The list is sorted by descending similarity, then by descending date.\n\nRequirements\n------------\n\nThis plugin requires Python 3.6 or later.\n\nIt depends on [Gensim](https://radimrehurek.com/gensim/index.html), which has its own dependencies such as [NumPy](http://www.numpy.org/), [SciPy](https://www.scipy.org/), and [`smart_open`](https://pypi.org/project/smart_open/).\n\nInstallation\n------------\n\nThis plugin can be installed via:\n\n    python -m pip install pelican-similar-posts\n\nConfiguration\n-------------\n\nBy default, up to five articles are listed. You may customize this value by defining `SIMILAR_POSTS_MAX_COUNT` in your Pelican settings file. For example:\n\n    SIMILAR_POSTS_MAX_COUNT = 10\n\nYou may also define `SIMILAR_POSTS_MIN_SCORE` in the settings file. It defaults to .0001. A value of 1.0 would restrict the list of similar posts to articles that have the same set of tags. Any value greater than 0.0 acts as a similarity threshold, but to play with this you\'ll probably have to find a proper value empirically. When running Pelican with the `--debug` option, extra messages show the scores of the similar posts.\n\nYou can output the `similar_posts` variable in your article template. This might look like the following:\n\n    ```html+jinja\n    {% if article.similar_posts %}\n        <ul>\n        {% for similar in article.similar_posts %}\n            <li><a href="{{ SITEURL }}/{{ similar.url }}">{{ similar.title }}</a></li>\n        {% endfor %}\n        </ul>\n    {% endif %}\n    ```\n\nSimilarity Score\n----------------\n\nThe measure of similarity is based on the [vector space model](https://en.wikipedia.org/wiki/Vector_space_model), which represents text documents as vectors. Each vector component corresponds to one of the terms that exists in the corpus. Thus the corpus may be represented as a matrix whose lines correspond to documents, and whose columns correspond to terms.\n\nIn this implementation, terms (tags) are weighted using the [tf-idf model](https://en.wikipedia.org/wiki/Tf–idf), which essentially means that terms that are rare across the whole corpus have greater values than those that are very common. The idea is that a term that is present in a great number of documents does not provide much specificity; it does not help relate a document to another in particular as much as a term that occurs in only a few documents.\n\nSay we have a corpus with five terms. A document\'s vector might look like:\n\n    [.9, .1, .0, .0, .3]\n\nThis document has three terms. The first one has a high value, meaning it is relatively rare across the whole corpus. The second one has a low value, meaning it is much more common. The next two terms are absent from this document, while the last term is present and also somewhat common in the corpus, although not as common as the second term. If, for example, another document contains only the first and last terms, it should be considered more relevant to this document than another that would have just the first and second terms, or just the second and last terms.\n\nWe measure the similarity of two documents by computing the cosine of the angle between their unit vectors. The resulting "score" is bounded in [0, 1]. Two vectors with the same orientation have a [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity) of 1. The lower the value, the greater the angle between the vectors; the more "dissimilar" the documents are.\n\nComparison with the *Related Posts* plugin\n------------------------------------------\n\nThe [Related Posts plugin](https://github.com/pelican-plugins/related-posts) relates articles that have the greatest number of tags in common, without any tag weighting. If many articles match with the same number of tags, they all get the same score. On most web sites, the list of recommended articles is short, so the most relevant ones will often be left out if all have the same score.\n\nPerhaps to circumvent this problem, the plugin allows one to manually link related posts by slug. However, that creates a content maintenance burden; old posts will not link to newer ones, unless they are manually edited to add them.\n\nContributing\n------------\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[existing issues]: https://github.com/pelican-plugins/similar-posts/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n',
    'author': 'David Lesieur',
    'author_email': 'david@davidlesieur.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pelican-plugins/similar-posts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
