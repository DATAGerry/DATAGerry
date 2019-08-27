/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 NETHINKS GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.

* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import { ControlsCommon, StructureContent, randomName } from './controls.common';

class SectionContent implements StructureContent {

  label: string;
  name: string;
  position: number;
  access: boolean;
  groups: number[];
  users: number[];
  fields: [] = [];
  type: string = 'section';

}

export class SectionControl implements ControlsCommon {

  name = 'section';
  label = 'Section';
  icon = 'fa fa-square-o';
  dndType: string = 'sections';

  content() {
    const section = new SectionContent();
    section.name = randomName(this.name);
    section.label = this.label;
    return section;
  }

}
