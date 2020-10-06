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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, OnDestroy, OnInit } from '@angular/core';
import { GroupService } from '../services/group.service';
import { ReplaySubject } from 'rxjs';
import { Group } from '../models/group';
import { APIGetMultiResponse } from '../../services/models/api-response';
import { CollectionParameters } from '../../services/models/api-parameter';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'cmdb-groups',
  templateUrl: './groups.component.html',
  styleUrls: ['./groups.component.scss']
})
export class GroupsComponent implements OnInit, OnDestroy {

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  public groups: Array<Group> = [];
  private groupAPIResponse: APIGetMultiResponse<Group>;
  public tableOptions: any;

  constructor(private groupService: GroupService) {
  }

  public ngOnInit(): void {
    this.tableOptions = {
      columnDefs: [
        {
          orderable: true,
          searchable: true,
          targets: [0, 1, 2]
        },
        {
          name: 'public_id',
          targets: [0]
        },
        {
          name: 'name',
          targets: [1]
        },
        {
          name: 'label',
          targets: [2]
        },
        {
          name: 'action',
          targets: [3],
          orderable: false,
          searchable: false
        }
      ],
      ordering: true,
      searching: true,
      serverSide: true,
      processing: true,
      ajax: (params: any, callback) => {
        let filter;
        if (params.search.value !== '') {
          const searchableColumns = params.columns.filter(column => {
            return column.searchable === true;
          });

          const columnQueries = [];
          for (const column of searchableColumns) {
            const regex = {
              $regexMatch: {
                input: { $toString: `$${ column.name }` },
                regex: params.search.value,
                options: 'ismx'
              }
            };
            columnQueries.push(regex);
          }
          const query = [
            { $addFields: { match: { $or: columnQueries } } },
            { $match: { match: true } },
            { $project: { match: 0 } }
          ];
          filter = JSON.stringify(query);
        }

        const apiParameters: CollectionParameters = {
          filter,
          page: Math.ceil(params.start / params.length) + 1,
          limit: params.length,
          sort: params.columns[params.order[0].column].name,
          order: params.order[0].dir === 'desc' ? -1 : 1,
        };

        this.groupService.getGroups(apiParameters).pipe(
          takeUntil(this.subscriber)).subscribe(
          (response: APIGetMultiResponse<Group>) => {
            this.groupAPIResponse = response;
            this.groups = this.groupAPIResponse.results;
            callback({
              recordsTotal: response.total,
              recordsFiltered: response.total,
              data: []
            });
          });
      }
    };

  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
