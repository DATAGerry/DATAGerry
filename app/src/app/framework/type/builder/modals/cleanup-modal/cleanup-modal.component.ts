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

import { Component, Input, OnInit} from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { CmdbType } from '../../../../models/cmdb-type';
import { TypeService } from '../../../../services/type.service';
import { UserService } from '../../../../../management/services/user.service';

@Component({
  selector: 'cmdb-cleanup-modal',
  templateUrl: './cleanup-modal.component.html',
  styleUrls: ['./cleanup-modal.component.scss']
})
export class CleanupModalComponent implements OnInit {

  @Input() typeInstance: CmdbType = null;
  public remove: boolean = false;
  public update: boolean = false;

  constructor( private typeService: TypeService, public userService: UserService, public activeModal: NgbActiveModal) {
  }

  ngOnInit() {
    if (this.typeInstance.clean_db === false) {
      this.typeService.cleanupRemovedFields(this.typeInstance.public_id).subscribe(() => {
          this.remove = true;
        }, error => {console.log(error); },
        () => {
          this.typeService.cleanupInsertedFields(this.typeInstance.public_id).subscribe(() => {
              this.update = true;
            }, error => console.log(error),
            () => {
              if (this.remove && this.update) {
                this.typeInstance.clean_db = true;
                this.typeService.putType(this.typeInstance).subscribe(() => {
                  console.log('ok');
                });
              }
            });
        });
    }
  }
}
