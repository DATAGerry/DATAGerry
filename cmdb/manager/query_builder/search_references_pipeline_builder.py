# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2024 becon GmbH
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""TODO: document"""
import logging

from cmdb.manager.query_builder.pipeline_builder import PipelineBuilder
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                        SearchReferencesPipelineBuilder - CLASS                                       #
# -------------------------------------------------------------------------------------------------------------------- #
class SearchReferencesPipelineBuilder(PipelineBuilder):
    """TODO: document"""

    def __init__(self, pipeline: list[dict] = None):
        """
        Init constructor load reference fields in runtime.
        The search should interpret reference section like normal field contents.
        This means that fields should already be loaded into the object during runtime.
        Args:
            pipeline: preset a for defined pipeline
        """
        super().__init__(pipeline=pipeline)


    def build(self, *args, **kwargs) -> list[dict]:
        # Load reference fields in runtime
        self.add_pipe(self.lookup_('framework.objects', 'fields.value', 'public_id', 'data'))
        self.add_pipe(
            self.project_({
                '_id': 1, 'public_id': 1, 'type_id': 1, 'active': 1, 'author_id': 1, 'creation_time': 1, 'version': 1,
                'last_edit_time': 1, 'fields': 1, 'relatesTo': '$data.public_id',
                'simple': {
                    '$reduce': {
                        'input': "$data.fields",
                        'initialValue': [],
                        'in': {'$setUnion': ["$$value", "$$this"]}
                    }
                }
            })
        )
        self.add_pipe(
            self.group_('$_id', {
                'public_id': {'$first': '$public_id'},
                'type_id': {'$first': '$type_id'},
                'active': {'$first': '$active'},
                'author_id': {'$first': '$author_id'},
                'creation_time': {'$first': '$creation_time'},
                'last_edit_time': {'$first': '$last_edit_time'},
                'version': {'$first': 'version'},
                'fields': {'$first': '$fields'},
                'simple': {'$first': '$simple'},
                'relatesTo': {'$first': '$relatesTo'}
            })
        )
        self.add_pipe(
            self.project_({
                '_id': 1, 'public_id': 1, 'type_id': 1, 'active': 1, 'author_id': 1, 'creation_time': 1, 'version': 1,
                'last_edit_time': 1, 'fields': {'$concatArrays': ['$fields', '$simple']}, 'relatesTo': 1,
            })
        )
        self.add_pipe(self.sort_('public_id', 1))
        return self.pipeline
