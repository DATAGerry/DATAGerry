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

import {
  ChangeDetectionStrategy,
  Component,
  HostBinding,
  Input,
  OnDestroy,
  OnInit,
  ViewEncapsulation
} from '@angular/core';
import { ProgressSpinnerService } from '../progress-spinner.service';
import { ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { ProgressSpinner } from './progress-spinner.types';

@Component({
  selector: 'cmdb-progress-spinner',
  templateUrl: './progress-spinner.component.html',
  styleUrls: ['./progress-spinner.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class ProgressSpinnerComponent implements OnInit, OnDestroy {

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Reference name for ProgressSpinnerService.
   */
  @Input() public ref: string = 'app';

  /**
   * Z Index value.
   */
  @Input() public zIndex: number = 4000;

  /**
   * Fullscreen enabled
   */
  @Input() public fullScreen: boolean = false;

  /**
   * Fullscreen enabled
   */
  @Input() public text: boolean = true;

  public spinner: ProgressSpinner;

  constructor(private spinnerService: ProgressSpinnerService) {
  }

  public ngOnInit(): void {
    this.spinnerService.getSpinner(this.ref).pipe(takeUntil(this.subscriber)).subscribe(
      (spinner: ProgressSpinner) => {
        this.spinner = spinner;
      });
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }


}
