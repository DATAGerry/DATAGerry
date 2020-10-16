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

import { AfterViewInit, Component, OnDestroy, OnInit } from '@angular/core';
import { User } from '../models/user';
import { APIGetMultiResponse } from '../../services/models/api-response';
import { UserService } from '../services/user.service';
import { ReplaySubject, Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { CollectionParameters } from '../../services/models/api-parameter';
import { Group } from '../models/group';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'cmdb-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.scss']
})
export class UsersComponent implements OnInit, AfterViewInit, OnDestroy {

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  public tableOptions: any;
  public dtTrigger: Subject<void> = new Subject();

  /**
   * Displayed users
   */
  public users: Array<User> = [];

  /**
   * Backend api call
   */
  private apiUsersResponse: APIGetMultiResponse<User>;

  /**
   * List of current loaded groups.
   */
  public groups: Array<Group> = [];

  constructor(private route: ActivatedRoute, private userService: UserService) {
    this.groups = this.route.snapshot.data.groups as Array<Group>;
  }

  public ngOnInit(): void {

    this.tableOptions = {
      columnDefs: [
        { orderable: true, searchable: true, targets: [0, 1, 3] },
        { name: 'public_id', targets: [0] },
        { name: 'user_name', targets: [1] },
        { name: 'display', targets: [2], orderable: false, searchable: false },
        { name: 'email', targets: [3] },
        { name: 'registration_time', targets: [4],  orderable: false, searchable: false },
        { name: 'group_id', targets: [5],  orderable: false, searchable: false },
        { name: 'action', targets: [6], orderable: false, searchable: false }
      ],
      ordering: true,
      searching: true,
      serverSide: true,
      processing: true,
      dom:
        '<"row" <"col-sm-2" l><"col" f> >' +
        '<"row" <"col-sm-12"tr>>' +
        '<\"row\" <\"col-sm-12 col-md-5\"i> <\"col-sm-12 col-md-7\"p> >',
      ajax: (params: any, callback) => {
        let query;
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
          query = [
            { $addFields: { match: { $or: columnQueries } } },
            { $match: { match: true } },
            { $project: { match: 0 } }
          ];
        }

        const apiParameters: CollectionParameters = {
          filter: query,
          page: Math.ceil(params.start / params.length) + 1,
          limit: params.length,
          sort: params.columns[params.order[0].column].name,
          order: params.order[0].dir === 'desc' ? -1 : 1,
        };

        this.userService.getUsers(apiParameters).pipe(
          takeUntil(this.subscriber)).subscribe(
          (response: APIGetMultiResponse<User>) => {
            this.apiUsersResponse = response;
            this.users = response.results;
            callback({
              recordsTotal: response.total,
              recordsFiltered: response.total,
              data: []
            });
          });
      }
    };

  }

  public ngAfterViewInit(): void {
    this.dtTrigger.next();
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
