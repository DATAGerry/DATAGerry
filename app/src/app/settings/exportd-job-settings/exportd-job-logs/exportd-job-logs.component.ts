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

import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BehaviorSubject, ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'cmdb-task-logs',
  templateUrl: './exportd-job-logs.component.html',
  styleUrls: ['./exportd-job-logs.component.scss']
})
export class ExportdJobLogsComponent implements OnInit, OnDestroy {

  /**
   * Component un-subscriber.
   * @private
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Export query
   */
  public query: any;

  /**
   * ID of the given task.
   * @private
   */
  private taskIDSubject: BehaviorSubject<number> = new BehaviorSubject<number>(undefined);

  constructor(private route: ActivatedRoute) {
    this.route.params.pipe(takeUntil(this.subscriber)).subscribe((id) => this.taskIDSubject.next(id.publicID));
  }

  /**
   * Get the current task id.
   */
  public get taskID(): number {
    return this.taskIDSubject.value;
  }

  public ngOnInit(): void {
    this.taskIDSubject.asObservable().pipe(takeUntil(this.subscriber)).subscribe((id: number) => this.genQuery(id));
  }

  /**
   * Get the query with the task id.
   * @param id
   * @private
   */
  private genQuery(id: number): void {
    this.query = [{
      $match: {
        job_id: id
      }
    }];
  }

  /**
   * Component destroyer.
   */
  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
