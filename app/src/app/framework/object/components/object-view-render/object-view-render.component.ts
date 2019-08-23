/*
* dataGerry - OpenSource Enterprise CMDB
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

import { Component, Input } from '@angular/core';
import { CmdbMode } from '../../../modes.enum';
import { CmdbType } from '../../../models/cmdb-type';
import { CmdbObject } from '../../../models/cmdb-object';
import { FormGroup } from '@angular/forms';

@Component({
  selector: 'cmdb-object-view-render',
  templateUrl: './object-view-render.component.html',
  styleUrls: ['./object-view-render.component.scss']
})
export class ObjectViewRenderComponent {

  @Input() public mode: CmdbMode = CmdbMode.View;
  @Input() public objectInstance: CmdbObject;
  @Input() public typeInstance: CmdbType;
  public renderForm: FormGroup;
  public fieldsGroups: FormGroup;

  public constructor() {
    this.renderForm = new FormGroup({});
    this.fieldsGroups = new FormGroup({});
  }


}
