/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2024 becon GmbH
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

class DateContent implements ControlsContent {

  helperText: string;
  name: string;
  placeholder: string;
  required: boolean;
  type: string;
  value: any;
  label: string;
  format: string;

  public constructor() {
    this.type = 'date';
    this.name = randomName(this.type);
    this.label = 'Date';
  }

}

export class DateControl extends ControlsCommon {

  public name: string = 'date';
  public label: string = 'Date';
  public icon: string = 'fas fa-calendar-alt';
  public dndType: string = 'inputs';

  public content(): DateContent {
    return new DateContent();
  }

}


