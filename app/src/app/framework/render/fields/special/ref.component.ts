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

import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { ComponentsFields } from '../components.fields';
import { ObjectService } from '../../../services/object.service';

@Component({
  selector: 'cmdb-ref',
  templateUrl: './ref.component.html',
  styleUrls: ['./ref.component.scss']
})
export class RefComponent implements OnInit, OnChanges, ComponentsFields {

  @Input() data: any;
  public objectList;

  constructor(private obj: ObjectService) {
  }

  ngOnInit() {

  }

  ngOnChanges(changes: SimpleChanges): void {
    console.log('test');
    if (this.data.ref_types !== 'undefined') {
      this.objectList = this.obj.getObjectsByType(this.data.ref_types);
    }
  }

}
