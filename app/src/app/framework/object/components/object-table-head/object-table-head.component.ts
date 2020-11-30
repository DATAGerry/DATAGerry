/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2020 NETHINKS GmbH
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

import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CmdbType } from '../../../models/cmdb-type';
import { ExportObjectsFileExtension } from '../../../../export/export-objects/model/export-objects-file-extension';

@Component({
  selector: 'cmdb-object-table-head',
  templateUrl: './object-table-head.component.html',
  styleUrls: ['./object-table-head.component.scss']
})
export class ObjectTableHeadComponent {

  private objectType: CmdbType;
  @Input() set type(type: CmdbType) {
    this.objectType = type;
  }
  get type(): CmdbType {
    return this.objectType;
  }

  @Input() selectedObjects: Array<number> = [];
  @Input() formatList: ExportObjectsFileExtension[] = [];
  @Input() totalResults: number = 0;

  @Output() fileExport: EventEmitter<any> = new EventEmitter<any>();
  @Output() manyObjectDeletes: EventEmitter<any> = new EventEmitter<any>();


}
