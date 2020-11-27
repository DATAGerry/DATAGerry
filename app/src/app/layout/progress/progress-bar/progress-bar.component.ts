/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2020 NETHINKS GmbH
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

import { Component, Input, OnInit, OnDestroy, ViewEncapsulation } from '@angular/core';
import { ProgressBarService } from '../progress-bar.service';
import { ReplaySubject } from 'rxjs';

@Component({
  selector: 'cmdb-progress-bar',
  templateUrl: './progress-bar.component.html',
  styleUrls: ['./progress-bar.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class ProgressBarComponent implements OnInit, OnDestroy {

  public static readonly MIN_VALUE: number = 0;
  public static readonly MAX_VALUE: number = 100;

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Width in percent.
   */
  @Input() public width: number = 0;
  @Input() public ref: string = 'default';
  @Input() public fixed: boolean = true;

  constructor(private progressBarService: ProgressBarService) {
  }

  public ngOnInit(): void {
    this.progressBarService.getRef(this.ref);
  }

  public increase(value: number): void {
    if ((this.width + value) <= ProgressBarComponent.MAX_VALUE) {
      this.width = ProgressBarComponent.MAX_VALUE;
    } else {
      this.width += value;
    }
  }

  public decrease(value: number): void {
    if ((this.width - value) <= ProgressBarComponent.MIN_VALUE) {
      this.width = ProgressBarComponent.MIN_VALUE;
    } else {
      this.width -= value;
    }
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }


}
