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
import { ApiCallService } from '../../../../services/api-call.service';
import {ActivatedRoute, Router} from '@angular/router';
import {CmdbObject} from '../../../models/cmdb-object';
import {ObjectService} from '../../../services/object.service';

@Component({
  selector: 'cmdb-type-view',
  templateUrl: './object-view.component.html',
  styleUrls: ['./object-view.component.scss']
})
export class ObjectViewComponent implements OnInit {

  private objID: number;
  private objectInstance: any;
  public editDisable: boolean = true;

  constructor(private api: ApiCallService, private objService: ObjectService,
              private activRoute: ActivatedRoute, private route: Router) {
    this.activRoute.params.subscribe((id) => {
      this.objID = id.publicID;
      this.ngOnInit();
    });
  }

  ngOnInit() {
    this.api.callGetRoute<any>('object/' + `${this.objID}`)
      .subscribe(obj => this.objectInstance = obj);
  }

  public delObject(value: any) {
    const id = value.object_id;
    this.api.callDeleteRoute('object/' + id).subscribe(data => {
      this.route.navigate(['/']);
    });
  }

  public copy(clone: any) {
    const newInstance = new CmdbObject();
    newInstance.version = '1.0.0';
    newInstance.type_id = clone.type_id;
    newInstance.author_id = clone.author_id;
    newInstance.active = clone.type_active;
    newInstance.fields = clone.obj_fields;

    this.objService.postAddObject(newInstance).subscribe(res => {
      this.route.navigate(['framework/object/' + res]);
    });
  }

  public isEditable() {
    return this.editDisable = !this.editDisable;
  }
}
