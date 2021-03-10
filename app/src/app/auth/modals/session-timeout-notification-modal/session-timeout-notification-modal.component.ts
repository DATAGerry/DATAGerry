/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2021 NETHINKS GmbH
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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { Observable, ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'cmdb-session-timeout-notification-modal',
  templateUrl: './session-timeout-notification-modal.component.html',
  styleUrls: ['./session-timeout-notification-modal.component.scss']
})
export class SessionTimeoutNotificationModalComponent implements OnInit, OnDestroy {

  /**
   * Component un-subscriber.
   * @private
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Timeout observer of the session timeout service.
   */
  @Input() public remainingTime$: Observable<string>;

  /**
   * Dateformat of the remaining token lifetime.
   */
  public remainingTime: string = '';

  /**
   * Renew session password form group.
   */
  public form: FormGroup;

  constructor(public activeModal: NgbActiveModal) {
    this.form = new FormGroup({
      password: new FormControl('', Validators.required)
    });
  }

  /**
   * Entered password from the form.
   */
  public get password(): string {
    return this.form.get('password').value;
  }

  /**
   * On password pass.
   */
  public onRenew(): void {
    if (this.form.valid) {
      this.activeModal.close({ password: this.password });
    }
  }

  public ngOnInit(): void {
    this.remainingTime$.pipe(takeUntil(this.subscriber)).subscribe((timeout: string) => this.remainingTime = timeout);
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }


}
