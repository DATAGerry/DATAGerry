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

import { Component, EventEmitter, Output } from '@angular/core';

export class ExportdLogsSync {
  query: Array<any> | any;
  id: string;
}

@Component({
  selector: 'cmdb-deactivate-exportd-tab',
  templateUrl: './deleted-exportd-tab.component.html',
  styleUrls: ['./deleted-exportd-tab.component.scss']
})
export class DeletedExportdTabComponent {

  /**
   * Outputs the total number of logs.
   */
  @Output() totalLogsChange: EventEmitter<number> = new EventEmitter<number>();

  public query: ExportdLogsSync = {
    query: [
      { $match: { log_type: 'ExportdJobLog' } },
      { $lookup: { from: 'exportd.jobs', localField: 'job_id', foreignField: 'public_id', as: 'job' } },
      { $match: { job: { $size: 0 } } },
      { $project: { job: 0 } }
    ],
    id: 'exportd-logs-table-deleted'
  };

}
