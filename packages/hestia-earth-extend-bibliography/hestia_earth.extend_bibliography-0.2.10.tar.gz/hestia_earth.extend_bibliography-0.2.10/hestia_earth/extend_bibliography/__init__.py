from pkgutil import extend_path
from functools import reduce
from hestia_earth.schema import SchemaType, Bibliography

from .bibliography_apis.utils import has_key, is_enabled, unique_values, biblio_name, actor_name
from .bibliography_apis.crossref import extend_crossref
from .bibliography_apis.mendeley import extend_mendeley
from .bibliography_apis.wos import extend_wos


__path__ = extend_path(__path__, __name__)


def is_node_of(node_type: SchemaType): return lambda node: node.get('type') == node_type.value


def update_source_from_biblios(source: dict, bibliographies: list):
    def update_key(key: str):
        value = source.get(key)
        biblio = next((x for x in bibliographies if value and value.get('title') == x.get('originalTitle')), None)
        if biblio:
            source[key] = {**source[key], **biblio}
            del source[key]['originalTitle']

            name = biblio.get('name', biblio.get('title'))
            if key == 'bibliography' and name:
                source['name'] = name

    update_key('bibliography')
    update_key('metaAnalysisBibliography')
    return source


def need_update_source(node: dict):
    def has_title(key: str): return key in node and 'title' in node.get(key)

    return has_title('bibliography') or has_title('metaAnalysisBibliography')


def update_sources(bibliographies: list):
    def update_single_source(source: dict):
        return update_source_from_biblios(source, bibliographies) if need_update_source(source) else source
    return update_single_source


def update_biblio(node: dict):
    name = biblio_name(node.get('authors'), node.get('year'))
    return {**node, **{'name': name if name else node.get('name')}}


def update_actor(node: dict):
    name = actor_name(node)
    if name:
        node['name'] = name
    return node


def update_source(node: dict):
    biblio = node.get('bibliography')
    if biblio:
        name = biblio.get('name', biblio.get('title'))
        if name:
            node['name'] = name
    return node


UPDATE_NODE_TYPE = {
    SchemaType.ACTOR.value: update_actor,
    SchemaType.BIBLIOGRAPHY.value: update_biblio,
    SchemaType.SOURCE.value: update_source,
}


def update_node(node):
    if isinstance(node, list):
        return list(reduce(lambda p, x: p + [update_node(x)], node, []))
    elif isinstance(node, dict):
        node_type = node.get('type')
        node = UPDATE_NODE_TYPE[node_type](node) if node_type in UPDATE_NODE_TYPE else node
        for key, value in node.items():
            node[key] = update_node(value)
    return node


def has_node_value(node: dict):
    def has_value(key: str):
        value = node.get(key)
        if isinstance(value, str) or isinstance(value, list):
            return len(value) > 0
        if isinstance(value, int):
            return value > 0
        return value is not None
    return has_value


def get_node_citation(node: dict):
    # name can be created from authors, therefore if authors not empty name can be skipped
    def can_compute_name(): return len(node.get('name', '')) > 0 or len(node.get('authors', [])) > 0

    required = Bibliography().required
    required_values = list(filter(has_node_value(node), required))
    required_values.extend(['name'] if 'name' not in required_values and can_compute_name() else [])
    title = node.get('title', '')
    return title if len(title) > 0 and len(required_values) != len(required) else None


def get_titles_from_node(node: dict):
    title = get_node_citation(node) if is_node_of(SchemaType.BIBLIOGRAPHY)(node) else None
    return list(set(reduce(lambda x, y: x + get_citations(y), node.values(), [] if title is None else [title])))


def get_citations(nodes):
    if isinstance(nodes, list):
        return list(set(reduce(lambda p, x: p + get_citations(x), nodes, [])))
    elif isinstance(nodes, dict):
        return get_titles_from_node(nodes)
    else:
        return []


def extend(content, **kwargs):
    nodes = content.get('nodes') if 'nodes' in content else []

    actors = []
    sources = list(filter(is_node_of(SchemaType.SOURCE), nodes))

    if has_key('mendeley_username', **kwargs):
        (authors, bibliographies) = extend_mendeley(sorted(get_citations(sources)), **kwargs)
        actors.extend([] if authors is None else authors)
        list(map(update_sources(bibliographies), sources))

    if has_key('wos_api_key', **kwargs) or (has_key('wos_api_user', **kwargs) and has_key('wos_api_pwd', **kwargs)):
        (authors, bibliographies) = extend_wos(sorted(get_citations(sources)), **kwargs)
        actors.extend([] if authors is None else authors)
        list(map(update_sources(bibliographies), sources))

    if is_enabled('enable_crossref', **kwargs):
        (authors, bibliographies) = extend_crossref(sorted(get_citations(sources)), **kwargs)
        actors.extend([] if authors is None else authors)
        list(map(update_sources(bibliographies), sources))

    # update all nodes except sources
    nodes = list(map(update_node, nodes))
    # TODO: find a better way, because of children we need to run twice for parents to have correct values
    nodes = list(map(update_node, nodes))

    return {'nodes': unique_values(actors) + nodes}
