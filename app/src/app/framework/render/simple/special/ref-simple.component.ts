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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, AfterViewChecked } from '@angular/core';
import { RenderField } from '../../fields/components.fields';
import { RenderResult } from '../../../models/cmdb-render';
import { ObjectService } from '../../../services/object.service';

@Component({
  selector: 'cmdb-ref-simple',
  templateUrl: './ref-simple.component.html',
  styleUrls: ['./ref-simple.component.scss']
})
export class RefSimpleComponent extends RenderField implements AfterViewChecked {

  public refData: any;

  constructor() {
    super();
  }

  public ngAfterViewChecked() {
    if (this.data && this.data.value && this.data.value !== 0) {
      this.refData = this.data;
    } else {
    }
  }
}
