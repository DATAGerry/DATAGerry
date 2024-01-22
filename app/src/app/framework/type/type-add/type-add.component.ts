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

import { Component } from '@angular/core';
import { CmdbType } from '../../models/cmdb-type';
import { ActivatedRoute } from '@angular/router';
import { TypeService } from '../../services/type.service';
import { UserService } from '../../../management/services/user.service';

@Component({
  selector: 'cmdb-type-add',
  templateUrl: './type-add.component.html',
  styleUrls: ['./type-add.component.scss']
})
export class TypeAddComponent {
  public typeInstance: CmdbType;

  constructor(private route: ActivatedRoute, private typeService: TypeService, private userService: UserService) {
    this.typeInstance = new CmdbType();
    this.route.queryParams.subscribe((query) => {
      if (query.copy !== undefined) {
        this.typeService.getType(query.copy).subscribe((copyType: CmdbType) => {
          // @ts-ignore
          delete copyType.public_id;
          // @ts-ignore
          delete copyType._id;
          delete copyType.author_id;
          this.typeInstance = copyType;
          this.typeInstance.author_id = this.userService.getCurrentUser().public_id;
        });
      }
    });
  }

}
