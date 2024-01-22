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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, Input, OnInit, OnDestroy, ViewEncapsulation, HostBinding } from '@angular/core';
import { ProgressBarService } from '../progress-bar.service';
import { Observable, of, ReplaySubject } from 'rxjs';
import { ProgressBarState } from './progress-bar.types';

@Component({
  selector: 'cmdb-progress-bar',
  templateUrl: './progress-bar.component.html',
  styleUrls: ['./progress-bar.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class ProgressBarComponent {

  /**
   * Z Index value.
   */
  @HostBinding('style.z-index') @Input() public zIndex: number = 4000;

  /**
   * Bar height in px.
   */
  @Input() public height: number = 4;

  /**
   * Reference name for ProgressBarService.
   */
  @Input() public ref: string = 'default';

  /**
   * Displayed fixed on top of page.
   */
  @Input() public fixed: boolean = true;

  constructor(private progressBarService: ProgressBarService) {
  }

  /**
   * Get the progress bar state as observable.
   */
  public get state(): Observable<ProgressBarState> {
    return this.progressBarService.getInstance(this.ref).state;
  }

}
