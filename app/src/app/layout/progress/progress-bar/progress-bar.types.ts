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

import { BehaviorSubject, interval, Observable, Subscription, timer } from 'rxjs';
import { delay } from 'rxjs/operators';

export class ProgressBarInstance {

  public static readonly INIT_VALUE: number = 0;
  public static readonly MIN_VALUE: number = ProgressBarInstance.INIT_VALUE;
  public static readonly MAX_VALUE: number = 100;
  private worker: Subscription = Subscription.EMPTY;
  private _state: BehaviorSubject<ProgressBarState>;

  constructor() {
    this._state = new BehaviorSubject<ProgressBarState>({ value: 0 });
    this.worker = Subscription.EMPTY;
  }

  public get state(): Observable<ProgressBarState> {
    return this._state.asObservable();
  }

  /**
   * Start the bar increment.
   * @param startDelay MS time before the par starts.
   */
  public start(startDelay = 100): void {
    this._state.next({ value: ProgressBarInstance.INIT_VALUE });

    this.worker = interval(10).pipe(delay(startDelay)).subscribe((val) => {
      this._state.next({ value: this.increment() });
    });

  }

  /**
   * Finish the bar increment.
   */
  public complete(): void {
    this.worker.unsubscribe();
    if (this._state.value.value > 0) {
      this._state.next({ value: 100 });
    }
    const completeTimeout = timer(350).subscribe(() => {
      this._state.next({ value: 0 });
    }).add(() => completeTimeout.unsubscribe());
  }

  /**
   * Step up based on current value.
   * @param rnd
   * @private
   */
  private increment(rnd = ProgressBarInstance.INIT_VALUE) {
    const stat = this._state.value.value;
    if (stat >= ProgressBarInstance.MAX_VALUE) {
      rnd = 0;
    }
    if (rnd === ProgressBarInstance.MIN_VALUE) {
      if (stat >= 0 && stat < 25) {
        rnd = Math.random() * (5 - 3 + 1) + 3;
      } else if (stat >= 25 && stat < 65) {
        rnd = Math.random() * 3;
      } else if (stat >= 65 && stat < 90) {
        rnd = Math.random() * 2;
      } else if (stat >= 90 && stat < 99) {
        rnd = 0.5;
      } else {
        rnd = 0;
      }
    }

    return rnd + stat;
  }
}

export interface ProgressBarState {
  value: number;
}
