import yaml
import json
import argparse
from collections import defaultdict

def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

vertex_map = defaultdict(int)
edge_map = defaultdict(int)

def build_maps_from_statistics(statistics):
    global vertex_map, edge_map
    vertex_map.clear()
    edge_map.clear()

    for v in statistics.get("vertex_type_statistics", []):
        vertex_map[v["type_name"].lower()] = v["count"]

    for e in statistics.get("edge_type_statistics", []):
        edge_type_name = e["type_name"].lower()
        for pair_stat in e.get("vertex_type_pair_statistics", []):
            src_name = pair_stat["source_vertex"].lower()
            dst_name = pair_stat["destination_vertex"].lower()
            edge_map[src_name + "_" + edge_type_name] = pair_stat["count"]
            edge_map[edge_type_name + "_" + dst_name] = pair_stat["count"]
            edge_map[edge_type_name] = pair_stat["count"]

def transform_vertex_types(vertex_types):
    vertex_stats = []
    for vt in vertex_types:
        type_name = vt['type_name']
        stats = {
            'type_id': vt['type_id'],
            'type_name': type_name,
            'count': vertex_map.get(type_name, 0)
        }
        vertex_stats.append(stats)
    return vertex_stats

def transform_edge_types(edge_types):
    edge_stats = []
    for et in edge_types:
        base_type_name = et['type_name']
        relations = et.get('vertex_type_pair_relations', [])
        stats_array = []
        for rel in relations:
            source = rel['source_vertex']
            dest = rel['destination_vertex']
            count = edge_map.get(base_type_name, 0)
            new_et = {
                'source_vertex': source,
                'destination_vertex': dest,
                'count': count
            }
            stats_array.append(new_et)
        stats = {
            'type_id': et['type_id'],
            'type_name': base_type_name,
            'vertex_type_pair_statistics': stats_array
        }
        edge_stats.append(stats)
    return edge_stats

def transform_yaml(schema_path, statistics_path, output_path):
    schema = load_yaml(schema_path)['schema']
    statistics = load_json(statistics_path)
    build_maps_from_statistics(statistics)

    stats = {}
    if 'vertex_types' in schema:
        stats['vertex_type_statistics'] = transform_vertex_types(schema['vertex_types'])
    if 'edge_types' in schema:
        stats['edge_type_statistics'] = transform_edge_types(schema['edge_types'])
    stats['total_vertex_count'] = statistics.get('total_vertex_count', 0)
    stats['total_edge_count'] = statistics.get('total_edge_count', 0)

    save_json(stats, output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform YAML schema using statistics JSON.")
    parser.add_argument('-s', '--schema', required=True, help='Path to the input YAML schema file.')
    parser.add_argument('-t', '--statistics', required=True, help='Path to the input statistics JSON file.')
    parser.add_argument('-o', '--output', required=True, help='Path to the output JSON file.')
    args = parser.parse_args()

    transform_yaml(args.schema, args.statistics, args.output)
