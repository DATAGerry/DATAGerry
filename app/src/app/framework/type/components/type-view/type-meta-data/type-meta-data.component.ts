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

import { Component, Input, OnInit } from '@angular/core';
import { UserService } from '../../../../../user/services/user.service';
import { CmdbType } from '../../../../models/cmdb-type';
import { User } from '../../../../../user/models/user';

@Component({
  selector: 'cmdb-type-meta-data',
  templateUrl: './type-meta-data.component.html',
  styleUrls: ['./type-meta-data.component.scss']
})
export class TypeMetaDataComponent {

  public currentTypeInstance: CmdbType;
  public author: User = null;

  constructor(private userService: UserService) {

  }

  @Input()
  public set typeInstance(typeInstance: CmdbType) {
    this.currentTypeInstance = typeInstance;
    if (typeInstance !== undefined) {
      this.author = this.userService.findUser(this.typeInstance.author_id);
    }
  }

  public get typeInstance() {
    return this.currentTypeInstance;
  }


}
