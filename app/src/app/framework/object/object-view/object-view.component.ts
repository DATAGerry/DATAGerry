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
import { ApiCallService } from '../../../services/api-call.service';
import { ActivatedRoute, Router } from '@angular/router';
import { CmdbObject } from '../../models/cmdb-object';
import { ObjectService } from '../../services/object.service';
import { CmdbType } from '../../models/cmdb-type';
import { TypeService } from '../../services/type.service';
import { CmdbMode } from '../../modes.enum';

@Component({
  selector: 'cmdb-object-view',
  templateUrl: './object-view.component.html',
  styleUrls: ['./object-view.component.scss']
})
export class ObjectViewComponent implements OnInit {

  public mode: CmdbMode = CmdbMode.View;
  private objectID: number;
  public objectInstance: CmdbObject;
  public typeInstance: CmdbType;

  constructor(private api: ApiCallService, private objectService: ObjectService, private typeService: TypeService,
              private route: ActivatedRoute) {
    this.route.params.subscribe((params) => {
      this.objectID = params.publicID;
    });
  }

  public ngOnInit(): void {
    // RenderResult
    this.objectService.getObject(this.objectID).subscribe((objectInstanceResp: CmdbObject) => {
      this.objectInstance = objectInstanceResp;
    }, (error) => {
      console.error(error);
    }, () => {
      this.typeService.getType(this.objectInstance.type_id).subscribe((typeInstanceResp: CmdbType) => {
        this.typeInstance = typeInstanceResp;
      });
    });
  }

}
