/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2021 NETHINKS GmbH
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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { ControlsCommon, randomName, StructureContent } from './controls.common';

export class RefSectionContent implements StructureContent {

  label: string;
  name: string;
  type: string = 'ref-section';
  reference: {
    type_id: number;
    section_name: string;
    selected_fields?: any;
  };

}


export class RefSectionControl implements ControlsCommon {

  name = 'ref-section';
  label = 'Reference';
  icon = 'fas fa-layer-group';
  dndType: string = 'sections';

  content() {
    const section = new RefSectionContent();
    section.name = randomName(this.name);
    section.label = this.label;
    section.reference = {
      type_id: undefined,
      section_name: undefined,
      selected_fields: undefined
    };
    return section;
  }

}
