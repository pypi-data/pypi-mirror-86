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
'''


import setuptools


with open("README.md", "r") as f:
    long_description = f.read()


setuptools.setup(
    name="pipeline_utils",
    version="0.0.2",
    description="Utility functions for Coral Atlas Pipelines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['earthengine-api>=0.1.239', 'geeutils>=0.3.0', 'geojson>=2.5.0'],
    packages=['pipeline_utils'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    url='https://github.com/CoralMapping/proc_pipeline_utils'
)
