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

import { Component, OnDestroy, OnInit } from '@angular/core';
import { ConnectionService } from '../../connect/connection.service';
import { AuthService } from '../../auth/services/auth.service';

@Component({
  selector: 'cmdb-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss']
})
export class FooterComponent implements OnInit, OnDestroy {

  public constructor(private connectionService: ConnectionService, private authService: AuthService) {
    this.docUrl = `${ connectionService.currentConnection }/docs`;
  }

  public today: number = Date.now();
  public docUrl: string = 'localhost';
  public userTokenExpire: number = 0;
  public timeout: string = '';
  private timer: number;

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

  public ngOnInit(): void {
    this.userTokenExpire = this.authService.currentUserValue.token_expire;
    this.timeout = FooterComponent.convertToDate(this.calcRestTime(this.userTokenExpire));
    this.interval();
  }

  public interval() {
    this.timer = setInterval(() => {
      this.timeout = FooterComponent.convertToDate(this.calcRestTime(this.userTokenExpire));
    }, 1000);
  }

  public calcRestTime(countDownDate){
    const now = Math.floor(Date.now() / 1000);
    const distance = countDownDate - now;

    if (distance < 0) {
      return 'EXPIRED';
    }
    return distance;
  }

  public ngOnDestroy(): void {
    clearInterval(this.timer);
  }

}





