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

import { Component, OnInit } from '@angular/core';
import { RenderField } from '../components.fields';
import { ObjectService } from '../../../services/object.service';
import { RenderResult } from '../../../models/cmdb-render';
import { Observable } from 'rxjs';

@Component({
  templateUrl: './ref.component.html',
  styleUrls: ['./ref.component.scss']
})
export class RefComponent extends RenderField implements OnInit {

  public objectList: Observable<RenderResult[]>;
  public refObject: RenderResult;

  public constructor(private objectService: ObjectService) {
    super();
  }

  public ngOnInit(): void {
    if (this.data.ref_types !== undefined) {
      this.objectList = this.objectService.getObjectsByType(this.data.ref_types);
    }
    if (this.controller.value !== '' && this.data.value !== undefined) {
      this.objectService.getObject(this.controller.value).subscribe((refObject: RenderResult) => {
          this.refObject = refObject;
        },
        (error) => {
          console.error(error);
        });
    }
  }

  public searchRef(term: string, item: any) {
    term = term.toLocaleLowerCase();
    const value = item.object_information.object_id + item.type_information.type_label + item.summary_line;
    return value.toLocaleLowerCase().indexOf(term) > -1 || value.toLocaleLowerCase().includes(term);
  }
}
