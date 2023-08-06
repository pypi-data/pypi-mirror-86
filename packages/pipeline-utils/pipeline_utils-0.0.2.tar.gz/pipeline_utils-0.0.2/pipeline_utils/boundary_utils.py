'''
 Copyright Vulcan Inc. 2020
 Licensed under the Apache License, Version 2.0 (the "License").
 You may not use this file except in compliance with the License.
 A copy of the License is located at
     http://www.apache.org/licenses/LICENSE-2.0
 or in the "license" file accompanying this file. This file is distributed
 on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 express or implied. See the License for the specific language governing
 permissions and limitations under the License.

 This module gets the boundary for the provided geojson input.
    The input can be in multiple formats:
    - Polygon geometry
    - MultiPolygon geometry
    - Feature with Polygon
    - Feature with MultiPolygon
    - FeatureCollection with Polygon
    - FeatureCollection with MultiPolygon 
    The supported locations are:
    - Function argument
    - Local file
    - Public (unauthenticated) URL
    - Google Earth Engine Asset ID
'''

import geojson
import requests
import ee
import os
import logging
import json
from geeutils import eu

EMPTY_BOUNDARY = {}


def _merge_geometries(features):
    # For multiple features, merge all geometries into one MultiPolygon
    merged_coordinates = []
    for feature in features:
        if feature.geometry.type == 'Polygon':
            merged_coordinates.append(feature.geometry.coordinates)
        elif feature.geometry.type == 'MultiPolygon':
            merged_coordinates.extend(feature.geometry.coordinates)

    merged_geometries = geojson.geometry.MultiPolygon(coordinates=merged_coordinates)

    return merged_geometries


def _get_boundary_from_local_path(boundary):
    if os.path.exists(boundary):
        logging.info('Reading boundary coordinates from file {}'.format(boundary))
        with open(boundary) as f:
            return geojson.loads(f.read())


def _get_boundary_from_url(boundary):
    try:
        resp = requests.get(boundary)
        if resp.status_code == 200:
            logging.info('Reading boundary coordinates from URL')
            return geojson.loads(resp.text)
        else:
            logging.info('Request to {0} returned HTTP {1}'.format(boundary, resp.status_code))
    except (requests.exceptions.InvalidSchema,
            requests.exceptions.InvalidURL,
            requests.exceptions.MissingSchema):
        pass


def _get_boundary_from_command_line(boundary):
        logging.info('Reading boundary coordinates from command line')
        try:
            return geojson.loads(boundary)
        except json.decoder.JSONDecodeError as e:
            raise ValueError('Invalid JSON: {}'.format(boundary)) from e


def _get_boundary_from_earthengine(boundary):

    try:
        logging.info('Authenticating to Google Earth Engine')
        eu.authenticate(allow_interactive=False)
    except ee.ee_exception.EEException:
        logging.info('You are not authenticated to Google Earth Engine API')
        return

    try:
        feature_collection = ee.FeatureCollection(boundary)
        first_feature = feature_collection.first()
        feature_dict = first_feature.getInfo()
        logging.info('Reading boundary coordinates from Google Earth Engine')
    except ee.ee_exception.EEException:
        logging.info('Boundary {} not found in Google Earth Engine')
        return

    boundary = geojson.MultiPolygon(feature_dict['geometry']['coordinates'])
    if not boundary.is_valid:
        boundary = geojson.Polygon(feature_dict['geometry']['coordinates'])

    return boundary


def get_boundary(boundary):
    '''
    Provide the boundary for the given geojson input.
    Args: 
        boundary(json): Json boundary input from variable locations and formats. 
    
    Returns a list of GeoJSON coordinates.
    '''
    geojson_obj = _get_boundary_from_earthengine(boundary) or \
                  _get_boundary_from_local_path(boundary) or \
                  _get_boundary_from_url(boundary) or \
                  _get_boundary_from_command_line(boundary)

    if not geojson_obj:
        return EMPTY_BOUNDARY

    if type(geojson_obj) == geojson.feature.FeatureCollection:
        boundary = _merge_geometries(geojson_obj.features)
    elif type(geojson_obj) == geojson.feature.Feature:
        boundary = _merge_geometries([geojson_obj])
    elif type(geojson_obj) in [geojson.geometry.Polygon, geojson.geometry.MultiPolygon]:
        boundary = geojson_obj
    else:
        raise ValueError('Boundary not recognized as a GeoJSON Feature, FeatureCollection, Polygon, or MultiPolygon')

    if not boundary.is_valid:
        raise ValueError(boundary.errors())

    return boundary.coordinates
