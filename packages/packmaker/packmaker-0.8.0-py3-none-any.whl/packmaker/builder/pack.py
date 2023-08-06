# vim:set ts=4 sw=4 et nowrap syntax=python ff=unix:
#
# Copyright 2020 Mark Crewson <mark@crewson.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .base import BaseBuilder

##############################################################################


class PackBuilder (BaseBuilder):

    build_subloc = 'pack'

    ##########################################################################

    def do_build(self):
        self.log.info('Copying local files ...')
        self.copy_files(self.build_location('files'), self.packlock.yield_clientonly_files())

        self.log.info('Generating packlock manifest file ...')
        self.packlock.save('{}/packmaker.lock'.format(self.build_location()))

        pkgfilename = '{}/{}-{}.{}'.format(self.release_location(),
                                           self.packlock.get_metadata('name'),
                                           self.packlock.get_metadata('version'),
                                           self.release_extension)
        self.log.info('Packaging the modpack: {} ...'.format(pkgfilename))
        self.release_pkg(pkgfilename)

##############################################################################
# THE END
