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

import { ControlsCommon, ControlsContent, randomName } from '../controls.common';

class TelContent implements ControlsContent {

  access: boolean;
  helperText: string;
  name: string;
  optional: any;
  placeholder: string;
  required: boolean;
  type: string;
  value: any;
  label: string;
  groups: number[];
  users: number[];

  public constructor() {
    this.type = 'tel';
    this.name = randomName(this.type);
    this.label = 'Phone Field';
  }

}

export class TelControl implements ControlsCommon {

  name = 'phone';
  label = 'Phone';
  icon = 'fas fa-phone';
  dndType: string = 'inputs';

  content() {
    return new TelContent();
  }

}


