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

import { Component, Input, OnInit } from '@angular/core';
import { TypeService } from '../../../../services/type.service';
import { ConfigEditBaseComponent } from '../config.edit';
import { RenderResult } from '../../../../models/cmdb-render';
import { ObjectService } from '../../../../services/object.service';
import { CmdbType } from '../../../../models/cmdb-type';

@Component({
  selector: 'cmdb-ref-field-edit',
  templateUrl: './ref-field-edit.component.html',
  styleUrls: ['./ref-field-edit.component.scss']
})
export class RefFieldEditComponent extends ConfigEditBaseComponent implements OnInit {
  @Input() groupList: any;
  @Input() userList: any;

  /**
   * Type list for reference selection
   */
  public typeList: CmdbType[];
  public filteredTypeList: CmdbType[] = [];

  /**
   * Nested summaries
   */
  public summaries: any[] = [];

  /**
   * Object list for default reference value
   */
  public objectList: RenderResult[] = [];
  public filteredObjectList: RenderResult[] = [];

  constructor(private typeService: TypeService, private objectService: ObjectService) {
    super();
  }

  public ngOnInit(): void {
    this.typeService.getTypeList().subscribe((res: CmdbType[]) => {
      this.typeList = res;
    }, (err) => console.log(err)
    , () => this.prepareSummaries());

    if (this.data.value !== null && this.data.value !== undefined && this.data.value !== '') {
      this.objectService.getObjectsByType(this.data.ref_types).subscribe((res: RenderResult[]) => {
        this.objectList = res;
      });
    }
  }

  private prepareSummaries() {
    if (this.data.ref_types) {
      if (!Array.isArray(this.data.ref_types)) {
        this.data.ref_types = [this.data.ref_types];
      }
      this.filteredTypeList = this.typeList.filter(type => this.data.ref_types.includes(type.public_id));
      this.data.summaries = this.data.summaries ? this.data.summaries : this.summaries;
      this.summaries = this.data.summaries;
    }
  }

  public onChange() {
    const {ref_types} = this.data;
    if (ref_types && ref_types.length === 0) {
      this.objectList = [];
      this.filteredTypeList = [];
      this.data.value = '';
    } else {
      this.objectService.getObjectsByType(ref_types).subscribe((res: RenderResult[]) => {
        this.objectList = res;
        this.prepareSummaries();
      });
    }
  }

  public summaryFieldFilter(id: number) {
    return id ? this.typeList.find(s => s.public_id === id).fields : [];
  }

  public changeSummaryOption(type: CmdbType) {
    this.summaries.find(s => s.type_id === type.public_id).label = type.label;
  }

  public changeDefault(value: any) {
    this.data.default = parseInt(value, 10);
    return this.data.default;
  }

  public addSummary() {
    if (this.filteredTypeList) {
      this.summaries.push({
        type_id: null,
        line: null,
        label: null,
        fields: [],
        icon: null,
      });
    }
  }

  public delSummary(value: any) {
    if (this.summaries.length > 0) {
      const index = this.summaries.indexOf(value, 0);
      if (index > -1) {
        this.summaries.splice(index, 1);
      }
    }
  }
}
