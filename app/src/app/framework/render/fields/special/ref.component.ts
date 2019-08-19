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

import { Component, OnInit } from '@angular/core';
import { RenderField } from '../components.fields';
import { ObjectService } from '../../../services/object.service';
import { CmdbObject } from '../../../models/cmdb-object';

@Component({
  templateUrl: './ref.component.html',
  styleUrls: ['./ref.component.scss']
})
export class RefComponent extends RenderField implements OnInit {

  public objectList: CmdbObject[];
  public refObject: CmdbObject;

  public constructor(private objectService: ObjectService) {
    super();
  }

  public ngOnInit(): void {
    if (this.data.ref_types !== undefined) {
      this.objectService.getObjectsByType(this.data.ref_types).subscribe((list: CmdbObject[]) => {
        this.objectList = list;
      });
    }
    if (this.controller.value !== undefined) {
      this.objectService.getObject(this.controller.value).subscribe((refObject: CmdbObject) => {
        this.refObject = refObject;
      });
    }
  }


}
