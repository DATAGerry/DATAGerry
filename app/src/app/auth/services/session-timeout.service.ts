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

import { Injectable, OnDestroy } from '@angular/core';
import { AuthService } from './auth.service';
import { interval, Observable, ReplaySubject, Subject, Subscription } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { Token } from '../models/token';
import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { SessionTimeoutNotificationModalComponent } from '../modals/session-timeout-notification-modal/session-timeout-notification-modal.component';

@Injectable({
  providedIn: 'root'
})
export class SessionTimeoutService implements OnDestroy {

  static readonly TIME_CHECK_INTERVAL: number = 1000;
  static readonly NOTIFICATION_THRESHOLD: number = 60 * 15;

  private notificationModalRef: NgbModalRef;
  private notified: boolean = false;

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();
  private timer$: Observable<number>;
  private timerSubscription = new Subscription();

  public sessionTimeout: Subject<number>;
  public sessionTimeoutRemaining: Subject<string>;

  private tokenExpire: number;

  constructor(private authService: AuthService, private modal: NgbModal) {
    this.authService.currentUserToken.pipe(takeUntil(this.subscriber)).subscribe((token: Token) => {
      if (token) {
        this.tokenExpire = token.expire;
        this.startTimer();
      } else {
        this.stopTimer();
      }
    });
  }

  public static convertToDate(secs) {
    const secsInt = parseInt(secs, 10);
    const days = Math.floor(secsInt / 86400) % 7;
    const hours = Math.floor(secsInt / 3600) % 24;
    const minutes = Math.floor(secsInt / 60) % 60;
    const seconds = secsInt % 60;
    return [days, hours, minutes, seconds]
      .map(v => v < 10 ? '0' + v : v)
      .filter((v, i) => v !== '00' || i > 0)
      .join(':');
  }

  public get remaining(): number {
    if (!this.tokenExpire) {
      return 0;
    }
    const currentTime: number = Math.floor(Date.now() / 1000);
    const distance = this.tokenExpire - currentTime;

    if (distance > 0) {
      return distance;
    }
    return 0;
  }

  private startTimer(): void {
    if (this.timerSubscription) {
      this.stopTimer();
    }
    this.notified = false;
    this.sessionTimeout = new Subject<number>();
    this.sessionTimeoutRemaining = new Subject<string>();
    this.timer$ = interval(SessionTimeoutService.TIME_CHECK_INTERVAL);
    this.timerSubscription = this.timer$.subscribe((t: number) => {
      this.sessionTimeout.next(this.remaining);
      this.sessionTimeoutRemaining.next(SessionTimeoutService.convertToDate(this.remaining));
      if (this.remaining <= 0) {
        this.sessionTimeout.complete();
        this.sessionTimeoutRemaining.complete();
        this.stopTimer();
        this.authService.logout();
      } else if ((this.remaining <= SessionTimeoutService.NOTIFICATION_THRESHOLD) && !this.notified) {
        this.notified = true;
        this.notifyPossibleTimeout();
      }
    });
  }

  private notifyPossibleTimeout() {
    this.notificationModalRef = this.modal.open(SessionTimeoutNotificationModalComponent);
    this.notificationModalRef.componentInstance.remainingTime$ = this.sessionTimeoutRemaining;
    this.notificationModalRef.result.then((result) => {
    });
  }

  private stopTimer(): void {
    this.timerSubscription.unsubscribe();
  }

  public resetTimer(): void {
    this.startTimer();
  }

  public ngOnDestroy(): void {
    this.stopTimer();
    if (this.notificationModalRef) {
      this.notificationModalRef.close();
    }
    this.subscriber.next();
    this.subscriber.complete();
  }
}
