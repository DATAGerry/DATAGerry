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

import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { CmdbType } from '../../../models/cmdb-type';
import { TypeService } from '../../../services/type.service';
import { ObjectService } from '../../../services/object.service';
import { UserService } from '../../../../management/services/user.service';
import { ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'cmdb-cleanup-modal',
  templateUrl: './cleanup-modal.component.html',
  styleUrls: ['./cleanup-modal.component.scss']
})
export class CleanupModalComponent implements OnInit, OnDestroy {

  @Input() typeInstance: CmdbType = null;
  public remove: boolean = false;

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  constructor(private typeService: TypeService, private objectService: ObjectService,
              public userService: UserService, public activeModal: NgbActiveModal) {
  }

  public ngOnInit(): void {
    this.objectService.cleanObjects(this.typeInstance.public_id).pipe(takeUntil(this.subscriber))
      .subscribe(() => {
      this.remove = true;
    });
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }
}
