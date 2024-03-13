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
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CmdbType } from '../../../models/cmdb-type';
import { SupportedExporterExtension } from '../../../../export/export-objects/model/supported-exporter-extension';
import { RenderResult } from '../../../models/cmdb-render';
import { Router } from '@angular/router';

@Component({
  selector: 'cmdb-object-table-head',
  templateUrl: './object-table-head.component.html',
  styleUrls: ['./object-table-head.component.scss']
})
export class ObjectTableHeadComponent {

  @Input() public selectedObjects: Array<RenderResult> = [];
  @Input() public selectedObjectsIDs: Array<number> = [];
  @Input() public formatList: SupportedExporterExtension[] = [];
  @Input() public totalResults: number = 0;

  @Output() public fileExport: EventEmitter<any> = new EventEmitter<any>();
  @Output() public manyObjectDeletes: EventEmitter<any> = new EventEmitter<any>();

  @Input() public type: CmdbType;

  public constructor(private router: Router) {

  }

  public onBulkChange(): void {
    this.router.navigate(['/framework/object/change/'],
      { state: { type: this.type, objects: this.selectedObjects } });
  }

  public exporter(see: SupportedExporterExtension, view: string = 'native'): void {
    see.view = view;
    this.fileExport.emit(see);
  }
}
