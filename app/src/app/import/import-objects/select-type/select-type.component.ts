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

import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { TypeService } from '../../../framework/services/type.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { CmdbType } from '../../../framework/models/cmdb-type';

@Component({
  selector: 'cmdb-select-type',
  templateUrl: './select-type.component.html',
  styleUrls: ['./select-type.component.scss']
})
export class SelectTypeComponent implements OnInit {

  public typeForm: FormGroup;
  public typeList: CmdbType[];
  public typeInstance: CmdbType;
  @Output() public typeChange: EventEmitter<CmdbType>;

  constructor(private typeService: TypeService) {
    this.typeChange = new EventEmitter<CmdbType>();
    this.typeForm = new FormGroup({
      typeID: new FormControl(null, Validators.required)
    });
  }

  public ngOnInit(): void {
    this.typeService.getTypeList().subscribe((typeList: CmdbType[]) => {
      this.typeList = typeList;
    });

    this.typeForm.get('typeID').valueChanges.subscribe((typeID: number) => {
      const typeInit = this.typeList.find(typeInstance => typeInstance.public_id === typeID);
      this.typeInstance = typeInit;
      this.typeChange.emit(typeInit);
    });
  }

}
