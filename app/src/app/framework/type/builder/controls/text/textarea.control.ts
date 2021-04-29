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

class TextAreaContent implements ControlsContent {

  helperText: string;
  name: string;
  placeholder: string;
  required: boolean;
  type: string;
  value: any;
  label: string;

  public constructor() {
    this.type = 'textarea';
    this.name = randomName(this.type);
    this.label = 'Textarea Field';
  }

}

export class TextAreaControl implements ControlsCommon {

  public name: string = 'textarea';
  public label: string = 'Textarea';
  public icon: string = 'fas fa-align-left';
  public dndType: string = 'inputs';

  public content(): TextAreaContent {
    return new TextAreaContent();
  }

}


